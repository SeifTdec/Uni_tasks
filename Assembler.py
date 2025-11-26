Opcode_table={
    "AND":0x0,
    "ADD":0x1,
    "LDA":0x2,
    "STA":0x3,
    "BUN":0x4,
    "BSA":0x5,
    "ISZ":0x6,
    "CLA":0x7800,
    "CLE":0x7400,
    "CMA":0x7200,
    "CME":0x7100,
    "CIR":0x7080,
    "CIL":0x7040,
    "INC":0x7020,
    "SPA":0x7010,
    "SNA":0x7008,
    "SZA":0x7004,
    "SZE":0x7002,
    "HLT":0x7001,
    "INP":0xF800,
    "OUT":0xF400,
    "SKI":0xF200,
    "SKO":0xF100,
    "ION":0xF080,
    "IOF":0xF040
}

program = ["ORG 300","LDA A","STA TEMP","LDA B","STA A","LDA TEMP","STA B","HLT","A, DEC 7","B, DEC 12","TEMP, HEX 0", "END" ]
class two_step_assembler:
    def __init__(self,program):
        self.ToExecute=program
        self.symbol_table={}
        self.binary_code=[]

    def first_pass(self):
        location_counter=0
        for line in self.ToExecute:
            symbol_precomma=line.find(",")
            if line.split()[0]=="ORG":
                location_counter=int(line.split()[1],16)
            elif line.split()[0]=="END":
                break
            else:
                if symbol_precomma!=-1:
                    symbol=line[:symbol_precomma]
                    self.symbol_table[symbol]=location_counter
                
                location_counter+=1
    def second_pass(self):
        location_counter=0
        for line in self.ToExecute:
            line_part=line.split()
            if line_part[0]=="ORG":
                location_counter=int(line_part[1],16)
            elif line.split()[0]=="END":
                break
            else:
                is_indirect = False
                
                if line_part[0] in Opcode_table:
                    instruction=line_part[0]
                    operand=line_part[1] if len(line_part)>1 else None
                
                    if len(line_part) > 2 and line_part[2] == "I":
                        is_indirect = True
                else:
                    instruction=line_part[1]
                    operand=line_part[2] if len(line_part)>2 else None

                    if len(line_part) > 3 and line_part[3] == "I":
                        is_indirect = True

                if instruction in Opcode_table:
                    if operand is not None:
                        machine_code=(Opcode_table[instruction]<<12)| (self.symbol_table[operand] & 0xFFF)
                        if is_indirect:
                            machine_code |= 0x8000
                        self.binary_code.append((location_counter,machine_code))
                    else:
                        machine_code=Opcode_table[instruction]
                        self.binary_code.append((location_counter,machine_code))
                    location_counter+=1
                
                elif instruction=="DEC":
                    value=int(operand)
                    if value<0:
                        value&=0xFFFF
                    self.binary_code.append((location_counter,value))
                    location_counter+=1
                elif instruction =="HEX":
                    value=int(operand,16)
                   k self.binary_code.append((location_counter,value))
                    location_counter+=1

if __name__=="__main__":
    assembler=two_step_assembler(program)
    assembler.first_pass()
    print("Symbol Table:")
    for symbol in assembler.symbol_table:
        print(f"{symbol}: {assembler.symbol_table[symbol]:03X}")
    assembler.second_pass()
    print("\nBinary Code:")
    for address,code in assembler.binary_code:
        print(f"{address:03X}: {code:016b}")
