MOV num, 100
MOV name, "Ahmad"
MOV marks, 50
MOV show, ""
CMP marks, 50
JG L1
JMP L1
L1:
MOV show, "You have passed the exam"
MOV a, 10
MOV b, 20
add:
MOV TMP2, a
ADD TMP2, b
MOV res, TMP2
CALL add a, b