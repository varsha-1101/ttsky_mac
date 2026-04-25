# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Clock: 10 us period
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # -----------------------------
    # Reset
    # -----------------------------
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 5)

    dut.rst_n.value = 1

    # -----------------------------
    # Test MAC behavior
    # -----------------------------
    dut._log.info("Test MAC behavior")

    # a = ui_in[3:0], b = ui_in[7:4]

    # Test 1: a=2, b=3 → acc = 6
    dut.ui_in.value = (3 << 4) | 2   # b=3, a=2
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 6, f"Expected 6, got {int(dut.uo_out.value)}"

    # Test 2: a=1, b=4 → acc = 6 + 4 = 10
    dut.ui_in.value = (4 << 4) | 1
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 10, f"Expected 10, got {int(dut.uo_out.value)}"

    # Test 3: a=2, b=2 → acc = 10 + 4 = 14
    dut.ui_in.value = (2 << 4) | 2
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 14, f"Expected 14, got {int(dut.uo_out.value)}"

    # Test 4: a=3, b=3 → acc = 14 + 9 = 23
    dut.ui_in.value = (3 << 4) | 3
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 23, f"Expected 23, got {int(dut.uo_out.value)}"

    dut._log.info("All tests passed!")
