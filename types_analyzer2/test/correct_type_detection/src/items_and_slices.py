ilist = [1, 2, 3, 4, 5]
i1 = ilist[0]  # expects: int
i2 = ilist[1:2]  # expects: list<int>
i3 = ilist[:2]  # expects: list<int>
i4 = ilist[1:]  # expects: list<int>
i5 = ilist[:]  # expects: list<int>

s = "Hello, World!"
s1 = s[0]  # expects: str
s2 = s[1:2]  # expects: str
s3 = s[:2]  # expects: str
s4 = s[1:]  # expects: str
s5 = s[:]  # expects: str