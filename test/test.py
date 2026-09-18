import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def test_project(dut):
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    # Enable design and set default inputs
    dut.ena.value = 1
    dut.ui_in.value = 0   # [0]=en, [1]=ld
    dut.uio_in.value = 0  # load value bus
    dut.rst_n.value = 0  # Assert reset (active low)
    await Timer(10, unit="ns")
    dut.rst_n.value = 1  # Deassert reset
    await Timer(1, unit="ns")

    # 1. Tri-state output check (en=0)
    assert str(dut.uo_out.value).lower() == "zzzzzzzz"

    # 2. Enable output (en=1) -> Should be 0
    dut.ui_in.value = 0b00000001
    await Timer(1, unit="ns")
    assert dut.uo_out.value == 0

    # 3. Synchronous Load (ld=1, load=0xAB)
    dut.uio_in.value = 0xAB
    dut.ui_in.value = 0b00000011  # en=1, ld=1
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    dut.ui_in.value = 0b00000001  # en=1, ld=0
    assert dut.uo_out.value == 0xAB

    # 4. Count up
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    assert dut.uo_out.value == 0xAC
