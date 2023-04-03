# import itertools
#
#
# def rule_check(reS, n, k, j, s):
#     # Check the length of each set
#     for _ in reS:
#         if len(_) != k:
#             return False
#
#     sample_space = range(1, n + 1)
#
#     # Check Rule 1
#     if j != k:
#         AnOj = itertools.combinations(sample_space, j)
#         for _ in AnOj:
#             if not any(set(_).issubset(set(__)) for __ in reS):
#                 return False
#
#     # Check Rule 2
#     if j != s:
#         for _ in itertools.combinations(sample_space, j):
#             AjOs = itertools.combinations(_, s)
#             if not any(any(set(__).issubset(set(___)) for ___ in reS) for __ in AjOs):
#                 return False
#
#     return True
import torch


def rule_check(reS, n, k, j, s):
    # Check the length of each set
    if not (reS.size(1) == k):
        return False

    sample_space = torch.arange(1, n + 1, device=reS.device)

    # Check Rule 1
    if j != k:
        AnOj = torch.combinations(sample_space, j)
        intersection_counts = torch.sum(reS[:, None, :] == AnOj[None, :, :], dim=2)
        if not torch.all(torch.any(intersection_counts == j, dim=0)):
            return False

    # Check Rule 2
    if j != s:
        for _ in torch.combinations(sample_space, j):
            AjOs = torch.combinations(_, s)
            intersection_counts = torch.sum(reS[:, None, :] == AjOs[None, :, :], dim=2)
            if not torch.all(torch.any(intersection_counts == s, dim=0)):
                return False

    return True
