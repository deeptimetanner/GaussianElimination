import numpy as np
from gauss_solve import plu  # Import your PLU decomposition function

# Reference matrices
A = np.array([
    [2, 3, -1],
    [4, 1, 2],
    [-2, 7, 2]
], dtype=float)

b = np.array([5, 6, 3], dtype=float)
x_ref = np.array([13/10, 8/10, 0], dtype=float)  # Reference solution vector

# Perform PLU decomposition using your function
P_vec, L, U = plu(A)

# Convert L and U to numpy arrays for matrix operations
L = np.array(L)
U = np.array(U)

# Convert the permutation vector to a permutation matrix
P_matrix = np.eye(len(P_vec))[P_vec]

# Validate PLU decomposition: Check if P * A equals L * U
PA = np.dot(P_matrix, A)
LU = np.dot(L, U)
plu_decomposition_valid = np.allclose(PA, LU)

# Validate solution to A * x = b with the provided solution vector x_ref
solution_valid = np.allclose(np.dot(A, x_ref), b)

# Output the results
print("PLU Decomposition Validation:")
print("P * A equals L * U:", plu_decomposition_valid)
print("\nP (Permutation Matrix):")
print(P_matrix)
print("\nL:")
print(L)
print("\nU:")
print(U)
print("\nP * A:")
print(PA)
print("\nL * U:")
print(LU)
print("\nOriginal A:")
print(A)

print("\nSolution Validation:")
print("A * x_ref equals b:", solution_valid)
print("Expected b:", b)
print("Computed b from A * x_ref:", np.dot(A, x_ref))
