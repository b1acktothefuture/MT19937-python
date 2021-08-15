import MT19937OBJ as mersenne
import matplotlib.pyplot as plt

U, D = 11, 0xFFFFFFFF
S, B = 7, 0x9D2C5680
T, C = 15, 0xEFC60000
L = 18
N = 624


def inverseTemper(Y):
    Y = Y ^ (Y >> L)
    Y = ((Y << T) & C) ^ Y
    Y1 = Y
    i = 0
    while(i < 4):
        Y1 = Y ^ ((Y1 << S) & B)
        i += 1
    Y = Y1
    Y = Y ^ (Y >> U) ^ (Y >> 2*U)
    return Y


class Oracle():
    def __init__(self, seed):
        self.internal = mersenne.MT19937()
        self.internal.seedIT(seed)


def main():
    orac = Oracle(100)
    data = [0]*N
    L1 = []
    for i in range(N):
        temp = orac.internal.extract_number()
        L1.append(temp/(2**32))
        data[i] = (inverseTemper(temp))
    clone = mersenne.MT19937()
    clone.mt = data
    clone.index = N
    L2 = [0]*N
    for i in range(60):
        L1.append(orac.internal.extract_number()/(2**32))
        L2.append(clone.extract_number()/(2**32))

    b = 610
    plt.subplot(2, 1, 1)
    plt.plot(L1[b:])
    plt.title("Original")

    plt.subplot(2, 1, 2)
    plt.plot(L2[b:])
    plt.title("Cloned")

    plt.show()


main()
