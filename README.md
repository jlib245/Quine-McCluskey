# Quine-McCluskey Algorithm이란?
Quine-McCluskey 알고리즘은 논리식을 최소화하는 알고리즘이다. 내부적으로는 카르노 맵과 동일하지만, 그림을 그려서 맞추는 카르노 맵과 달리 표를 사용하기 때문에 컴퓨터에서 쉽게 돌릴 수 있다. 또한 논리함수의 최소 형태를 결정론적으로 구할 수 있다.

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
