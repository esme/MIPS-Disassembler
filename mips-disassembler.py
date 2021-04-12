import math
import collections
  
def invertBits(num):  
    x = int(math.log2(num)) + 1
  
    for i in range(x):  
        num = (num ^ (1 << i))

    return num

def hexFormat(address):
  return str(hex(address))[2:].upper()

# FUNC for R-format instruction where OPCODE is 0
funcs = {32:"add", 34:"sub", 36:"and", 37:"or", 42:"slt"}

# OPCODE for I-format instruction
opcodes = {4:"beq", 5:"bne", 35:"lw", 43:"sw"}

# & bitmask with instruction to get specific bits
bitmasks = {
  "src1":0b00000011111000000000000000000000,
  "src2":0b00000000000111110000000000000000,
  "dest":0b00000000000000001111100000000000,
  "func":0b00000000000000000000000000111111,
  "offset":0b00000000000000001111111111111111
}

address = 0x9A040

def disassemble(instruction):
  global address
  opcode = 0
  src1 = 0
  src2 = 0
  dest = 0
  func = 0

  current_address = address
  # increment address by 4
  address += 4

  opcode = instruction >> 32 - 6
  src1 = (instruction & bitmasks['src1']) >> 6 + 5 + 5 + 5
  src2 = (instruction & bitmasks['src2']) >> 6 + 5 + 5

  # R-format instruction
  if opcode == 0:
    dest = (instruction & bitmasks['dest']) >> 6 + 5
    func = instruction & bitmasks['func']
    return f'{hexFormat(current_address)} {funcs[func]} ${dest}, ${src1}, ${src2}'

  offset = 0

  # I-format instruction
  if opcode in opcodes:
    offset = instruction & bitmasks['offset']
    # check if leftmost digit is 1 for negative number
    if offset >> 15 == 1:
      # one's complement
      ones_complement = invertBits(offset)
      # two's complement
      twos_complement = ones_complement + 1
      offset = -twos_complement

    # for sw or lw
    if opcodes[opcode] == 'sw' or opcodes[opcode] == 'lw':
      return f'{hexFormat(current_address)} {opcodes[opcode]} ${src2}, {offset}(${src1})'

    # for beq or bne
    if opcodes[opcode] == 'beq' or opcodes[opcode] == 'bne':
      # next address is incremented address + offset shifted left by 2 positions
      next_address = address + (offset << 2)
      return f'{hexFormat(current_address)} {opcodes[opcode]} ${src1}, ${src2} address {hexFormat(next_address)}'


  return 'invalid opcode'

instructions = [0x032BA020, 0x8CE90014, 0x12A90003, 0x022DA822, 0xADB30020, 0x02697824, 0xAE8FFFF4, 0x018C6020, 0x02A4A825, 0x158FFFF7, 0x8ECDFFF0]
for instruction in instructions:
  print(disassemble(instruction))
