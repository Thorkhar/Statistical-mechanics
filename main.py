##set variables
k = 1
T = 1

def efficiency(Ephoton, Egap, N):
    n = 0
    for i in range(0,N):
        if Ephoton > Egap:
            n += 1
    eff = n/N
    return eff
