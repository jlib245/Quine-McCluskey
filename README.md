# Quine-McCluskey
입력 방식

띄어쓰기로 구분해서 입력

ex) 교재 4.7 Solved Problems 3-c.

## input

(literal)

W X Y Z

(minterm)

1 3 5 6 7 13 14

(dontCare)

8 10 12

## output

<< essentialPrimeImplicant >>

W'Z

<< minimumSolution >>

W'Z + XYZ' + WXY'

W'Z + XY'Z + XYZ'
