def get_lowest_bits(n, number_of_bits):
    mask = (1 << number_of_bits) - 1
    return n & mask


class MT19937:
    W, N, M, R = 32, 624, 397, 31
    A = 0x9908B0DF
    U, D = 11, 0xFFFFFFFF
    S, B = 7, 0x9D2C5680
    T, C = 15, 0xEFC60000
    L = 18
    F = 1812433253
    LOWER_MASK = (1 << R) - 1
    UPPER_MASK = get_lowest_bits(not LOWER_MASK, W)
    mt = []
        
       
    def seedIT(self,seed):
        #seed the mersenne twister, and initialize the states
        self.mt = []
        self.index = self.N
        self.mt.append(seed)
        for i in range(1, self.index):
            self.mt.append(get_lowest_bits(self.F * (self.mt[i - 1] ^ (self.mt[i - 1] >> (self.W - 2))) + i, self.W))

    def extract_number(self):
        #applies the tempering function(invertible) to the state wrt to index and outputs the result
        if self.index >= self.N:
            self.twist()

        y = self.mt[self.index]
        y ^= (y >> self.U) & self.D
        y ^= (y << self.S) & self.B
        y ^= (y << self.T) & self.C
        y ^= (y >> self.L)
        self.index += 1
        return get_lowest_bits(y, self.W)

    def twist(self):
        #after we have used all the randomness we twist the 624 states 
        for i in range(self.N):
            x = (self.mt[i] & self.UPPER_MASK) + (self.mt[(i + 1) % self.N] & self.LOWER_MASK)
            x_a = x >> 1
            if x % 2 != 0:
                x_a ^= self.A

            self.mt[i] = self.mt[(i + self.M) % self.N] ^ x_a

        self.index = 0



def main():
    seed = int(input("enter seed: "))
    n = int(input("enter n: "))
    rng = MT19937()
    rng.seedIT(seed)
    li = [0]*n
    for i in range(n):
        li[i] = rng.extract_number()/2**32
    
    print(li)


#main()