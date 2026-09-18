`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when powered
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // Map TT signals to counter inputs
    wire en   = ui_in[0];
    wire ld   = ui_in[1];
    wire rst  = ~rst_n;         // Active-low to Active-high
    wire [7:0] load = uio_in;   // Use bidirectional bus as input for load

    // Set bidirectional IOs as inputs
    assign uio_oe  = 8'b00000000;
    assign uio_out = 8'b00000000;

    // Instantiate your 8-bit counter
    counter8bit my_counter (
        .en(en),
        .clk(clk),
        .ld(ld),
        .rst(rst),
        .load(load),
        .out(uo_out)
    );

endmodule

module counter8bit (
    input  wire       en,
    input  wire       clk,
    input  wire       ld,
    input  wire       rst,
    input  wire [7:0] load,
    output wire [7:0] out
);

    reg [7:0] count;

    always @(posedge clk or posedge rst) begin
        if (rst)
            count <= 8'h00;
        else if (ld)
            count <= load;
        else
            count <= count + 1'b1;
    end

    assign out = en ? count : 8'bZZZZZZZZ;

endmodule
