# Scalar values assignment
i = 1  # expects: int
r = 1.4  # expects: float
b = True  # expects: bool
n = None  # expects: NoneType
s = "Hello"  # expects: str

# List value assignments
alist = []  # expects: list
ilist = [1, 2]  # expects: list<int>
rlist = [1.1, 1.2]  # expects: list<float>
nlist = [1, 2.5]  # expects: list<_numeric>
vlist = [1, None]  # expects: list

# Tuples assignment and values reuse
a, b = 1, 2  # expects: a: int, b: int
a = i  # expects: int
b = r  # expects: float
a, b = r, i  # expects: a: float, b: int

# Arithmetics operations
a = 1 + 2  # expects: int
b = 1 + r  # expects: float
c = s * 2  # expects: str

# Value methods call
sl = s.lower()  # expects: str
sil = s.islower()  # expects: bool


