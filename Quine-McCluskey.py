'''
입력 방식
띄어쓰기로 구분해서 입력

ex) 교재 4.7 Solved Problems 3-c.

>> input
(literal)
W X Y Z
(minterm)
1 3 5 6 7 13 14
(dontCare)
8 10 12

>> output
<< essentialPrimeImplicant >>
W'Z
<< minimumSolution >>
W'Z + XYZ' + WXY'
W'Z + XY'Z + XYZ'
'''


def custom_sort(tup:tuple):
    care , dontCare = tup
    # dontCare 순으로 배치
    return dontCare
def custom_sort_res(tup: tuple):
    # 1. 비용이 작은 순 2. 사전 순으로 배치
    le = len(tup)
    return -le, tup

def QM_compare(a : tuple, b : tuple):
    # xor해서 다른 비트가 1개일 때 (True, 새로운 dontCare) 리턴
    calculed = a[0]^b[0]
    if calculed.bit_count() == 1:
        newDontCare = calculed | a[1]
        return True, newDontCare
    else:
        return False, 0

def QM_one_column(c : int):
    lenc = len(lst[c])
    lst[c].sort(key=custom_sort)
    TF = [True for _ in range(lenc)]
    for i in range(lenc):
        for j in range(i+1, lenc):
            # dontCare이 다를 경우 break로 다음 group으로
            if lst[c][i][1] != lst[c][j][1] :
                break
            tf, newDontCare = QM_compare(lst[c][i], lst[c][j])
            if tf:
                TF[i] = False # 체크(v)표시
                TF[j] = False
                newCare = lst[c][i][0]&(~newDontCare)
                # (원래 숫자에서 dontCare만 뺀 값, 새로운 dontCare값)을 다음 그룹에 추가
                add_ = (newCare, newDontCare)
                if c+1 == len(lst):
                    lst.append([add_])
                else:
                    lst[c+1].append(add_)
    for i in range(lenc):
        # 한 column이 끝날 때 체크되지 않은 term 확인
        if TF[i] :
            prime_implicant.append(lst[c][i])
    return

def bt_term_ing(n : int, base : int):
    if n == len(bt_term_basis):
        return
    for i in range(n+1, len(bt_term_basis)):
        bt_term_lst.append(2**bt_term_basis[i])
        bt_term_res.append(base + sum(bt_term_lst))
        bt_term_ing(i, base)
        bt_term_lst.pop()
    return
        
def bt_term(l : list, base : int):
    global bt_term_res, bt_term_lst, bt_term_basis
    bt_term_res = [base]
    bt_term_lst = []
    bt_term_basis = l
    bt_term_ing(-1, base)
    return tuple(sorted(bt_term_res))

def bt_min_ing(n : int, essential: list, remains : set, basis : list):
    # bt_min_lst에 포함된 것들로 남은 minterm을 전부 충족시키는 경우 리턴
    setCheck = set()
    for i in bt_min_lst:
        for j in i:
            if j in remains:
                setCheck.add(j)
    if setCheck == remains:
        bt_min_res.append(essential + sorted(bt_min_lst,key=custom_sort_res))
        return
    for i in range(n+1, len(basis)):
        bt_min_lst.append(basis[i])
        bt_min_ing(i, essential, remains, basis)
        bt_min_lst.pop()
    return 

def bt_min(essential : list, remains : set, reL : set):
    global bt_min_res, bt_min_lst
    bt_min_res = []
    bt_min_lst = []
    bt_min_ing(-1, essential, remains, list(reL))
    # term의 개수가 가장 짧은 것들만 선별
    min_count = len(minterm)
    for i in bt_min_res:
        if min_count > len(i):
            min_count = len(i)
    count_res = []
    for i in bt_min_res:
        if len(i) == min_count:
            count_res.append(i)
    # 비용이 가장 작은 것들 선별
    min_cost = 0
    cost_lst = []
    res = []
    for i in count_res:
        cost = 0
        for j in i:
            cost += len(j) 
        cost_lst.append(cost)   
        if min_cost < cost:
            min_cost = cost
    for i in range(len(count_res)):
        if cost_lst[i] == min_cost:
            res.append(count_res[i])

    return res

