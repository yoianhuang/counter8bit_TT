import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def test_counter8bit(dut):
    """Test asynchronous reset, synchronous load, continuous counting, and tri-state control."""

    # 1. Start a 10ns clock (100 MHz)
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    # Initialize inputs
    dut.rst.value = 0
    dut.en.value = 0
    dut.ld.value = 0
    dut.load.value = 0
    await Timer(2, unit="ns")

    # 2. Test Asynchronous Reset
    dut.rst.value = 1
    await Timer(5, unit="ns")
    dut.rst.value = 0
    await Timer(1, unit="ns")

    # 3. Verify High-Z output when disabled
    assert str(dut.out.value).lower() == "zzzzzzzz", f"Expected 'zzzzzzzz', got {dut.out.value}"

    # 4. Enable Output and Check Value BEFORE Next Clock Edge (Should be 0)
    dut.en.value = 1
    await Timer(1, unit="ns")
    assert dut.out.value == 0, f"Expected 0 after reset, got {dut.out.value}"

    # 5. Let it count once
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    assert dut.out.value == 1, f"Expected 1, got {dut.out.value}"

    # 6. Test Synchronous Load
    dut.load.value = 0x42
    dut.ld.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    dut.ld.value = 0
    assert dut.out.value == 0x42, f"Expected 0x42, got {hex(dut.out.value.integer)}"

    # 7. Test Continuous Counting while Output Disabled (en = 0)
    dut.en.value = 0
    await RisingEdge(dut.clk)  # Counter becomes 0x43
    await RisingEdge(dut.clk)  # Counter becomes 0x44
    await Timer(1, unit="ns")
    assert str(dut.out.value).lower() == "zzzzzzzz", "Output should stay high-Z while en=0"

    # 8. Re-enable Output and Verify Internal Counter Advanced
    dut.en.value = 1
    await Timer(1, unit="ns")
    assert dut.out.value == 0x44, f"Expected 0x44, got {hex(dut.out.value.integer)}"
