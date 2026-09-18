module counter8bit (
    input wire en, // wire means it is driven externally and reg is for if the thing is dynamically chaning in the always block
    input wire clk,
    input wire ld,
    input wire rst,          // example input driving transitions
    input wire [7:0] load,
    output wire [7:0] out      // example output
);

    // State encoding
    // localparam acts like a #DEFINE in Cpp

    reg [7:0] count;

    // 1) State register (sequential) - only place state actually updates
    always @(posedge clk or posedge rst) begin

        if (rst)
            count <= 8'h00;

        else
            if (ld)
                count <= load;
            else
                count <= count + 1'b1; //overflow auto mods it
    end

    // // 2) Next-state logic (combinational) - decides where to go
    // always @(*) begin
    //         next_state = ld ? LD : CT;
    //         default: next_state = CT;
    // end

    // 3) Output logic (combinational) - Moore style: output depends only on state

    assign out = en ? count : 8'bZZZZZZZZ;

endmodule
