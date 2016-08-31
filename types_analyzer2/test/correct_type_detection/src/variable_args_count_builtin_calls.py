# Built-in functions (using kwlist of kwdict arguments passing) calls
round_1 = round(1)  # expects: int
round_2 = round(1, 2)  # expects: int
round_3 = round(1.2, 2)  # expects: float

max_1 = max([1, 2])  # expects: int
max_1a = max(1, 2)  # expects: int
max_2 = max([1, 2, 3])  # expects: int
max_2a = max(1, 2, 3)  # expects: int
max_3 = max([1, 2, 3, 4])  # expects: int
max_3a = max(1, 2, 3, 4)  # expects: int
max_4 = max([1, 2.4, 3])  # expects: _numeric
max_4a = max(1, 2.4, 3)  # expects: _numeric
max_5 = max([1, 2, 3, 3.5])  # expects: _numeric
max_5a = max(1, 2, 3, 3.5)  # expects: _numeric
max_6 = max([1.2, 3.4])  # expects: float
max_6a = max(1.2, 3.4)  # expects: float

min_1 = min([1, 2])  # expects: int
min_1a = min(1, 2)  # expects: int
min_2 = min([1, 2, 3])  # expects: int
min_2a = min(1, 2, 3)  # expects: int
min_3 = min([1, 2, 3, 4])  # expects: int
min_3a = min(1, 2, 3, 4)  # expects: int
min_4 = min([1, 2.4, 3])  # expects: _numeric
min_4a = min(1, 2.4, 3)  # expects: _numeric
min_5 = min([1, 2, 3, 3.5])  # expects: _numeric
min_5a = min(1, 2, 3, 3.5)  # expects: _numeric
min_6 = min([1.2, 3.4])  # expects: float
min_6a = min(1.2, 3.4)  # expects: float
