from dataclasses import dataclass
from typing import List


@dataclass
class Literal:
    var_index: int
    negated: bool


Clause = List[Literal]
Formula = List[Clause]


def evaluate_clause(clause: Clause, assignment: List[bool]) -> bool:
    for lit in clause:
        value = assignment[lit.var_index]

        if lit.negated:
            value = not value

        if value:
            return True

    return False


def evaluate_formula(formula: Formula, assignment: List[bool]) -> bool:
    for clause in formula:
        if not evaluate_clause(clause, assignment):
            return False

    return True


def print_formula(formula: Formula, var_names: List[str]) -> None:
    print("\nFormula (CNF): ", end="")

    for c, clause in enumerate(formula):
        print("(", end="")

        for l, lit in enumerate(clause):
            if lit.negated:
                print("¬", end="")

            print(var_names[lit.var_index], end="")

            if l + 1 < len(clause):
                print(" ∨ ", end="")

        print(")", end="")

        if c + 1 < len(formula):
            print(" ∧ ", end="")

    print()


def solve(formula: Formula, var_names: List[str]) -> bool:
    n = len(var_names)
    total_combinations = 1 << n

    print(f"\nVariables: {n}")
    print(f"Total combinations: {total_combinations}")

    print_formula(formula, var_names)

    satisfiable = False
    solutions = []

    for mask in range(total_combinations):

        assignment = []

        for i in range(n):
            assignment.append(bool((mask >> (n - 1 - i)) & 1))

        result = evaluate_formula(formula, assignment)

        if result:
            satisfiable = True
            solutions.append(assignment)

    print("\n================ RESULT ================")

    if satisfiable:
        print("SATISFIABLE")
        print(f"\nFound {len(solutions)} satisfying assignment(s):\n")

        for s, sol in enumerate(solutions, start=1):

            print(f"Solution #{s}:")

            for i, name in enumerate(var_names):
                print(f"  {name} = {'T' if sol[i] else 'F'}")

            print()

    else:
        print("UNSATISFIABLE")
        print("No assignment makes the formula true.")


    return satisfiable


def main() -> None:

    var_names = ["P", "Q", "R"]

    formula = [
        [Literal(0, False), Literal(1, False)],
        [Literal(0, True),  Literal(2, False)],
        [Literal(1, True),  Literal(2, True)],
    ]

    solve(formula, var_names)

    print("UNSAT Example:")
    print("(P) ∧ (¬P)")

    var_names2 = ["P"]

    unsat_formula = [
        [Literal(0, False)],
        [Literal(0, True)],
    ]

    solve(unsat_formula, var_names2)


if __name__ == "__main__":
    main()
