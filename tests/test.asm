start:
    # Simple test of ADDI, ADD, and SUB
    addi $1 0
    addi $1 1
    addi $2 2
    addi $3 3
    add $4 $3
    add $4 $1
    sub $5 $1
    sub $6 $3
    sub $6 $3
    # Testing assigni
    assigni $1 1
    assigni $2 2
    assigni $3 3
    assigni $4 4
    assigni $5 5
    # Testing store/load
    store $1 $1
    store $2 $2
    store $3 $3
    store $4 $4
    load $1 $7
    load $2 $6
    load $3 $5
    load $4 $4
    # BNE/BEQ test
    assigni $7 1
    assigni $1 1
    bne $1 start
    assigni $1 0
    beq $1 start
    bne $1 label
    assigni $1 100
label:
    assigni $1 1
    beq $1 label2
    assigni $1 100
label2:
    # SGT testing
    assigni $1 1
    assigni $2 200
    sgt $1 $2
    sgt $2 $1
    # In / Out Testing
    in $1 $0
    in $2 $1
    in $3 $2
    in $4 $3
    # Assign all button to 1
    assigni $1 1
    out $1 $0
    out $1 $1
    out $1 $2
    out $1 $3
    # Testing rand
    rand $1 1
    rand $2 2
    rand $3 3
    rand $4 4
    rand $5 5
    rand $6 6


