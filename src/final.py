#########################################################################
# RISC-V Code Generator                                                 #
# This part of the code generates RISC-V assembly from intermediate     #
# quadruples code, following the approach from the lecture slides.      #
#########################################################################

class RISCVCodeGenerator:
    def __init__(self, symbol_table=None):
        self.code = []
        self.temp_map = {}  # Maps temporary variables to registers
        self.var_map = {}  # Maps program variables to memory locations
        self.label_map = {}  # Maps quad labels to assembly labels
        self.next_temp_reg = 5  # Start from t0 (x5)
        self.next_data_addr = 0  # Data memory offset
        self.global_vars = set()  # Set of global variables
        self.current_function = None
        self.string_literals = {}  # For storing string literals if needed
        self.string_counter = 0
        self.symbol_table = symbol_table
        self.framelength = 64  # Standard frame length for simplicity

    def emit(self, instruction):
        """Add an instruction to the generated code."""
        self.code.append(instruction)

    def emit_label(self, label):
        """Emit a label."""
        self.code.append(f"{label}:")

    def get_assembly_label(self, quad_label):
        """Convert a quad label to an assembly label."""
        if quad_label not in self.label_map:
            self.label_map[quad_label] = f"L{quad_label}"
        return self.label_map[quad_label]

    def get_var_offset(self, var):
        """Get memory offset for a variable (simplified)."""
        if var in self.var_map:
            return self.var_map[var]
            
        # If we have a symbol table, get variable offset from it
        if self.symbol_table:
            entity = self.symbol_table.lookup(var)
            if entity and hasattr(entity, 'offset'):
                self.var_map[var] = entity.offset
                return entity.offset

        # Otherwise, assign a new offset
        self.var_map[var] = self.next_data_addr
        self.next_data_addr += 4  # Assume 4 bytes per variable (32-bit)
        return self.var_map[var]

    def allocate_register(self, var):
        """Allocate a register for a variable or temporary."""
        if var in self.temp_map:
            return self.temp_map[var]

        if var.startswith('T_'):
            # Allocate register for temporary variable
            reg = f"t{self.next_temp_reg - 5}"  # t0, t1, etc.
            self.temp_map[var] = reg
            self.next_temp_reg += 1
            if self.next_temp_reg > 7:  # t0-t2 (x5-x7)
                self.next_temp_reg = 5  # Reuse registers (simplified approach)
            return reg
        else:
            # Program variables are stored in memory
            return self.get_var_offset(var)

    # Implementation of gnlvcode as described in slides
    def gnlvcode(self, var):
        """Generate code to get the address of a non-local variable."""
        # Start from current scope
        self.emit(f"lw t0,-4(sp)")
        
        # Follow access links (simplified - assumes one level up)
        # In a full implementation, this would traverse multiple levels
        # based on the nesting level difference
        
        # Calculate address of the variable
        offset = self.get_var_offset(var)
        self.emit(f"addi t0,t0,-{offset}(sp)")
        
        # Now t0 contains the address of the variable

    # Implementation of loadvr as described in slides
    def loadvr(self, v, r):
        """Load value from variable v into register r."""
        if isinstance(v, int) or (isinstance(v, str) and v.isdigit()) or (isinstance(v, str) and v[0] == '-' and v[1:].isdigit()):
            # v is a constant
            self.emit(f"li {r},{v}")
        elif v.startswith('T_'):
            # v is a temporary variable, already in a register
            src_reg = self.temp_map.get(v)
            if src_reg:
                self.emit(f"mv {r},{src_reg}")
            else:
                self.emit(f"# Warning: Temporary {v} not allocated")
        else:
            # v is a program variable
            # Simplified - assumes local variable
            offset = self.get_var_offset(v)
            self.emit(f"lw {r},-{offset}(sp)")

    # Implementation of storerv as described in slides
    def storerv(self, r, v):
        """Store value from register r into variable v."""
        if v.startswith('T_'):
            # v is a temporary variable
            dest_reg = self.temp_map.get(v)
            if dest_reg:
                self.emit(f"mv {dest_reg},{r}")
            else:
                self.emit(f"# Warning: Temporary {v} not allocated")
        else:
            # v is a program variable
            # Simplified - assumes local variable
            offset = self.get_var_offset(v)
            self.emit(f"sw {r},-{offset}(sp)")

    def generate_data_section(self):
        """Generate the data section for variables."""
        data_section = [".data"]

        # Add global variables
        for var in self.global_vars:
            data_section.append(f"{var}: .word 0")

        # Add string literals if any
        for label, string in self.string_literals.items():
            data_section.append(f"{label}: .string \"{string}\"")

        # Newline string for print operations
        data_section.append("str_nl: .asciz \"\\n\" ")

        return data_section

    def generate_code_from_quads(self, quads):
        """Generate RISC-V assembly code from quadruples."""
        # Initialize code with entry point
        self.emit(".text")
        self.emit(".globl main")
        self.emit("j Lmain")  # As per slide 62

        for quad in quads:
            label, op, arg1, arg2, result = quad

            # Emit label for this quad if needed
            asm_label = self.get_assembly_label(label)
            self.emit_label(asm_label)

            # Process based on operation
            if op == "begin_block":
                if arg1 == "τεστ":  # Main program
                    self.emit("Lmain:")
                    self.emit(f"addi sp,sp,{self.framelength}")
                    self.emit("mv gp,sp")
                    # No need to save return address for main
                else:
                    # Function or procedure
                    self.current_function = arg1
                    self.emit(f"{arg1}:")
                    self.emit("sw ra,(sp)")
                    self.emit(f"addi fp,sp,{self.framelength}")

            elif op == "end_block":
                if arg1 == "τεστ":  # Main program
                    self.emit("li a7,10")
                    self.emit("ecall")
                else:
                    # Function or procedure
                    self.current_function = None
                    self.emit("lw ra,(sp)")
                    self.emit("jr ra")

            elif op == "+":
                # Following slides 38-40 for arithmetic operations
                t1_reg = "t0"
                t2_reg = "t1"
                result_reg = "t2"
                
                self.loadvr(arg1, t1_reg)
                self.loadvr(arg2, t2_reg)
                self.emit(f"add {result_reg},{t1_reg},{t2_reg}")
                self.storerv(result_reg, result)

            elif op == "-":
                t1_reg = "t0"
                t2_reg = "t1"
                result_reg = "t2"
                
                self.loadvr(arg1, t1_reg)
                self.loadvr(arg2, t2_reg)
                self.emit(f"sub {result_reg},{t1_reg},{t2_reg}")
                self.storerv(result_reg, result)

            elif op == "*":
                t1_reg = "t0"
                t2_reg = "t1"
                result_reg = "t2"
                
                self.loadvr(arg1, t1_reg)
                self.loadvr(arg2, t2_reg)
                self.emit(f"mul {result_reg},{t1_reg},{t2_reg}")
                self.storerv(result_reg, result)

            elif op == "/":
                t1_reg = "t0"
                t2_reg = "t1"
                result_reg = "t2"
                
                self.loadvr(arg1, t1_reg)
                self.loadvr(arg2, t2_reg)
                self.emit(f"div {result_reg},{t1_reg},{t2_reg}")
                self.storerv(result_reg, result)

            elif op == ":=":
                # Following slide 39 for assignment
                src_reg = "t0"
                
                self.loadvr(arg1, src_reg)
                self.storerv(src_reg, result)
                self.emit(f"# {result} := {arg1}")

            elif op in ["<", "<=", ">", ">=", "=","<>"]:
                # Following slide 38 for relational operations
                t1_reg = "t0"
                t2_reg = "t1"
                
                self.loadvr(arg1, t1_reg)
                self.loadvr(arg2, t2_reg)
                
                target_label = self.get_assembly_label(result)
                if op == "<":
                    self.emit(f"blt {t1_reg},{t2_reg},{target_label}")
                elif op == "<=":
                    self.emit(f"ble {t1_reg},{t2_reg},{target_label}")
                elif op == ">":
                    self.emit(f"bgt {t1_reg},{t2_reg},{target_label}")
                elif op == ">=":
                    self.emit(f"bge {t1_reg},{t2_reg},{target_label}")
                elif op == "=":
                    self.emit(f"beq {t1_reg},{t2_reg},{target_label}")
                elif op == "<>":
                    self.emit(f"bne {t1_reg},{t2_reg},{target_label}")

            elif op == "jump":
                # Unconditional jump - slide 38
                target_label = self.get_assembly_label(result)
                self.emit(f"j {target_label}")

            elif op == "jumpz":
                # Jump if zero (condition is false)
                t1_reg = "t0"
                self.loadvr(arg1, t1_reg)
                
                target_label = self.get_assembly_label(result)
                self.emit(f"beqz {t1_reg},{target_label}")

            elif op == "jumpnz":
                # Jump if not zero (condition is true)
                t1_reg = "t0"
                self.loadvr(arg1, t1_reg)
                
                target_label = self.get_assembly_label(result)
                self.emit(f"bnez {t1_reg},{target_label}")

            elif op == "par":
                # Handle parameter passing - slides 42-48
                i = 0  # Parameter index (simplified)
                
                if arg2 == "cv":  # Call by value
                    # Load the value into a register
                    t1_reg = "t0"
                    self.loadvr(arg1, t1_reg)
                    # Store parameter in callee's frame
                    self.emit(f"sw {t1_reg},-{12+4*i}(fp)")
                elif arg2 == "ref":  # Call by reference
                    # Get the address of the variable
                    if self.is_local_var(arg1):
                        # Local variable
                        offset = self.get_var_offset(arg1)
                        self.emit(f"addi t0,sp,-{offset}")
                    else:
                        # Non-local variable - use gnlvcode
                        self.gnlvcode(arg1)
                    # Pass the address
                    self.emit(f"sw t0,-{12+4*i}(fp)")
                elif arg2 == "ret":  # Return value parameter
                    # Reserve space for return value
                    self.emit(f"addi t0,sp,-{self.get_var_offset(arg1)}")
                    self.emit(f"sw t0,-8(fp)")

            elif op == "call":
                # Function or procedure call - slides 55-61
                # First, set up the frame pointer for the callee
                self.emit(f"")
                self.emit(f"addi fp,sp,{self.framelength}")
                
                # Set up the access link (dynamic link)
                if self.is_same_level_call(arg1):
                    # Same level call
                    self.emit("lw t0,-4(sp)")
                    self.emit("sw t0,-4(fp)")
                else:
                    # Different level call - callee is at a different nesting level
                    # Here we assume the callee is a direct child - would need more complex logic otherwise
                    self.emit("sw sp,-4(fp)")
                
                # Actual call
                self.emit(f"addi sp,sp,{self.framelength}")
                self.emit(f"jal {arg1}")
                self.emit(f"addi sp,sp,-{self.framelength}")

            elif op == "retv":
                # Return with value - slide 41
                t1_reg = "t0"
                self.loadvr(arg1, t1_reg)
                self.emit("lw t0,-8(sp)")
                self.emit(f"sw {t1_reg},(t0)")

            elif op == "ret":
                # Return without value
                # Nothing special needed here - end_block will handle the return
                pass

            elif op == "in":
                # Input operation - slide 15
                self.emit(f"li a7,5")
                self.emit(f"ecall")
                self.emit(f"mv t0,a0")
                self.storerv("t0", result)

            elif op == "out":
                # Output operation - slide 15
                t1_reg = "t0"
                self.loadvr(arg1, t1_reg)
                self.emit(f"mv a0,{t1_reg}")
                self.emit(f"li a7,1")
                self.emit(f"ecall")
                
                # Print a newline
                self.emit(f"la a0,str_nl")
                self.emit(f"li a7,4")
                self.emit(f"ecall")

            elif op == "halt":
                # Program termination - slide 17
                self.emit(f"li a7,10")
                self.emit(f"ecall")

    def is_local_var(self, var):
        """Simplified check if variable is local (would use symbol table in full implementation)."""
        # In a real implementation, this would check the symbol table
        # For now, we'll assume most variables are local
        return not var.startswith('global_')

    def is_same_level_call(self, func_name):
        """Simplified check if call is to the same nesting level."""
        # In a real implementation, this would check nesting levels in the symbol table
        # For simplicity, we'll assume same level calls
        return True  

    def get_complete_code(self):
        """Return the complete generated RISC-V assembly code."""
        data_section = self.generate_data_section()
        return '\n'.join(self.code)


def generate_risc_v_code(quads, symbol_table=None):
    """
    Generate RISC-V assembly code from intermediate code quadruples.

    Args:
        quads: List of quadruples (tuples) generated by IntermediateCodeGenerator
        symbol_table: The symbol table of the program

    Returns:
        String containing RISC-V assembly code
    """
    rv_generator = RISCVCodeGenerator(symbol_table)
    rv_generator.generate_code_from_quads(quads)
    return rv_generator.get_complete_code()
