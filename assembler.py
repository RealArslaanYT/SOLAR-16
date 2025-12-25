# SOLAR-16 - A custom CPU architecture/ISA
# assembler.py
# (C) Copyright 2025  Arslaan Pathan
import re
import sys

opcode_map = {
    'ADD': 0x00,
    'SUB': 0x01,
    'MUL': 0x02,
    'RADD': 0x03,
    'RSUB': 0x04,
    'RMUL': 0x05,
    'MOV': 0x10,
    'LD': 0x11,
    'ST': 0x12,
    'CLR': 0x13,
    'JMP': 0x20,
    'JZ': 0x21,
    'JNZ': 0x22,
    'HALT': 0x23,
    'CMP': 0x30,
    'AND': 0x40,
    'NOT': 0x41,
    'OR': 0x42,
    'XOR': 0x43,
    'SHL': 0x44,
    'SHR': 0x45,
    'NOP': 0xFF,
    'CLZ': 0xF0,
}

instruction_size = 4  # Each instruction is 4 bytes

def parse_register(reg_str):
    match = re.match(r'R(\d+)', reg_str.strip().upper())
    if match:
        reg_num = int(match.group(1))
        if 0 <= reg_num <= 15:
            return reg_num
    raise ValueError(f'Invalid register {reg_str}')

def first_pass(lines):
    labels = {}
    address = 0

    for line in lines:
        line = line.strip()
        if not line or line.startswith(';'):
            continue
        if ':' in line:
            label, rest = line.split(':', 1)
            labels[label.strip()] = address
            line = rest.strip()
            if not line:
                continue  # Label only line
        address += instruction_size
    return labels

def assemble_line(line, labels):
    line = line.strip()
    if not line or line.startswith(';'):
        return None

    # Remove label if present
    if ':' in line:
        _, line = line.split(':', 1)
        line = line.strip()
        if not line:
            return None

    parts = re.split(r'[ ,]+', line)
    mnemonic = parts[0].upper()

    if mnemonic not in opcode_map:
        raise ValueError(f'Unknown instruction {mnemonic}')

    opcode = opcode_map[mnemonic]
    b = [opcode, 0, 0, 0]

    def resolve(val):
        return labels[val] if val in labels else int(val, 0)

    if mnemonic in ['ADD', 'SUB', 'MUL']:
        rd = parse_register(parts[1])
        imm = resolve(parts[2])
        b[1] = rd
        b[2] = imm & 0xFF
        b[3] = (imm >> 8) & 0xFF

    elif mnemonic in ['RADD', 'RSUB', 'RMUL']:
        rd = parse_register(parts[1])
        rs = parse_register(parts[2])
        b[1] = rd
        b[2] = rs

    elif mnemonic == 'MOV':
        rd = parse_register(parts[1])
        rs = parse_register(parts[2])
        b[1] = rd
        b[2] = rs

    elif mnemonic in ['LD', 'ST']:
        reg = parse_register(parts[1])
        addr = resolve(parts[2])
        b[1] = reg
        b[2] = addr & 0xFF
        b[3] = (addr >> 8) & 0xFF

    elif mnemonic in ['JMP', 'JZ', 'JNZ']:
        addr = resolve(parts[-1])
        b[1] = 0
        b[2] = addr & 0xFF
        b[3] = (addr >> 8) & 0xFF

    elif mnemonic == 'HALT':
        pass

    elif mnemonic == 'CMP':
        rd = parse_register(parts[1])
        rs = parse_register(parts[2])
        b[1] = rd
        b[2] = rs

    elif mnemonic in ['AND', 'OR', 'XOR']:
        rd = parse_register(parts[1])
        rs = parse_register(parts[2])
        b[1] = rd
        b[2] = rs

    elif mnemonic in ['NOT', 'CLR']:
        rd = parse_register(parts[1])
        b[1] = rd

    elif mnemonic in ['SHL', 'SHR']:
        rd = parse_register(parts[1])
        imm = resolve(parts[2]) & 0x0F
        b[1] = rd
        b[2] = imm

    elif mnemonic in ['NOP', 'CLZ']:
        pass

    else:
        raise ValueError(f'Assembler: Unhandled instruction {mnemonic}')

    return bytes(b)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 assembler.py <input.asm> <output.bin>")
        sys.exit(1)

    try:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error! Input file {sys.argv[1]} not found.")
        sys.exit(1)

    # Pass 1: collect labels
    labels = first_pass(lines)

    # Pass 2: assemble instructions
    with open(sys.argv[2], 'wb') as f:
        for line in lines:
            machine_code = assemble_line(line, labels)
            if machine_code:
                print(machine_code.hex())
                f.write(machine_code)
