#########################################################################
# RISC-V Code Generator                                                 #
# This part of the code generates RISC-V assembly from intermediate     #
# quadruples code.                                                      #
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
            return self.get_var_address(var)

    def get_var_address(self, var):
        """Get or create a memory address for a variable using the symbol table if available."""
        if var in self.var_map:
            return self.var_map[var]

        # If we have a symbol table, try to get variable offset from it
        if self.symbol_table:
            entity = self.symbol_table.lookup(var)
            if entity and hasattr(entity, 'offset'):
                self.var_map[var] = entity.offset
                return entity.offset

        # If not found in symbol table or we don't have one
        self.var_map[var] = self.next_data_addr
        self.next_data_addr += 4  # Assume 4 bytes per variable (32-bit)
        self.global_vars.add(var)
        return self.var_map[var]

    def get_assembly_label(self, quad_label):
        """Convert a quad label to an assembly label."""
        if quad_label not in self.label_map:
            self.label_map[quad_label] = f"L{quad_label}"
        return self.label_map[quad_label]

    def load_value(self, operand, dest_reg):
        """Load a value (constant, variable, or temporary) into a register."""
        if operand.startswith('T_'):
            # If operand is a temporary, get its register
            src_reg = self.temp_map.get(operand)
            if src_reg:
                self.emit(f"mv {dest_reg}, {src_reg}")
            else:
                # This should not happen in a well-formed program
                self.emit(f"# Warning: Temporary {operand} not allocated")
        elif operand.isdigit() or (operand[0] == '-' and operand[1:].isdigit()):
            # If operand is a numeric constant
            self.emit(f"li {dest_reg}, {operand}")
        else:
            # If operand is a program variable
            addr = self.get_var_address(operand)
            self.emit(f"lw {dest_reg}, {addr}(s0)")

    def store_value(self, src_reg, dest):
        """Store a value from a register to a memory location."""
        if dest.startswith('T_'):
            # If destination is a temporary, get its register
            dest_reg = self.temp_map.get(dest)
            if dest_reg:
                self.emit(f"mv {dest_reg}, {src_reg}")
            else:
                # This should not happen in a well-formed program
                self.emit(f"# Warning: Temporary {dest} not allocated")
        else:
            # If destination is a program variable
            addr = self.get_var_address(dest)
            self.emit(f"sw {src_reg}, {addr}(s0)")

    def emit(self, instruction):
        """Add an instruction to the generated code."""
        self.code.append(instruction)

    def emit_label(self, label):
        """Emit a label."""
        self.code.append(f"{label}:")

    def generate_data_section(self):
        """Generate the data section for variables."""
        data_section = [".data"]

        # Add global variables
        for var in self.global_vars:
            data_section.append(f"{var}: .word 0")

        # Add string literals if any
        for label, string in self.string_literals.items():
            data_section.append(f"{label}: .string \"{string}\"")

        return data_section

    def generate_code_from_quads(self, quads):
        """Generate RISC-V assembly code from quadruples."""
        # Initialize code with entry point
        self.emit(".text")
        self.emit(".globl main")

        for quad in quads:
            label, op, arg1, arg2, result = quad

            # Emit label for this quad if needed
            asm_label = self.get_assembly_label(label)
            self.emit_label(asm_label)

            # Process based on operation
            if op == "begin_block":
                if arg1 == "τεστ":  # Main program
                    self.emit("main:")
                    self.emit("addi sp, sp, -64")  # Allocate stack frame
                    self.emit("sw ra, 60(sp)")  # Save return address
                    self.emit("sw s0, 56(sp)")  # Save frame pointer
                    self.emit("addi s0, sp, 64")  # Set new frame pointer
                else:
                    # Function or procedure
                    self.current_function = arg1
                    self.emit(f"{arg1}:")
                    self.emit("addi sp, sp, -64")  # Allocate stack frame
                    self.emit("sw ra, 60(sp)")  # Save return address
                    self.emit("sw s0, 56(sp)")  # Save frame pointer
                    self.emit("addi s0, sp, 64")  # Set new frame pointer

            elif op == "end_block":
                if arg1 == "τεστ":  # Main program
                    self.emit("lw ra, 60(sp)")  # Restore return address
                    self.emit("lw s0, 56(sp)")  # Restore frame pointer
                    self.emit("addi sp, sp, 64")  # Deallocate stack frame
                    self.emit("ret")  # Return from main
                else:
                    # Function or procedure
                    self.current_function = None
                    self.emit("lw ra, 60(sp)")  # Restore return address
                    self.emit("lw s0, 56(sp)")  # Restore frame pointer
                    self.emit("addi sp, sp, 64")  # Deallocate stack frame
                    self.emit("ret")  # Return from function

            elif op == "+":
                t1_reg = "t0"
                t2_reg = "t1"
                result_reg = "t2" if not result.startswith('T_') else self.allocate_register(result)

                self.load_value(arg1, t1_reg)
                self.load_value(arg2, t2_reg)
                self.emit(f"add {result_reg}, {t1_reg}, {t2_reg}")

                if not result.startswith('T_'):
                    self.store_value(result_reg, result)

            elif op == "-":
                t1_reg = "t0"
                t2_reg = "t1"
                result_reg = "t2" if not result.startswith('T_') else self.allocate_register(result)

                self.load_value(arg1, t1_reg)
                self.load_value(arg2, t2_reg)
                self.emit(f"sub {result_reg}, {t1_reg}, {t2_reg}")

                if not result.startswith('T_'):
                    self.store_value(result_reg, result)

            elif op == "*":
                t1_reg = "t0"
                t2_reg = "t1"
                result_reg = "t2" if not result.startswith('T_') else self.allocate_register(result)

                self.load_value(arg1, t1_reg)
                self.load_value(arg2, t2_reg)
                self.emit(f"mul {result_reg}, {t1_reg}, {t2_reg}")

                if not result.startswith('T_'):
                    self.store_value(result_reg, result)

            elif op == "/":
                t1_reg = "t0"
                t2_reg = "t1"
                result_reg = "t2" if not result.startswith('T_') else self.allocate_register(result)

                self.load_value(arg1, t1_reg)
                self.load_value(arg2, t2_reg)
                self.emit(f"div {result_reg}, {t1_reg}, {t2_reg}")

                if not result.startswith('T_'):
                    self.store_value(result_reg, result)

            elif op == ":=":
                src_reg = "t0"
                dest_reg = "t1" if result.startswith('T_') else None

                self.load_value(arg1, src_reg)

                if result.startswith('T_'):
                    dest_reg = self.allocate_register(result)
                    self.emit(f"mv {dest_reg}, {src_reg}")
                else:
                    self.store_value(src_reg, result)

            elif op == "<":
                t1_reg = "t0"
                t2_reg = "t1"

                self.load_value(arg1, t1_reg)
                self.load_value(arg2, t2_reg)

                # Jump to the destination label if arg1 < arg2
                target_label = self.get_assembly_label(result)
                self.emit(f"blt {t1_reg}, {t2_reg}, {target_label}")

            elif op == "<=":
                t1_reg = "t0"
                t2_reg = "t1"
                result_reg = "t2" if result.startswith('T_') else None

                self.load_value(arg1, t1_reg)
                self.load_value(arg2, t2_reg)

                if result.startswith('T_'):
                    # Store comparison result (1 if true, 0 if false)
                    result_reg = self.allocate_register(result)
                    self.emit(f"slt {result_reg}, {t2_reg}, {t1_reg}")  # result = (arg2 < arg1)
                    self.emit(f"xori {result_reg}, {result_reg}, 1")  # result = !result
                else:
                    # Jump to the destination label if arg1 <= arg2
                    target_label = self.get_assembly_label(result)
                    self.emit(f"ble {t1_reg}, {t2_reg}, {target_label}")

            elif op == ">":
                t1_reg = "t0"
                t2_reg = "t1"

                self.load_value(arg1, t1_reg)
                self.load_value(arg2, t2_reg)

                # Jump to the destination label if arg1 > arg2
                target_label = self.get_assembly_label(result)
                self.emit(f"bgt {t1_reg}, {t2_reg}, {target_label}")

            elif op == ">=":
                t1_reg = "t0"
                t2_reg = "t1"

                self.load_value(arg1, t1_reg)
                self.load_value(arg2, t2_reg)

                # Jump to the destination label if arg1 >= arg2
                target_label = self.get_assembly_label(result)
                self.emit(f"bge {t1_reg}, {t2_reg}, {target_label}")

            elif op == "=":
                t1_reg = "t0"
                t2_reg = "t1"

                self.load_value(arg1, t1_reg)
                self.load_value(arg2, t2_reg)

                # Jump to the destination label if arg1 == arg2
                target_label = self.get_assembly_label(result)
                self.emit(f"beq {t1_reg}, {t2_reg}, {target_label}")

            elif op == "<>":
                t1_reg = "t0"
                t2_reg = "t1"

                self.load_value(arg1, t1_reg)
                self.load_value(arg2, t2_reg)

                # Jump to the destination label if arg1 != arg2
                target_label = self.get_assembly_label(result)
                self.emit(f"bne {t1_reg}, {t2_reg}, {target_label}")

            elif op == "jump":
                # Unconditional jump
                target_label = self.get_assembly_label(result)
                self.emit(f"j {target_label}")

            elif op == "jumpz":
                # Jump if zero (condition is false)
                t1_reg = "t0"
                self.load_value(arg1, t1_reg)

                target_label = self.get_assembly_label(result)
                self.emit(f"beqz {t1_reg}, {target_label}")

            elif op == "jumpnz":
                # Jump if not zero (condition is true)
                t1_reg = "t0"
                self.load_value(arg1, t1_reg)

                target_label = self.get_assembly_label(result)
                self.emit(f"bnez {t1_reg}, {target_label}")

            elif op == "par":
                # Handle parameter passing
                # arg2 indicates parameter passing method (cv: call by value)
                if arg2 == "cv":
                    # Call by value - load the value into a register
                    t1_reg = "t0"
                    self.load_value(arg1, t1_reg)
                    # Store parameter in stack (simplified approach)
                    self.emit(f"sw {t1_reg}, -4(sp)")
                    self.emit(f"addi sp, sp, -4")
                elif arg2 == "ret":
                    # Return value parameter - save space for return value
                    self.emit(f"addi sp, sp, -4")  # Reserve space for return value

            elif op == "call":
                # Function or procedure call
                self.emit(f"jal ra, {arg1}")
                # Adjust stack pointer after call (parameters cleanup would be here)

            elif op == "retv":
                # Return with value
                t1_reg = "t0"
                self.load_value(arg1, t1_reg)
                self.emit(f"mv a0, {t1_reg}")  # Return value in a0

            elif op == "ret":
                # Return without value
                pass  # The end_block will handle the actual return

            elif op == "in":
                # Input operation
                self.emit(f"li a7, 5")  # System call code for reading integer
                self.emit(f"ecall")  # Make the system call
                self.emit(f"mv t0, a0")  # Move input value to t0
                self.store_value("t0", result)  # Store input in the result variable

            elif op == "out":
                # Output operation
                t1_reg = "t0"
                self.load_value(arg1, t1_reg)
                self.emit(f"mv a0, {t1_reg}")  # Move value to a0 for printing
                self.emit(f"li a7, 1")  # System call code for printing integer
                self.emit(f"ecall")  # Make the system call
                # Print a newline
                self.emit(f"li a0, 10")  # Newline character
                self.emit(f"li a7, 11")  # System call code for printing character
                self.emit(f"ecall")  # Make the system call

            elif op == "halt":
                # Program termination
                self.emit(f"li a7, 10")  # System call code for exit
                self.emit(f"ecall")  # Make the system call

    def get_complete_code(self):
        """Return the complete generated RISC-V assembly code."""
        data_section = self.generate_data_section()
        return '\n'.join(data_section + [''] + self.code)


def generate_risc_v_code(quads, symbol_table=None):
    """
    Generate RISC-V assembly code from intermediate code quadruples.

    Args:
        quads: List of quadruples (tuples) generated by IntermediateCodeGenerator

    Returns:
        String containing RISC-V assembly code
        :param symbol_table: the symbol table of the program
    """
    rv_generator = RISCVCodeGenerator(symbol_table)
    rv_generator.generate_code_from_quads(quads)
    return rv_generator.get_complete_code()
