from .__functions import mask, validate


class Bits:
    def __init__(self, bits: int, shift: int, name: str):
        self.bits = bits
        self.mask = mask(bits)
        self.name = name
        self.shift = shift
        self.value = 0

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self)})"

    def __str__(self):
        return f"{self.value}"

    def __int__(self):
        return self.value

    def __get__(self, instance, cls):
        return self.value if instance is None else self

    def __set__(self, instance, other):
        if isinstance(other, int):
            self.value = other & self.mask
        elif isinstance(other, Bits):
            self.value = other.value & self.mask
        else:
            raise TypeError(f"{other} is not an int")

        return self

    def __radd__(self, other):
        return self.value + other

    def __add__(self, other):
        self.value = (self.value + other) & self.mask
        return self

    @validate
    def __lt__(self, other):
        return self.value < other

    @validate
    def __gt__(self, other):
        return self.value > other

    @validate
    def __xor__(self, other):
        return self.value ^ other

    @validate
    def __and__(self, other):
        return self.value & other

    @validate
    def __or__(self, other):
        return self.value | other

    @validate
    def __lshift__(self, other):
        return self.value << other

    @validate
    def __rshift__(self, other):
        return self.value >> other
