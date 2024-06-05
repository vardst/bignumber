import re

class BigNumber:
    ZERO = None
    ONE = None

    notations = []
    notations_set = set()

    @staticmethod
    def init_notations():
        BigNumber.notations = ["k", "m", "b", "t"]
        for i in range(26):
            for j in range(26):
                target = chr(ord('a') + i)
                second = chr(ord('a') + j)
                notation = f"{target}{second}"
                BigNumber.notations.append(notation)
                BigNumber.notations_set.add(notation)

    def __init__(self, value=0):
        self.original_input_string = str(value)
        self.mantissa = 0.0
        self.exponent = 0
        if isinstance(value, str):
            self._parse_string(value)
        elif isinstance(value, (int, float)):
            self.mantissa = value
        self._calculate()

    def _parse_string(self, value):
        pattern = re.compile(r"([0-9\.]*)([a-zA-Z]*)")
        matcher = pattern.match(value)
        if matcher and matcher.group(1):
            self.mantissa = float(matcher.group(1))
            notation = matcher.group(2)
            if notation:
                self.exponent = (BigNumber.notations.index(notation) + 1) * 3

    def _calculate(self):
        while self.mantissa >= 10:
            self.mantissa /= 10
            self.exponent += 1
        while self.mantissa < 1 and self.mantissa != 0:
            self.mantissa *= 10
            self.exponent -= 1

    def add(self, other):
        if isinstance(other, BigNumber):
            if self.exponent == other.exponent:
                self.mantissa += other.mantissa
            elif self.exponent > other.exponent:
                self.mantissa += other.mantissa * 10 ** (other.exponent - self.exponent)
            else:
                self.mantissa = self.mantissa * 10 ** (self.exponent - other.exponent) + other.mantissa
                self.exponent = other.exponent
        else:
            self.mantissa += other
        self._calculate()
        return self

    def sub(self, other):
        if isinstance(other, BigNumber):
            if self.exponent == other.exponent:
                self.mantissa -= other.mantissa
            elif self.exponent > other.exponent:
                self.mantissa -= other.mantissa * 10 ** (other.exponent - self.exponent)
            else:
                self.mantissa = self.mantissa * 10 ** (self.exponent - other.exponent) - other.mantissa
                self.exponent = other.exponent
        else:
            self.mantissa -= other
        self._calculate()
        return self

    def multiply(self, other):
        if isinstance(other, BigNumber):
            self.mantissa *= other.mantissa
            self.exponent += other.exponent
        else:
            self.mantissa *= other
        self._calculate()
        return self

    def divide(self, other):
        if isinstance(other, BigNumber):
            self.mantissa /= other.mantissa
            self.exponent -= other.exponent
        else:
            self.mantissa /= other
        self._calculate()
        return self

    def pow(self, exponent):
        self.mantissa = self.mantissa ** exponent
        self.exponent *= exponent
        self._calculate()
        return self

    def __lt__(self, other):
        if self.exponent == other.exponent:
            return self.mantissa < other.mantissa
        return self.exponent < other.exponent

    def __eq__(self, other):
        return self.mantissa == other.mantissa and self.exponent == other.exponent

    def __str__(self):
        return f"{self.mantissa}e{self.exponent}"

    def to_float(self):
        return self.mantissa * 10 ** self.exponent

    @staticmethod
    def from_float(value):
        return BigNumber(value)

BigNumber.ZERO = BigNumber(0)
BigNumber.ONE = BigNumber(1)
BigNumber.init_notations()