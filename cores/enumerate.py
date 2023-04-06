from rule.rule_test import *
import itertools
from tqdm import tqdm

from tool.tools import comb_compute


def rule_check(reS, n, k, j, s):
    for j_value in range(s, j + 1):
        Anj = list(itertools.combinations(range(1, n + 1), j_value))
        for nj in Anj:
            if not any(set(nj).issubset(reS_item) for reS_item in reS):
                return False
    return True

def find_min_reS_length(n, k, j, s):
    for reL in range(n-k+1, n + 1):
        AnOk = list(itertools.combinations(range(1, n + 1), k))
        subsets = itertools.combinations(AnOk, reL)
        total_subsets = comb_compute(len(AnOk), reL)

        for reS in tqdm(subsets, total=total_subsets, desc=f"reL: {reL}", ncols=100):
            if rule_check(reS, n, k, j, s):
                return reS, reL

    return [[0]], -1

def enumerate_core(n, k, j, s):
    reS, reL = find_min_reS_length(n, k, j, s)
    return reS, reL


# reS, reL = enumerate_core(10, 6, 4, 4)
# print(f"reS:{reS}")
# print(f"reL:{reL}")