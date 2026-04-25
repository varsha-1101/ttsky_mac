`default_nettype none

module tt_um_mac (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path
    input  wire       ena,      // always 1 when powered
    input  wire       clk,      // clock
    input  wire       rst_n     // active-low reset
);

    // -----------------------------
    // Input mapping
    // -----------------------------
    wire [3:0] a = ui_in[3:0];   // first operand
    wire [3:0] b = ui_in[7:4];   // second operand

    // -----------------------------
    // Internal register (accumulator)
    // -----------------------------
    reg [7:0] acc;

    // -----------------------------
    // Multiply and accumulate
    // -----------------------------
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            acc <= 8'b0;
        else
            acc <= acc + (a * b);
    end

    // -----------------------------
    // Output mapping
    // -----------------------------
    assign uo_out = acc;

    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    // -----------------------------
    // Unused signals
    // -----------------------------
    wire _unused = &{ena, uio_in};

endmodule
