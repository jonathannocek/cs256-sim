#
# S20_SIM.py  --  Simulator class for the SIM CPU designed by CS256-S20.
#
from utils import print_val, print_mem, print_input, print_matrix
import random

# Constants for this architecture
_NUMREG = 8       # number of registers in the register file
_REGSIZE = 8      # size (in bits) of each register)
_ADDRSIZE = _REGSIZE  # size (in bits) of DMEM addresses
_NUMBUTTONS = 4   # Number of buttons (binary on/off) for input
_MATRIXSIZE = 10  # width and height of the pixel matrix output

_OPCODES = {
    "0": "R-format",
    "1": "ADDI",
    "2": "ASSIGNI",
    "3": "BEQ",
    "4": "BNE",
    "5": "RAND"
}

_FUNCTIONCODES = {
    "0": "ADD",
    "1": "SUB",
    "2": "LOAD",
    "3": "STORE",
    "4": "IN",
    "5": "OUT",
    "6": "SGT"
}

class Simulator:

    def __init__(self):
        # CPU state:
        self.imem = [0]  # not affected by CPU reset, so only initialized here
        self.reset()

        # Simulator state (separate from the CPU itself):
        self.bin_filename = ""

    def load_bin(self, filename):
        # Load machine code from a file into instruction memory
        self.bin_filename = filename
        print(bin_filename)
        with open(filename, 'r') as f:
            data = f.read()
        words = data.split()
        self.imem = [int(word, 16) for word in words]

        # Always reset on loading new code
        self.reset()

    def change_buttons(self, new_buttons):
        # Change the state of the simulated buttons
        # Parameter: new_buttons is a string, containing a 0 or 1 for each button
        #            e.g. "0110" for the first button not pressed, the second and
        #            third pressed, and the fourth not pressed.
        buttons = [int(c) for c in new_buttons]
        if len(buttons) != _NUMBUTTONS:
            raise Exception(f"Incorrect number of buttons.  Got {len(buttons)}, expected {_NUMBUTTONS}.")
        if max(buttons) > 1 or min(self.buttons) < 0:
            raise Exception(f"Invalid value for button.  Only allowed values are 0 and 1.")
        self.buttons = buttons

    def step_n(self, n):
        # Simulate n cycles of the CPU (see self.step()).
        for _ in range(n):
            self.step()

    def step(self):
        # Simulate *one* cycle of the CPU (Fetch-Decode-Execute)
        # Basic outline:
        #  1) Fetch the current instruction (using imem and PC)
        #  2) Decode the instruction into its different fields
        #  3) Execute the instruction by updating the CPU state
        #     according to what the execution of that instruction
        #     would do.
        word = self.fetch()
        op, r1, r2, imm, func = self.decode(word)
        if (op == 0):
            self.execute_r_type(op, r1, r2, func)
        if (op == 1):
            self.execute_i_type(op, r1, imm)

    def reset(self):
        # Reset the CPU state to just-powered-on, with everything but IMEM cleared
        self.PC = 0
        self.regfile = [0] * _NUMREG
        self.dmem = [0] * 2**_ADDRSIZE
        self.buttons = [0] * _NUMBUTTONS
        self.matrix = [([0] * _MATRIXSIZE) for _ in range(_MATRIXSIZE)]

    def print(self):
        # Print the current state of all state (memory) elements of the CPU
        print_val(self.PC, "PC")
        print_mem(self.imem, "IMEM", val_width=16)
        print_mem(self.regfile, "Regfile", label_all=True)
        print_mem(self.dmem, "DMEM")
        print_input(self.buttons, "Input")
        print_matrix(self.matrix, "Output")
    
    def fetch(self):
        word = self.imem[self.PC]
        self.PC += 1
        print(word)
        return(word)

    def decode(self, word):
        # Convert from hex to bin
        binary = SimulatorHelper._hex_to_binary(word)
        #need to get word from fetch this is just a placeholder
        word = 0b0001110110000001
        # decode word into fields 
        opcodeMask = (0b111 << 13)
        opcode = (word & opcodeMask) >> 13
        #if opcode is 1 then the instruction is R-type and we need to get the registers and func code
        if (opcode == 0):
            r1Mask = (0b111 << 10)
            r1 = (word & r1Mask) >> 10

            r2Mask = (0b111 << 7)
            r2 = (word & r2Mask) >> 7

            funcMask = (0b1111111) 
            funcCode = (word & funcMask)

        #if opcode is anything else then the instruction is I-type and we need a register and an immediate and the opcode will dictate the exact instruction
        else:
            r1Mask = (0b111 << 10)
            r1 = (word & r1Mask) >> 10

            immediateMask = (0b1111111111)
            immediate = (word & immediateMask)


        pass

    def execute(self):
        pass

