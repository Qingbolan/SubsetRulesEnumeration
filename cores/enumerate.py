from tqdm import tqdm

from rule.rule_test import *
# from tool.tools import comb_compute

def comb_compute(n, k, device):
    if k * 2 > n:
        k = n - k

    result = torch.tensor(1, dtype=torch.float32, device=device)

    for i in range(n - k + 1, n + 1):
        result *= i

    for _ in range(1, k + 1):
        result /= _

    return int(result.item())


def combinations_of_combinations(tensor, r):
    indices = torch.arange(r, device=tensor.device).unsqueeze(0)
    n = tensor.size(0)
    max_indices = torch.tensor([n], device=tensor.device)
    stop = False
    while not stop:
        yield tensor[indices]
        stop = True
        for i in range(r - 1, -1, -1):
            if indices[0, i] + 1 < max_indices - (r - 1 - i):
                stop = False
                indices[0, i:] = torch.arange(indices[0, i] + 1, indices[0, i] + 1 + r - i, device=tensor.device)
                break

def find_min_reS_length(n, k, j, s, device):
    for reL in range(n-k+1, n + 1):
        AnOk = torch.combinations(torch.arange(1, n + 1, device=device), k)
        subsets = combinations_of_combinations(AnOk, reL)
        total_subsets = comb_compute(len(AnOk), reL,device)

        for reS in tqdm(subsets, total=total_subsets, desc=f"reL: {reL}", ncols=100):
            if rule_check(reS, n, k, j, s):
                return reS, reL

    return torch.tensor([[0]], device=device), -1

def enumerate_core(device, n, k, j, s):
    reS, reL = find_min_reS_length(n, k, j, s, device)
    return reS, reL

# # 设置 PyTorch 使用 GPU
# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# print(f"Using device: {device}")

# # 在 GPU 上执行代码
# reS, reL = enumerate_core(10, 6, 4, 4, device)

# print(f"reS: {reS}")
# print(f"reL: {reL}")
