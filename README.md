## Quine-McCluskey 알고리즘이란?
Quine-McCluskey 알고리즘은 논리식을 최소화하는 알고리즘이다. 내부적으로는 카르노 맵과 동일하지만, 그림을 그려서 맞추는 카르노 맵과 달리 표를 사용하기 때문에 컴퓨터에서 쉽게 돌릴 수 있다. 또한 논리함수의 최소 형태를 결정론적으로 구할 수 있다.

> ### 구성
1. 주어진 함수의 후보항(Prime Implicants)들을 모두 구한다.
2. 후보항들을 이용해서 후보항 표에서 필수항(Essential Prime Implicant)을 구한다.

### 1. 후보항 구하기
$$f(a,b,c,d) = \sum m (0,1,2,5,6,7,8,9,10,14)$$
위와 같은  minterm의 조합이 있다면 다음과 같은 그림으로 나타낼 수 있다.
![](https://velog.velcdn.com/images/jlib245/post/4a3e3e6b-b1e9-4937-97d5-644dafd684b3/image.png)
각각의 그룹이름은 minterm을 2진수로 표현했을 때의 1의 개수를 의미 한다.
위와 같이 정리하고 나서, 인접한 그룹끼리 차례로 묶는다.
다음의 표를 살펴보자.
![](https://velog.velcdn.com/images/jlib245/post/12aebeab-6f7c-4981-883f-486094daf6a1/image.png)
Column 1은 우리가 위에서 보았던 그 표와 동일하다.
Column 1을 작성한 다음에는 차례로 column 2를 작성해야하는데,
작성하는 방법은 다음과 같다.
> 1. 차례로 인접하는 그룹 두 개를 선택해서 각 그룹의 원소 중 하나씩 고른다.
　 처음에는 group 0, 1를 고른 다음 2~3번을 수행한다. 나머지 group에 대해서도 순서대로 한다.
2. 두 원소 중 대쉬(-)칸을 제외한 자릿수 중 숫자가 다른 칸이 단 하나만 있다면
숫자가 다른 단 한 칸을 대쉬(-)칸으로 바꾼 원소를 다음 column에 생성한다.
두 원소에 체크(v)표시를 한다.
3. 가능한 모든 쌍을 찾아 반복한다. 이 쌍들은 곧 다시 하나의 group이된다. (마찬가지로 체크(v)표시를 한다.)
　 더 이상 선택할 이전 단계의 group이 없으면 4번으로 간다.
4. 새로운 column을 생성할 수 없을 때까지 1~3번의 과정을 반복한다.
5. 체크(v)표시를 하지 않은 원소들이 우리가 구해야 했던 후보항들이다.

### 2. 필수항 구하기
Quine-McCluskey method의 두번째 단계는 prime implicant chart를 통해서 minimum solution을 구하는 것이다.
먼저 prime implicant chart는 다음과 같이 prime implicant의 각각의 term들을 minterm의 번호에 맞게 X표시로 체크하여 그릴 수 있다.
![](https://velog.velcdn.com/images/jlib245/post/f3456353-2a3b-4562-8999-eec01c4651ae/image.png)
그러고 나서 X표시를 살펴보았을 때, 각 열당 X가 단 하나뿐인 minterm이 보일 것이다.
여기서는 9번과 14번이 X가 하나뿐이다. 
이러한 minterm들을 포함하는 prime implicant는 essential prime implicant이다.

### 3. minimum solution 구하기
![](https://velog.velcdn.com/images/jlib245/post/e5dce016-af94-4629-bc55-3bb08deaf36c/image.png)

위에서 찾아낸 essential prime implicant에 해당하는 X에 대해서 가로로 선을 긋는다.
이 예제에서는, b'c'와 cd'의 X에 대해서 각각 가로로 선을 긋는다.
여기서 지나간 X에 대해서 다시 세로로 선을 긋는다. 그러면 위와 같은 형태로 그려지게 된다.
여기서 선이 그어진 X들은 이미 해당 term에 포함된 minterm이라는 의미다.
다시 말해서 다른 term에서 해당 minterm을 포함하지 않아도 된다.
그림을 통해 보면, 이미 선이 그어진 X에 대해서는 다시 선을 그을 필요가 없다는 의미가 된다.

그리고 남아있는 X에 대해서도 선을 그어줘야 하는데,
가능한한 적은 수의 term을 선택하면서 모든 X에 선을 그을 수 있는 term들을 선택해야 한다.
여기서는 a'bd를 선택하게 되면 결국 모든 minterm을 cover하게 된다.
a'bd를 선택하면 a'bd위의 X에 선을 긋게 되고, 나머지 X에 대해서도 세로선으로 cover가 된다.
따라서 모든 X위에 선을 긋게 된 셈이다.
최종적으로 f = b'c' + cd' + a'bd 와 같은 minimum solution을 얻게 된다.

## 구현하기
### 구현 방법
먼저 Quine-McCluskey 알고리즘의 핵심은 don't care(-) 계산일 것이다.
나는 각각의 숫자를 don't care가 아닌 부분(대강 care라고 부르겠다.), don't care인 부분으로 나눠 튜플로 관리하였다.
1의 갯수와 별개로 같은 column 안에 don't care이 같아야 한다는 전제조건이 있기에 don't care 순대로 정렬한 뒤 don't care가 다르다면 break로 끊어 추가적인 탐색으로 낭비되는 시간을 아꼈다.
don't care가 같다면 care끼리 xor로 다른 부분의 갯수를 세어 단 1개라면 다음 column에 추가할 수 있다.
새로운 don't care는 기존 don't care와 xor로 계산했던 부분을 더하는 것으로 구할 수 있다.
새로운 care은 기존 care에서 새로운 don't care을 빼주는 것으로 구할 수 있다.

### 입력 방식

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