class Instructions(Simulator):
    def _add(self, r1, r2):
        '''
        r1 = r1 + r2
        R-format
        '''
        self.regfile[r1] += self.regfile[r2]

    def _addi(self, r1, imm):
        '''
        r1 = r1 + imm
        I-format
        '''
        self.regfile[r1] += imm

    def _assigni(self, r1, imm):
        '''
        r1 = imm
        I-format
        '''
        self.regfile[r1] = imm

    def _sub(self, r1, r2):
        '''
        r1 = r1 - r2
        R-format
        '''
        self.regfile[r1] -= self.regfile[r2]

    def _load(self, r1, r2):
        '''
        r1 = Mem[r2]
        R-format
        '''
        self.regfile[r1] = self.dmem[r2]

    def _store(self, r1, r2):
        '''
        Mem[r2] = r1
        R-format
        '''
        self.dmem[r2] = self.regfile[r1]

    def _beq(self, r1, label):
        '''
        If (r1 == $7) goto label [implicitly, $7 is always used in the comparison]
        I-format
        '''
        if (regfile[r1] == regfile[7]):
            self.pc = label
        else:
            pass

    def _bne(self, r1, label):
        '''        
        If (r1 != $7) goto label [implicitly, $7 is always used in the comparison]
        I-format
        '''
        if (regfile[r1] != regfile[7]):
            self.pc = label
        else:
            pass

    def _sgt(self, r1, r2):
        '''
        $7 = (r1 > r2) ? 1 : 0 [implicitly, $7 is always used in the comparison]
        R-format
        '''
        if (regfile[r1] > regfile[r2]):
            regfile[7] = 1
        else:
            regfile[7] = 0

    def _in(self, r1, r2):
        '''
        r1 = IO[r2]
        R-format
        '''
        self.regfile[r1] = self.buttons[r2]

    def _out(self, r1, r2):
        '''
        IO[r2] = r1
        R-format
        ''' 
        self.button[r2] = regfile[r1]
        
    def _rand(self, r1, r2):
        '''
        r1 = [randvalue] & imm    [randvalue is a random 8-bit value]
        I-format
        '''
        randvalue = random.randint(0, 63)
        binaryRand = SimulatorHelper._dec_to_binary(randvalue)
        regfile[r1] = binaryRand & imm

class SimulatorHelper(Simulator):
    def _hex_to_binary(hex_string):
        '''
        Convert hexadecimal to binary
        '''
        binary = bin(int(hex_string, 16))
        binary = binary[2:].zfill(16)
        return(binary)
    
    def _binary_to_hex(self, binary_string):
        '''
        Convert binary to hexadecimal
        '''
        hexadecimal = hex(int(binary_string, 2))
        return(hexadecimal)
    
    def _binary_to_dec(self, binary_string):
        dec = int(binary_string, 2)
        return(dec)

    def _dec_to_binary(self, dec_string):
        binary = bin(int(dec_string, 10))
        binary = binary[2:].zfill(16)
        return(binary)

# Main function for testing
if __name__ == '__main__':
    sim = Simulator()
    sim.step()    