def QM_min():
    set_ = set(prime_implicant)
    reL = set()
    # 백트래킹으로 각 term마다 가능한 수들을 계산
    for tup in set_:
        c, dc = tup
        ndc = bin(dc)[2:]
        p = []
        for i in range(len(ndc)):
            if ndc[-1-i] == '1':
                p.append(i)
        reL.add(bt_term(p, c))
    # essential prime number 구하기
    dic = dict()
    for i in minterm:
        dic[i] = set()
    for i in reL:
        for j in i:
            if j in dic:
                dic[j].add(i)
    res = set()
    ls = set(minterm)
    prev = None
    fin = True
    essentialPrimeImplicant = set()
    for i in dic:
        if len(dic[i]) == 1:
            essentialPrimeImplicant.add(list(dic[i])[0])
    while ls:
        for i in dic:
            if len(dic[i]) == 1:
                a = dic[i].pop()
                ls.discard(i)
                for j in a:
                    ls.discard(j)
                for k in dic:
                    dic[k].discard(i)
                    if not dic[k]:
                        ls.discard(k)
                reL.discard(a)
                res.add(a)
        # 더 줄여지지 않는 경우에 break
        if prev == ls:
            fin = False
            break
        prev = ls
    # minimum solution이 구해진 경우 list 씌워서 리턴
    if fin:
        return [list(res)], sorted(list(essentialPrimeImplicant), key=custom_sort_res)
    # 아직 남아 있는 경우 백트래킹으로 가능한 경우 계산해서 리턴
    else:
        return bt_min(sorted(list(res),key=custom_sort_res), ls, reL), sorted(list(essentialPrimeImplicant), key=custom_sort_res)
            
def QM():
    global lst, prime_implicant
    lst = [[]]
    prime_implicant = []
    # 0 번째 column 생성
    for i in minterm+dontCare:
        lst[0].append((i, 0))
    i = 0
    # 0 번째 column부터 계산 시작
    while i < len(lst):
        QM_one_column(i)
        i += 1
    # minimum solution 계산
    minimumSolution, essentialPrimeImplicant = QM_min()
    change_to_term(essentialPrimeImplicant)
    for i in range(len(minimumSolution)):
        change_to_term(minimumSolution[i])
    return minimumSolution, essentialPrimeImplicant

def tuple_to_term(tup:tuple):
    # Care 구하기
    care = 2**maxDigit-1
    for i in range(len(tup)):
        for j in range(i, len(tup)):
            care &= ~(tup[i]^tup[j])
    
    res = ""
    stdd = bin(tup[0])
    binCare = bin(care)
    for i in range(maxDigit):
        if binCare[-i-1] == '1':
            a = literal[-i-1]
            if len(stdd)-3 < i or stdd[-i-1] == '0':
                a += "'"
            res = a + res
    return res

def change_to_term(llll : list):
    for i in range(len(llll)):
        llll[i] = tuple_to_term(llll[i])
    return


print("literal")
literal = input().split()
print("minterm")
minterm = list(map(int, input().split()))
print("dontCare")
dontCare= list(map(int, input().split()))

# 입력된 리터럴의 개수로 가능한 minterm보다 큰 수가 minterm으로 입력될 경우 에러 발생
if max(minterm+dontCare) > 2**len(literal)-1:
    print("Error")
    exit()

a = max(minterm+dontCare)
maxDigit = len(bin(a))-2
minimumSolution, essentialPrimeImplicant = QM()
print("<< essentialPrimeImplicant >>")
print(*essentialPrimeImplicant, sep=', ')
print("<< minimumSolution >>")
for i in minimumSolution:
    print(*i, sep=' + ')

