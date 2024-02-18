; x69 ASM
; `Face Drawing`
; Made for Chip69
; By FunWithAlbi
; 2024

; DRW call draws pixels from point (TX, TY) to point (EX, EY)

CLS ; Clear the screen

; Draw the left eye
MV TX, 280
MV TY, 120
MV EX, 300
MV EY, 140
DRW

; Draw the right eye
MV TX, 340
MV TY, 120
MV EX, 360
MV EY, 140
DRW

; Draw the mouth
MV TX, 280
MV TY, 180
MV EX, 360
MV EY, 180
DRW

; When drawing letters or numbers you can
; set the size * that you want for it
MV TF, 2

; Draws letter `H`
MV TX, (25 * 2)
MV TY, 25
DRL 8

; Draws letter `I`
MV TX, (30 * 2)
MV TY, 25
DRL 9

; Draws number `5`
MV TX, (35 * 2)
MV TY, 25

CMP 1, 2 ; Compare 1 with 2
SE       ; Skip next instruction if 1 == 2

DRN 5    ; Draws number `0`

MV TX, (40 * 2)
MV TY, 25

CMP 1, 1 ; Compare 1 with 1
SNE      ; Skip next instruction if 1 != 1

DRN 0    ; Draws number `0`

; Sleeps for TF seconds
MV TF, 5
SLP

CLR ; Set the value of all registers to 0

EXT ; Exits the program