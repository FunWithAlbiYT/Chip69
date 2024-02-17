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