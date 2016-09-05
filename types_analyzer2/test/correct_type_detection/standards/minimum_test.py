# Scalar values assignment
i = 1  # expects: int  ### i: int
r = 1.4  # expects: float  ### r: float
b = True  # expects: bool  ### b: bool
n = None  # expects: NoneType  ### n: NoneType
s = "Hello"  # expects: str  ### s: str

# List value assignments
alist = []  # expects: list  ### alist: list
ilist = [1, 2]  # expects: list<int>  ### ilist: list<int>
rlist = [1.1, 1.2]  # expects: list<float>  ### rlist: list<float>
nlist = [1, 2.5]  # expects: list<_numeric>  ### nlist: list<_numeric>
vlist = [1, None]  # expects: list  ### vlist: list

# Tuples assignment
x, y = 1, 2  # expects: x: int, y: int  ### x: int, y: int
xx, yy = r, i  # expects: xx: float, yy: int  ### xx: float, yy: int

# Arithmetics operations
i_plus_i = 1 + 2  # expects: int  ### i_plus_i: int
i_plus_r = 1 + r  # expects: float  ### i_plus_r: float
s_mul_i = s * 2  # expects: str  ### s_mul_i: str

# Value methods call
sl = s.lower()  # expects: str  ### sl: str
sil = s.islower()  # expects: bool  ### sil: bool
