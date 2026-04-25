# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):

    # -----------------------------
    # Start clock (IMPORTANT)
    # -----------------------------
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # -----------------------------
    # Reset
    # -----------------------------
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1

    # -----------------------------
    # Cycle 1: 2 * 3 = 6
    # -----------------------------
    dut.ui_in.value = (3 << 4) | 2
    await ClockCycles(dut.clk, 1)
    assert int(dut.uo_out.value) == 6

    # -----------------------------
    # Cycle 2: + (1 * 4) = 10
    # -----------------------------
    dut.ui_in.value = (4 << 4) | 1
    await ClockCycles(dut.clk, 1)
    assert int(dut.uo_out.value) == 10

    # -----------------------------
    # Cycle 3: + (2 * 2) = 14
    # -----------------------------
    dut.ui_in.value = (2 << 4) | 2
    await ClockCycles(dut.clk, 1)
    assert int(dut.uo_out.value) == 14
