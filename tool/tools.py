def comb_compute(n,k):
    if k*2>n:
        k=n-k
    result = 1
    for i in range(n-k+1,n+1):
        # print(i,end=" ")
        result *= i

    # print(result)
    for _ in range(1, k+1):
        # print(f"{_} [{result}]",end="_")
        result = result / _
    # print("")
    # print(result)

    return int(result)