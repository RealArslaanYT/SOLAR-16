# SOLAR-16 v1.0 | ISA/Instruction Set Architecture
SOLAR-16 - A dead-simple 16-bit CPU Instruction Set.  

Developed by Arslaan Pathan  
(C) Copyright 2025  Arslaan Pathan

- 16-bit registers/16-bit architecture
- 32-bit long instructions (4 bytes)
- 16 registers
- Little endian (0x12345678 = [0x78, 0x56, 0x34, 0x12])
- Harvard-style memory management (Code and data have seperate memory)
- I/O is memory-mapped to data memory
- Memory mapped output port = 0xFF00
- Memory mapped input port = 0xFF10

## Arithmetic/Maths

**ADD**: 0x00
- Usage: ADD Rd, Imm16
- Adds an immediate value to the value in a register. If result is 0, sets the zero flag. Otherwise, clears it.
- Example: 0x00 0x01 0x20 0x00 - Adds 32 to the value in register R1

**SUB**: 0x01
- Usage: SUB Rd, Imm16
- Subtracts an immediate value from the value in a register. If result is 0, sets the zero flag. Otherwise, clears it.
- Example: 0x01 0x01 0x20 0x00 - Subtracts 32 from the value in register R1

**MUL**: 0x02
- Usage: MUL Rd, Imm16
- Multiplies the value in a register by an immediate value. If result is 0, sets the zero flag. Otherwise, clears it.
- Example: 0x02 0x01 0x02 0x00 - Multiplies the value in register R1 by 2

**RADD**: 0x03
- Usage: RADD Rd, Rs
- Adds an value in a register to the value in another register. If result is 0, sets the zero flag. Otherwise, clears it.
- Example: 0x03 0x01 0x02 0x00 - Adds the value in register R2 to the value in register R1

**RSUB**: 0x04  
- Usage: RSUB Rd, Rs  
- Subtracts the value in register Rs from the value in register Rd. If result is 0, sets the zero flag. Otherwise, clears it.  
- Example: 0x04 0x01 0x02 0x00 - Subtracts the value in register R2 from the value in register R1.

**RMUL**: 0x05  
- Usage: RMUL Rd, Rs  
- Multiplies the value in register Rd by the value in register Rs. If result is 0, sets the zero flag. Otherwise, clears it.  
- Example: 0x05 0x01 0x02 0x00 - Multiplies the value in register R1 by the value in register R2.


## Memory & Registers

**MOV**: 0x10
- Usage: MOV Rd, Rs
- Moves contents of a register into another
- Example: 0x10 0x03 0x01 0x00 - Moves the contents of register R1 into R3

**LD**: 0x11
- Usage: LD Rd, Address16
- Loads from memory into register
- Example: 0x11 0x04 0x00 0x10 - Loads from address 0x1000 into register R4

**ST**: 0x12
- Usage: ST Rs, Address16
- Stores from register into memory
- Example: 0x12 0x05 0x00 0x10 - Stores the contents of register R5 to memory address 0x1000

**CLR** 0x13
- Usage: CLR Rd
- Clears the value in a register by setting it to zero. Sets the zero flag.
- Example: 0x13 0x01 0x00 0x00 - Clears the value in register R1.

## Control Flow

**JMP**: 0x20
- Usage: JMP 0x00, Address16
- Jumps to address
- Example: 0x20 0x00 0x10 0x00 - Jumps to address 0x0010

**JZ**: 0x21
- Usage: JZ 0x00, Address16
- Jumps to address if zero flag set
- Example: 0x21 0x00 0x34 0x12 - Jumps to address 0x1234 if zero flag is set

**JNZ**: 0x22
- Usage: JNZ 0x00, Address16
- Jumps to address if zero flag not set
- Example: 0x22 0x00 0x34 0x12 - Jumps to address 0x1234 if zero flag is not set

**HALT**: 0x23
- Usage: HALT 0x00 0x00 0x00
- Stops execution.
- Example: 0x23 0x00 0x00 0x00

## Logic

**CMP**: 0x30
- Usage: CMP Rd, Rs
- Compares the value in Rd with Rs. Sets the zero flag if equal, otherwise clears it.
- Example: 0x30 0x04 0x03 0x00 - Compares the values in register R3 and R4

## Bitwise operations

**AND**: 0x40
- Usage: AND Rd, Rs
- Rd = Rd & Rs
- Example: 0x40 0x01 0x02 0x00 - Performs a bitwise AND on registers R1 and R2 and stores the result back in register R1

**NOT**: 0x41
- Usage: NOT Rd
- Inverts all the bits in register Rd. 
- Example: 0x41 0x04 0x00 0x00 - Inverts the bits in register R4

**OR**: 0x42
- Usage: OR Rd, Rs
- Performs a bitwise OR on Rd and Rs.
- Example: 0x42 0x05 0x03 0x00 - Performs a bitwise OR on registers R5 and R3 and stores the result back in register R5

**XOR**: 0x43
- Usage: XOR Rd, Rs
- Performs a bitwise XOR on Rd and Rs.
- Example: 0x43 0x05 0x03 0x00 - Performs a bitwise XOR on registers R5 and R3 and stores the result back in register R5

**SHL**: 0x44
- Usage: SHL Rd, Imm4 (lower 4 bits of the immediate byte)
- Shifts bits in Rd left by immediate value (Imm4), filling with zeros on the right.
- Example: 0x44 0x01 0x03 0x00 - Shifts bits in register R1 by 3 bits to the left

**SHR**: 0x45
- Usage: SHR Rd, Imm4 (lower 4 bits of the immediate byte)
- Shifts bits in Rd right by immediate value (Imm4), filling with zeros on the left.
- Example: 0x45 0x01 0x03 0x00 - Shifts bits in register R1 by 3 bits to the right

## Misc
**NOP**: 0xFF
- Usage: NOP 0x00 0x00 0x00
- Luigi wins by doing absolutely nothing.
- Example: 0xFF 0x00 0x00 0x00 - Does nothing.

**CLZ**: 0xF0
- Usage: CLZ 0x00 0x00 0x00
- Clears the zero flag.
- Example: 0xF0 0x00 0x00 0x00 - Clears the zero flag.

## System/More information
- Clock Speed: 20 MHz
- Flags:
  - Zero flag
    - Gets set and cleared by Arithmetic operations, Bitwise operations, and the CMP operation.