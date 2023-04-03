"""
Ming Creekmore
Professor Orfan
Introduction to AI

"""

import sys
import cnf_parts


VAR = 0
CONST = 1


def make_clauses(variables, constants, string):
    clauses = list()
    lines = string.split("\n")

    # each line represents a single clause and predicates is the list of predicates in a clause
    for line in lines:
        line = line.split()
        predicates = list()
        # to skip any blank lines
        if len(line) == 0:
            continue

        # pred is each predicate in the line
        for pred in line:
            param = list()
            if pred[0] == "!":
                neg = True
                pred = pred[1:]
            else:
                neg = False

            # getting only the parameters in the predicate
            parenth = pred.find("(")
            if parenth != -1:
                name = pred[:parenth]
                param_str = pred[parenth+1:-1].split(",")

                # assigning parameters to variable, constant, or function
                for para in param_str:
                    parenth = para.find("(")
                    if parenth == -1:
                        if para in variables:
                            param.append(cnf_parts.Parameter(para, VAR))
                        elif para in constants:
                            param.append(cnf_parts.Parameter(para, CONST))
                    else:
                        func_name = para[:parenth]
                        func_para = para[parenth+1:-1]
                        if func_para in variables:
                            p = cnf_parts.Parameter(func_para, VAR)
                        else:
                            p = cnf_parts.Parameter(func_para, CONST)
                        param.append(cnf_parts.Function(func_name, p))
                predicates.append(cnf_parts.Predicate(name, param, neg))
            predicates.append(cnf_parts.Predicate(pred, [], neg))
        clauses.append(predicates)

    return clauses


def parse_file(filename):
    with open(filename) as file:
        file.readline()
        line = file.readline().split()
        line.pop(0)
        variables = set(line)
        line = file.readline().split()
        line.pop(0)
        constants = set(line)
        file.readline()
        file.readline()
        clauses = make_clauses(variables, constants, file.read())
        return clauses


def resolution(clauses):
    tocheck = clauses.copy()
    unification = {}
    while len(tocheck) != 0:
        current = tocheck.pop()
        for clause in clauses:
            unified = current.copy()
            unified.extend(clause)
            for predA in current:
                for predB in clause:
                    #print(predA.neg, predA.name, predB.neg, predB.name)
                    alias = predA.opposites(predB)
                    if alias is not False:
                        #print("BEFORE", unified)
                        unified.remove(predA)
                        unified.remove(predB)
                        #print("ERROR",unified)
                        if len(unified) == 0:
                            return False
                        for pred in unified:
                            if pred is cnf_parts.Parameter:
                                if pred.name in alias:
                                    pred.name = alias[pred.name]
                            if pred is cnf_parts.Function:
                                if pred.param.name in alias:
                                    pred.param.name = alias[pred.param.name]
                        tocheck.append(unified)
    return True



def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        clauses = parse_file(filename)
        if resolution(clauses):
            print("Yes")
        else:
            print("No")
    else:
        print("Usage: python3 lab2.py KB.cnf ")


if __name__ == '__main__':
    main()
