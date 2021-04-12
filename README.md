# MIPS Disassembler
Details:
-  Input: the 32-bit machine instructions that a compiler or assembler produces (i.e. `0x032BA020`)
- Output: the original source instructions that created those 32-bit machine instructions (i.e. `9A040 add $20, $25, $11`)
- The possible source instructions are: add, sub, and, or, slt, lw, sw, beq, bne
- The first instruction begins at address hex 9A040 and the rest follow right after that one