def cat(*bits):
    # Concatenate an unknown number of bits and return an integer.
    r = 0
    for b in bits:
        r <<= 1
        if b:
            r += int(b)
    return r


class History(object):
    # A cell and its neighborhood. The center cell's next state is property Z.
    bits = None

    def __init__(self, bits):
        self.bits = bits & 511

    # Each of the nine individual cells.
    @property
    def nw(self):
        return bool(self.bits & 256)

    @property
    def n(self):
        return bool(self.bits & 128)

    @property
    def ne(self):
        return bool(self.bits & 64)

    @property
    def w(self):
        return bool(self.bits & 32)

    @property
    def c(self):
        return bool(self.bits & 16)

    @property
    def e(self):
        return bool(self.bits & 8)

    @property
    def sw(self):
        return bool(self.bits & 4)

    @property
    def s(self):
        return bool(self.bits & 2)

    @property
    def se(self):
        return bool(self.bits & 1)

    @property
    def Z(self):
        # The next state the center cell will be.
        neighbors = sum([self.nw, self.n, self.ne,
                        self.w,          self.e,
                        self.sw, self.s, self.se])
        return (self.c, neighbors) in [(True, 2), (True, 3), (False, 3)]

    # The eight shift operations.
    @property
    def NW(self):
        return cat(self.nw, self.n,
                   self.w,  self.c)

    @property
    def N(self):
        return cat(self.nw, self.n, self.ne,
                   self.w,  self.c, self.e)

    @property
    def NE(self):
        return cat(self.n, self.ne,
                   self.c, self.e)

    @property
    def W(self):
        return cat(self.nw, self.n,
                   self.w,  self.c,
                   self.sw, self.s)

    @property
    def C(self):
        return cat(self.nw, self.n, self.ne,
                   self.w,  self.c, self.e,
                   self.sw, self.s, self.se)

    @property
    def E(self):
        return cat(self.n, self.ne,
                   self.c, self.e,
                   self.s, self.se)

    @property
    def SW(self):
        return cat(self.w,  self.c,
                   self.sw, self.s)

    @property
    def S(self):
        return cat(self.w,  self.c, self.e,
                   self.sw, self.s, self.se)

    @property
    def SE(self):
        return cat(self.c, self.e,
                   self.s, self.se)



