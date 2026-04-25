<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This project implements a simple **Multiplier–Accumulator (MAC)** unit.

The design takes an 8-bit input (`ui_in`) and splits it into two 4-bit operands:
- `a = ui_in[3:0]`
- `b = ui_in[7:4]`

On every rising edge of the clock:
- The two inputs are multiplied (`a × b`)
- The result is added to an internal 8-bit accumulator register

The accumulator stores the running sum of all previous multiplications:
 acc = acc + (a × b)

The accumulator is reset to 0 when `rst_n = 0`.

The current accumulated value is continuously output on:
- `uo_out[7:0]`

All bidirectional IOs (`uio_*`) are unused in this design.

---

## How to test

This design is tested using a cocotb-based testbench.

### Test steps:

1. **Reset the design**
   - Set `rst_n = 0`
   - Wait a few clock cycles
   - Set `rst_n = 1`

2. **Apply inputs**
   - Provide values for `a` and `b` using `ui_in`:
     ```
     ui_in = (b << 4) | a
     ```

3. **Wait for one clock cycle**
   - The multiplication and accumulation occur on the rising edge

4. **Check output**
   - Verify `uo_out` equals the expected accumulated result

### Example:

| Cycle | a | b | a×b | Accumulator |
|-------|---|---|-----|-------------|
| 1 | 2 | 3 | 6 | 6 |
| 2 | 1 | 4 | 4 | 10 |
| 3 | 2 | 2 | 4 | 14 |

The cocotb testbench automatically performs these checks using assertions.

---

## External hardware

No external hardware is required.

The design is fully digital and intended for simulation and ASIC implementation within the Tiny Tapeout framework.
