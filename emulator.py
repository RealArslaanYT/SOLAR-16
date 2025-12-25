# SOLAR-16 - A custom CPU architecture/ISA
# emulator.py
# (C) Copyright 2025  Arslaan Pathan
import sys
import time


class SOLAR16:
    def __init__(self, code_bytes):
        self.registers = [0] * 16
        self.flags = {
            "zero_flag": False
        }
        self.instruction_memory = code_bytes
        self.data_memory = [0] * (2 ** 16)
        self.cycle_duration = 1 / 20_000_000  # 20 MHz
        self.PC = 0
        self.halted = False
        self.instruction_size = 4  # 4 bytes/32-bit instruction size

    def fetch(self):
        return self.instruction_memory[self.PC:self.PC + self.instruction_size]

    def decode(self, instruction_bytes):
        opcode = instruction_bytes[0]
        operand1 = instruction_bytes[1]
        operand2 = instruction_bytes[2]
        operand3 = instruction_bytes[3]
        return opcode, operand1, operand2, operand3

    def execute(self, opcode, op1, op2, op3):
        if opcode == 0x00:  # ADD Rd, Imm16
            rd = op1
            imm = op2 | (op3 << 8)  # little endian immediate
            self.registers[rd] = (self.registers[rd] + imm) & 0xFFFF
            self.flags['zero_flag'] = (self.registers[rd] == 0)
            self.PC += self.instruction_size

        elif opcode == 0x01:  # SUB Rd, Imm16
            rd = op1
            imm = op2 | (op3 << 8)  # little endian immediate
            self.registers[rd] = (self.registers[rd] - imm) & 0xFFFF
            self.flags['zero_flag'] = (self.registers[rd] == 0)
            self.PC += self.instruction_size

        elif opcode == 0x02:  # MUL Rd, Imm16
            rd = op1
            imm = op2 | (op3 << 8)  # little endian immediate
            self.registers[rd] = (self.registers[rd] * imm) & 0xFFFF
            self.flags['zero_flag'] = (self.registers[rd] == 0)
            self.PC += self.instruction_size

        elif opcode == 0x03:  # RADD Rd, Rs
            rd = op1
            rs = op2
            self.registers[rd] = (self.registers[rd] + self.registers[rs]) & 0xFFFF
            self.flags['zero_flag'] = (self.registers[rd] == 0)
            self.PC += self.instruction_size

        elif opcode == 0x04:  # RSUB Rd, Rs
            rd = op1
            rs = op2
            self.registers[rd] = (self.registers[rd] - self.registers[rs]) & 0xFFFF
            self.flags['zero_flag'] = (self.registers[rd] == 0)
            self.PC += self.instruction_size

        elif opcode == 0x05:  # RMUL Rd, Rs
            rd = op1
            rs = op2
            self.registers[rd] = (self.registers[rd] * self.registers[rs]) & 0xFFFF
            self.flags['zero_flag'] = (self.registers[rd] == 0)
            self.PC += self.instruction_size

        elif opcode == 0x10:  # MOV Rd, Rs
            rd = op1
            rs = op2
            self.registers[rd] = self.registers[rs]
            self.PC += self.instruction_size


        elif opcode == 0x11:  # LD Rd, Addr
            rd = op1
            addr = op2 | (op3 << 8)  # little endian address
            if addr == 0xFF10:
                user_char = sys.stdin.read(1)
                if user_char == '' or user_char == '\n':
                    # No input, maybe set zero or -1 or block
                    val = 0
                else:
                    val = ord(user_char)
                self.registers[rd] = val & 0xFFFF
            else:
                low = self.data_memory[addr]
                high = self.data_memory[(addr + 1) & 0xFFFF]
                self.registers[rd] = low | (high << 8)

            self.PC += self.instruction_size

        elif opcode == 0x12:  # ST Rs, Addr16
            rd = op1
            addr = op2 | (op3 << 8)  # combine low and high bytes to get address
            val = self.registers[rd]  # get 16-bit value from register
            self.data_memory[addr] = val & 0xFF
            self.data_memory[addr + 1] = (val >> 8) & 0xFF

            if addr == 0xFF00:
                # Print the ASCII char to host console
                print(chr(self.data_memory[addr]), end='', flush=True)

            self.PC += self.instruction_size

        elif opcode == 0x13:  # CLR Rd
            rd = op1
            self.registers[rd] = 0
            self.flags['zero_flag'] = True
            self.PC += 4

        elif opcode == 0x20:  # JMP 0x00, Addr16
            addr = op2 | (op3 << 8)  # combine low and high bytes to get address
            self.PC = addr

        elif opcode == 0x21:  # JZ 0x00, Addr16
            addr = op2 | (op3 << 8)  # combine low and high bytes to get address
            if self.flags['zero_flag']:
                self.PC = addr
            else:
                self.PC += self.instruction_size

        elif opcode == 0x22:  # JNZ 0x00, Addr16
            addr = op2 | (op3 << 8)  # combine low and high bytes to get address
            if not self.flags['zero_flag']:
                self.PC = addr
            else:
                self.PC += self.instruction_size

        elif opcode == 0x23:  # HALT
            self.halted = True

        elif opcode == 0x30:  # CMP Rd, Rs
            rd = op1
            rs = op2
            self.flags['zero_flag'] = (self.registers[rd] == self.registers[rs])
            self.PC += self.instruction_size

        elif opcode == 0x40:  # AND Rd, Rs
            rd = op1
            rs = op2
            value = self.registers[rd] & self.registers[rs]
            self.registers[rd] = value & 0xFFFF
            self.flags['zero_flag'] = (self.registers[rd] == 0)
            self.PC += self.instruction_size

        elif opcode == 0x41:  # NOT Rd
            rd = op1
            value = ~self.registers[rd] & 0xFFFF
            self.registers[rd] = value
            self.flags['zero_flag'] = (self.registers[rd] == 0)
            self.PC += self.instruction_size

        elif opcode == 0x42:  # OR Rd, Rs
            rd = op1
            rs = op2
            value = self.registers[rd] | self.registers[rs]
            self.registers[rd] = value & 0xFFFF
            self.flags['zero_flag'] = (self.registers[rd] == 0)
            self.PC += self.instruction_size

        elif opcode == 0x43:  # XOR Rd, Rs
            rd = op1
            rs = op2
            value = self.registers[rd] ^ self.registers[rs]
            self.registers[rd] = value & 0xFFFF
            self.flags['zero_flag'] = (self.registers[rd] == 0)
            self.PC += self.instruction_size

        elif opcode == 0x44:  # SHL Rd, Imm4
            rd = op1
            shift_amount = op2 & 0x0F  # only lower 4 bits used for shift amount
            value = (self.registers[rd] << shift_amount) & 0xFFFF
            self.registers[rd] = value
            self.flags['zero_flag'] = (value == 0)
            self.PC += self.instruction_size

        elif opcode == 0x45:  # SHR Rd, Imm4
            rd = op1
            shift_amount = op2 & 0x0F  # only lower 4 bits used for shift amount
            value = self.registers[rd] >> shift_amount
            self.registers[rd] = value
            self.flags['zero_flag'] = (value == 0)
            self.PC += self.instruction_size

        elif opcode == 0xFF:  # NOP
            # Luigi wins by doing absolutely nothing.
            self.PC += self.instruction_size

        elif opcode == 0xF0:  # CLZ (Clear zero flag)
            self.flags['zero_flag'] = False
            self.PC += self.instruction_size

        else:
            raise Exception(f"Unknown opcode {opcode:#02x} at PC {self.PC}")

    def run(self):
        print("SOLAR-16 Emulator")
        print("Developed by Arslaan Pathan")
        last_time = time.perf_counter()

        print("\nInstruction memory:")
        print(self.instruction_memory.hex())
        print()

        while not self.halted:
            instr_bytes = self.fetch()
            opcode, op1, op2, op3 = self.decode(instr_bytes)
            self.execute(opcode, op1, op2, op3)

            # throttle to maintain ~20 MHz speed
            elapsed = time.perf_counter() - last_time
            if elapsed < self.cycle_duration:
                time.sleep(self.cycle_duration - elapsed)
            last_time = time.perf_counter()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 emulator.py <input_file.bin>", file=sys.stderr)
        sys.exit()

    try:
        with open(sys.argv[1], 'rb') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error! File {sys.argv[1]} not found.")
        sys.exit()

    solar16 = SOLAR16(code)
    solar16.run()
