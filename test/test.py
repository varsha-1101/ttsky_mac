import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):

    cocotb.start_soon(Clock(dut.clk, 10, unit="us").start())

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 3)
    dut.rst_n.value = 1

    # IMPORTANT: wait extra cycle after reset
    await ClockCycles(dut.clk, 2)

    def apply(a, b):
        dut.ui_in.value = (b << 4) | a

    # Cycle 1
    apply(2, 3)
    await ClockCycles(dut.clk, 2)
    assert int(dut.uo_out.value) == 6

    # Cycle 2
    apply(1, 4)
    await ClockCycles(dut.clk, 2)
    assert int(dut.uo_out.value) == 10

    # Cycle 3
    apply(2, 2)
    await ClockCycles(dut.clk, 2)
    assert int(dut.uo_out.value) == 14
