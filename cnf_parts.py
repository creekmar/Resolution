from dataclasses import dataclass


@dataclass
class Predicate:
    name: str
    param: list
    neg: bool

    def __eq__(self, other):
        if not isinstance(other, Predicate):
            return NotImplemented
        return self.name == other.name


@dataclass
class Parameter:
    name: str
    type: int

    def __eq__(self, other):
        if not isinstance(other, Parameter):
            return NotImplemented
        return self.name == other.name and self.type == other.type


@dataclass
class Function:
    name: str
    param: Parameter

    def __eq__(self, other):
        if not isinstance(other, Function):
            return NotImplemented
        return self.name == other.name
