class MIPSAssembler:

    def __init__(self):
        self.data_memory = ['\0'] * 1024
        self.instruction_memory = []
        self.labels={}
    def load_program(self, program):
        i=1048576 # 4194304/4
        data_address=0
        lines=program.split('\n')

        for line in lines:
            line = line.strip()

        # Ignoring comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            if line.startswith('.data'):
                continue

            if line.startswith('.text'):
                continue

            elif ":" in line:
                parts = line.split(":")
                if len(parts) == 2:
                    label, instruction = parts
                    
                instruction=instruction.strip()
                label=label.strip()
                if instruction.startswith('.asciiz'):
                     self.labels[label] = data_address
                    #  print(f"label is {label} address is {data_address}")
                     string_value = instruction[instruction.index('"') +1 : instruction.rindex('"')]
                     self.data_memory[data_address:data_address + len(string_value)] = list(string_value)
                     data_address += len(string_value)+1
                     if(string_value==r'\n'):
                        data_address=data_address-1
                    #  print(string_value)
                    #  print(f"string length is {len(string_value)}")
                else:    
                    self.labels[label]=i
                    # print(instruction)
                    self.instruction_memory.append(instruction)
                    # print(f"label is {label}  i is {i*4} ")
                    i=i+1
            
            elif line[0:2]=='la':
                opcode,operands=line.split()
                register_dest,label_1=operands.split(",")
                instruction1="lui $at,4097"
                instruction2="ori"
                instruction2+=" "+register_dest+",$at,"
                instruction2+=str(self.labels[label_1])
                # lui $1,4097
                # ori $4,$1,2
                # print(instruction1)
                self.instruction_memory.append(instruction1)
                i=i+1
                # print(instruction2)
                self.instruction_memory.append(instruction2)
                i=i+1

            else:
                # print(line)
                self.instruction_memory.append(line)
                i=i+1

    def assemble_program(self):
        machine_code = []

    # Assembling instructions from the instruction memory
        for j in range(0, len(self.instruction_memory)):
            instruction = self.instruction_memory[j].strip()

            if(instruction==""):
                continue

            if instruction.startswith('syscall'):
                opcode = 'syscall'
                operands = ''
                opcode = opcode_mapping.get(opcode)
                opcode = 26 * "0" + opcode
                machine_instruction = opcode

            else:
                opcode, operands = instruction.split()
                opcode_code = opcode_mapping.get(opcode)
                machine_instruction = opcode_code


                if opcode =='add' or opcode=='sub' or opcode=='mul' or opcode=='slt':#case for add,sub,mul and slt instructions
                    register_dest, register_src1, register_src2 = operands.split(",")
                    register_dest = register_mapping.get(register_dest)
                    register_src1 = register_mapping.get(register_src1)   
                    register_src2 = register_mapping.get(register_src2) 
                    machine_instruction += register_src1
                    machine_instruction += register_src2
                    machine_instruction += register_dest
                    machine_instruction += '00000' 
                    if opcode == 'add':
                        funct = '100000' 
                    elif opcode == 'sub':
                        funct='100010'
                    elif opcode=='mul':
                        funct='000010'    
                    elif opcode=='slt':
                        funct='101010'
                    machine_instruction += funct

                elif opcode=='move':#case for move instruction
                    register_dest,register_src2 = operands.split(",")
                    register_dest = register_mapping.get(register_dest)
                    register_src1 = register_mapping.get('$0')   
                    register_src2 = register_mapping.get(register_src2) 
                    machine_instruction += register_src1
                    machine_instruction += register_src2
                    machine_instruction += register_dest
                    machine_instruction += '00000' 
                    funct= '100001'
                    machine_instruction += funct

                elif opcode=='jr':#case for jr instruction
                    register_src1=operands
                    register_dest = register_mapping.get('$0')
                    register_src2 = register_mapping.get('$0')
                    register_src1 = register_mapping.get(register_src1)   
                    machine_instruction += register_src1
                    machine_instruction += register_src2
                    machine_instruction += register_dest
                    machine_instruction += '00000' 
                    funct= '001000'
                    machine_instruction += funct

                elif opcode == 'lw' or opcode == 'sw':#case for lw or sw instruction
                    register_first, location = operands.split(",")
                    register_first = register_mapping.get(register_first)
                    
                    offset, register_base = location.split('(')
                    register_base = register_base[0:len(register_base) - 1]
                    register_base = register_mapping.get(register_base)
                    machine_instruction += register_base
                    
                    machine_instruction += register_first
                    offset = int(offset)  
                    offset = format(offset, '016b')
                    machine_instruction += offset

                elif opcode == 'addi' or opcode=='ori':#case for addi or ori instruction
                    register_dest, register_src, immediate = operands.split(",")
                    register_dest = register_mapping.get(register_dest)
                    register_src = register_mapping.get(register_src)   

                    machine_instruction += register_src
                    machine_instruction += register_dest
                    immediate = int(immediate)  
                    if immediate<0 :
                        immediate=bin(immediate % (1<<16))
                        immediate=immediate[2:]
                    else:    
                        immediate = format(immediate, '016b')
                    machine_instruction += immediate

                elif opcode == 'beq':#case for beq instruction
                    register1, register2, label = operands.split(",")
                    register1 = register_mapping.get(register1)
                    if(register2.isdigit()):
                        register2 = register_mapping.get('$at')
                    else:
                        register2 = register_mapping.get(register2)
                    machine_instruction += register1
                    machine_instruction += register2
                    label = self.labels[label]
                    beq_instruction_address = self.instruction_memory.index(instruction)
                    beq_instruction_address=beq_instruction_address+1048576
                    label = label - beq_instruction_address - 1
                    label = format(label, '016b')
                    machine_instruction += label

                elif opcode == 'li' or opcode =="lui":#case for li or lui instruction
                    register_dest, immediate = operands.split(",")
                    register_dest = register_mapping.get(register_dest)
                    register_src = register_mapping.get('$0')   
                    machine_instruction += register_src
                    machine_instruction += register_dest

                    immediate = int(immediate)  
                    if immediate<0 :
                        immediate=bin(immediate % (1<<16))
                        immediate=immediate[2:]
                    else:
                        immediate = format(immediate, '016b')
                    machine_instruction += immediate
                    

                elif opcode =='la':#case for la instruction
                    register_dest,label=operands.split(",")
                    register_dest = register_mapping.get(register_dest)
                    machine_instruction += register_dest
                    register_src = register_mapping.get('$0')   
                    machine_instruction += register_src
                    immediate=4097
                    immediate = format(immediate, '016b')
                    machine_instruction += immediate

                elif opcode == 'j' or opcode == 'jal':#case for jal or j instruction
                    label = operands
                    label=label.strip()
                    
                    label = self.labels[label]
                    label = format(label, '026b')
                    machine_instruction += label

            machine_code.append(machine_instruction)#appending new code to the machine code

        return machine_code#returning the machine code

    

