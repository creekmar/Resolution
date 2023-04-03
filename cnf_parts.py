from dataclasses import dataclass


VAR = 0
CONST = 1


@dataclass
class Predicate:
    name: str
    param: list
    neg: bool

    def __eq__(self, other):
        if not isinstance(other, Predicate):
            return NotImplemented
        return self.name == other.name and self.neg == other.neg and len(self.param) == len(other.param)

    def opposites(self, other):
        if not isinstance(other, Predicate):
            return NotImplemented
        if self.name != other.name or self.neg == other.neg:
            return False
        if len(self.param) != len(other.param):
            return False
        para_list = []
        alias = {}
        # looping through the parameters in the predicate to see if you can unify
        for i in range(len(self.param)):
            paraA = self.param[i]
            paraB = other.param[i]
            if type(paraA) is Function:
                if paraB is Parameter:
                    if paraB.type == CONST:
                        return False
                    else:  # Variable
                        if paraA.name == paraB.param.name:
                            return False
                        else:
                            alias[paraA.param.name] = paraB.name
                else:  # Function
                    if paraB.name != paraA.name:
                        return False
                    else:  # Variable
                        alias[paraA.param.name] = paraB.param.name
            elif paraA.type == VAR:
                if type(paraB) is Function:
                    if paraA.name == paraB.param.name:
                        return False
                else:
                    alias[paraA.name] = paraB.name
            else:  # Constant
                if type(paraB) is Function:
                    return False
                elif paraB.type == CONST:
                    if paraA.name != paraB.name:
                        return False
                else:  # Variable
                    alias[paraB.name] = paraA.name

        return alias


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
