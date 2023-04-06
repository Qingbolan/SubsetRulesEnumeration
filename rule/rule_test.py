import itertools


class RuleCheck:
    def __init__(self, reS, n, k, j, s):
        self.error = 0
        self.TestS = reS

        # Check the length of each set
        for subset in self.TestS:
            if len(subset) != k:
                self.error = 1
                break

        if self.error == 0:
            # Initialize the AnOj
            self.sample_space = range(1, n + 1)
            self.AnOj = itertools.combinations(self.sample_space, j)

            # Check Rule 1
            if j != k:
                if not self.rule_1():
                    self.error = 2

            # Check Rule 2
            if j != s and self.error == 0:
                self.error = self.check_rule_2()

    def rule_1(self):
        # Check if every subset of size j is a subset of some set in TestS
        for subset in self.AnOj:
            if not any(set(subset).issubset(set(test_set)) for test_set in self.TestS):
                return False
        return True

    def check_rule_2(self):
        for comb in itertools.combinations(range(1, len(self.sample_space) + 1), self.j):
            AjOs = itertools.combinations(comb, self.s)
            if not any(
                any(set(a).issubset(set(test_set)) for test_set in self.TestS)
                for a in AjOs
            ):
                return 3
        return 0

    def display(self):
        return self.error


def rule_check(reS, n, k, j, s):
    rule_check_obj = RuleCheck(reS, n, k, j, s)
    return rule_check_obj.display() == 0
