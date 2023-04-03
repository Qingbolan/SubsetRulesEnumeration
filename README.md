# SubsetRulesEnumeration
"SubsetRulesEnumeration" seeks optimal subset collections from an integer set under specific constraints. With applications in scheduling and resource allocation, this project helps find the best element combinations following predefined rules.

- Description

  "SubsetRulesEnumeration," aims to find an optimal set of subsets, referred to as reS, from a given integer set {1, 2, ..., n} that satisfies the following conditions:

  1. Each subset in reS has a size of k.
  2. For all subsets nj of size j, there exists a subset reS_item ∈ reS such that nj is a subset of reS_item.
  3. For all subsets nj of size j, there exists a subset reS_item ∈ reS such that some subset of nj with size s is a subset of reS_item.

  The goal of the project is to identify the reS with the minimum length that fulfills these conditions. To achieve this, you have developed a Python program that uses the itertools library to generate combinations and searches for the desired subset collection reS by iteratively checking if they meet the specified rules.

  During the project, you attempted to utilize GPU acceleration to enhance search performance. As a result, you have modified the code to use the PyTorch library and attempted to execute the core computation on the GPU. However, as some parts of the existing code still run on the CPU, the GPU acceleration may not have provided a significant performance improvement.

  To fully leverage the GPU's computational capabilities, you may need to further investigate how to optimize and improve the existing code to better execute multidimensional combination generation and rule checking on the GPU.

- main body
  - 
