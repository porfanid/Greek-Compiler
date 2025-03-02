.data
αύξηση: .word 0
α: .word 0
χ: .word 0
γ: .word 0
β: .word 0

.text
.globl main
L0:
main:
addi sp, sp, -64
sw ra, 60(sp)
sw s0, 56(sp)
addi s0, sp, 64
L1:
αύξηση:
addi sp, sp, -64
sw ra, 60(sp)
sw s0, 56(sp)
addi s0, sp, 64
L2:
lw t0, 0(s0)
li t1, 1
add t0, t0, t1
L3:
mv t0, t0
sw t0, 4(s0)
L4:
lw t0, 0(s0)
li t1, 1
add t1, t0, t1
L5:
mv t0, t1
sw t0, 8(s0)
L6:
lw ra, 60(sp)
lw s0, 56(sp)
addi sp, sp, 64
ret
L7:
τύπωσε_συν_1:
addi sp, sp, -64
sw ra, 60(sp)
sw s0, 56(sp)
addi s0, sp, 64
L8:
lw t0, 12(s0)
li t1, 1
add t2, t0, t1
L9:
mv t0, t2
mv a0, t0
li a7, 1
ecall
li a0, 10
li a7, 11
ecall
L10:
lw ra, 60(sp)
lw s0, 56(sp)
addi sp, sp, 64
ret
L11:
li t0, 1
sw t0, 0(s0)
L12:
lw t0, 0(s0)
sw t0, -4(sp)
addi sp, sp, -4
L13:
lw t0, 4(s0)
sw t0, -4(sp)
addi sp, sp, -4
L14:
addi sp, sp, -4
L15:
jal ra, αύξηση
L16:
# Warning: Temporary T_3 not allocated
sw t0, 16(s0)
L17:
li t0, 1
sw t0, 0(s0)
L18:
lw t0, 0(s0)
li t1, 8
slt t0, t1, t0
xori t0, t0, 1
L19:
mv t0, t0
beqz t0, L31
L20:
li t0, 1
sw t0, 4(s0)
L21:
lw t0, 4(s0)
li t1, 8
slt t1, t1, t0
xori t1, t1, 1
L22:
mv t0, t1
beqz t0, L28
L23:
lw t0, 0(s0)
sw t0, -4(sp)
addi sp, sp, -4
L24:
jal ra, τύπωσε_συν_1
L25:
lw t0, 4(s0)
li t1, 2
add t2, t0, t1
L26:
mv t0, t2
sw t0, 4(s0)
L27:
j L21
L28:
lw t0, 0(s0)
li t1, 2
add t0, t0, t1
L29:
mv t0, t0
sw t0, 0(s0)
L30:
j L18
L31:
li t0, 1
sw t0, 4(s0)
L32:
lw t0, 4(s0)
li t1, 10
blt t0, t1, L34
L33:
j L43
L34:
lw t0, 4(s0)
li t1, 10
blt t0, t1, L36
L35:
j L42
L36:
lw t0, 4(s0)
li t1, 1
add t1, t0, t1
L37:
mv t0, t1
sw t0, 4(s0)
L38:
j L41
L39:
lw t0, 4(s0)
li t1, 2
add t2, t0, t1
L40:
mv t0, t2
sw t0, 4(s0)
L41:
j L34
L42:
j L32
L43:
li a7, 5
ecall
mv t0, a0
sw t0, 4(s0)
L44:
lw t0, 4(s0)
li t1, 1
add t0, t0, t1
L45:
mv t0, t0
sw t0, 4(s0)
L46:
li t0, 0
li t1, 100
sub t1, t0, t1
L47:
lw t0, 4(s0)
mv t1, t1
blt t0, t1, L49
L48:
j L44
L49:
li a7, 10
ecall
L50:
lw ra, 60(sp)
lw s0, 56(sp)
addi sp, sp, 64
ret