# Opcode mapping for the instructions
opcode_mapping = {
    'addi': '001000',
    'lw': '100011',
    'sw': '101011',
    'beq': '000100',
    'add': '000000',
    'sub': '000000',
    'move':'000000',
    'slt':'000000',
    'jr':'000000',
    'j': '000010',  
    'move': '000000',  
    'syscall' : '001100',
    'li': '001001',
    'jal': '000011',
    'la': '001111',
    'mul':'011100',
    'lui':'001111',
    'ori':'001101',
    
}

# register mapping for the instructions
register_mapping = {
    '$0': '00000', '$zero': '00000',
    '$at': '00001',
    '$v0': '00010', '$v1': '00011',
    '$a0': '00100', '$a1': '00101', '$a2': '00110', '$a3': '00111',
    '$t0': '01000', '$t1': '01001', '$t2': '01010', '$t3': '01011',
    '$t4': '01100', '$t5': '01101', '$t6': '01110', '$t7': '01111',
    '$s0': '10000', '$s1': '10001', '$s2': '10010', '$s3': '10011',
    '$s4': '10100', '$s5': '10101', '$s6': '10110', '$s7': '10111',
    '$t8': '11000', '$t9': '11001',
    '$k0': '11010', '$k1': '11011',
    '$gp': '11100', '$sp': '11101', '$fp': '11110', '$ra': '11111',
}


with open('final_mips.asm', 'r') as file:#reading the input file(mips code)
    mips_code = file.read()

assembler = MIPSAssembler()#creating an instance of the MIPSAssembler class


assembler.load_program(mips_code)
machine_code=assembler.assemble_program()

for instructions in machine_code:#printing the output
    hexa=int(instructions, 2)
    hexa=format(hexa,'08x')
    # print(instructions)
    print('0x'+hexa)
