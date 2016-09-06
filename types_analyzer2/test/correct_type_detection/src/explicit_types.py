bool_1 = bool()  # expects: bool
bool_2 = bool(123)  # expects: bool
bytearray_1 = bytearray()  # expects: bytearray
bytearray_2 = bytearray(10)  # expects: bytearray
bytearray_3 = bytearray([1,2,3])  # expects: bytearray
bytearray_4 = bytearray(b"123")  # expects: bytearray
bytearray_5 = bytearray("hello", "ascii")  # expects: bytearray
bytes_1 = bytes()  # expects: bytes
bytes_2 = bytes(10)  # expects: bytes
bytes_3 = bytes([1,2,3])  # expects: bytes
bytes_4 = bytes(b"123")  # expects: bytes
bytes_5 = bytes("hello", "ascii")  # expects: bytes
complex_1 = complex()  # expects: complex
complex_2 = complex(1)  # expects: complex
complex_3 = complex(1.5)  # expects: complex
complex_4 = complex(1.4, 1.6)  # expects: complex
complex_5 = complex(complex(1,0), complex(0,1))  # expects: complex
complex_6 = complex("1+2j")  # expects: complex
dict_1 = dict()  # expects: { object: object }
dict_2 = dict({})  # expects: { object: object }
dict_3 = dict({"1": 2})  # expects: { str: int }
dict_4 = dict( [ (1, "2"), (3, "4") ] )  # expects: { int: str }
int_1 = int()  # expects: int
int_2 = int(10)  # expects: int
int_3 = int("AD", 16)  # expects: int
int_4 = int(b"AD", 16)  # expects: int
int_5 = int("10")  # expects: int
float_1 = float()  # expects: float
float_2 = float(1)  # expects: float
float_3 = float(1.4)  # expects: float
float_4 = float("1.2")  # expects: float
float_5 = float(b"1.9")  # expects: float
list_1 = list()  # expects: list
list_2 = list([])  # expects: list
list_3 = list([1,2,3])  # expects: list<int>
str_1 = str()  # expects: str
str_2 = str(10)  # expects: str
str_3 = str(complex(10, 15)) # expects: str
str_4 = str("Hello")  # expects: str
str_5 = str(b"Hello", encoding="ascii")  # expects: str
str_6 = str(b"Hello", encoding="ascii", errors="strict")  # expects: str
tuple_1 = tuple()
tuple_2 = tuple([])
tuple_3 = tuple([1,2,3])