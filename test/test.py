import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer, ClockCycles

@cocotb.test()
async def test_project(dut):
    # 10ns clock (100 MHz)
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    # Set default values
    dut.ena.value = 1
    dut.ui_in.value = 0   # en=0, ld=0
    dut.uio_in.value = 0  # load value

    # Apply active-low reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await Timer(1, unit="ns")

    # 1. Tri-state check when en=0
    assert str(dut.uo_out.value).lower() == "zzzzzzzz"

    # 2. Enable output (en=1) -> Should be 0 before next posedge clk
    dut.ui_in.value = 0b00000001
    await Timer(1, unit="ns")
    assert dut.uo_out.value == 0, f"Expected 0 after reset, got {dut.uo_out.value}"

    # 3. Synchronous Load (ld=1, load=0xAB)
    dut.uio_in.value = 0xAB
    dut.ui_in.value = 0b00000011  # en=1, ld=1
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    dut.ui_in.value = 0b00000001  # en=1, ld=0
    assert dut.uo_out.value == 0xAB, f"Expected 0xAB, got {hex(dut.uo_out.value.integer)}"

    # 4. Count up (0xAB + 1 = 0xAC)
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    assert dut.uo_out.value == 0xAC, f"Expected 0xAC, got {hex(dut.uo_out.value.integer)}"
