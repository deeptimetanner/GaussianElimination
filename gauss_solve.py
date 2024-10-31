import numpy as np
from ctypes import CDLL, POINTER, c_int, c_double, byref
import os

class NoImplementationInC(Exception):
    """Exception raised if the C implementation is requested but unavailable."""
    pass

def plu(A, use_c=False):
    """Perform PLU decomposition with partial pivoting.

    Args:
        A (list of list of floats): The matrix to decompose.
        use_c (bool): If True, try to use the C implementation. Defaults to False.

    Returns:
        tuple: (P, L, U) where
            P (list of int): Permutation vector.
            L (list of list of floats): Lower triangular matrix with 1s on the diagonal.
            U (list of list of floats): Upper triangular matrix.
    """
    n = len(A)
    A_np = np.array(A, dtype=np.float64)

    if use_c:
        # Attempt to load the C library and call the C plu function
        try:
            lib_path = os.path.join(os.getcwd(), "libgauss.so")
            lib = CDLL(lib_path)
            print(f"Successfully loaded C library: {lib_path}")

            # Set the function signature for `plu` in the shared library
            c_plu = lib.plu
            c_plu.argtypes = [c_int, POINTER(c_double * (n * n)), POINTER(c_int * n)]
            c_plu.restype = None  # No return value for `plu`

            # Prepare matrix A and permutation vector P for ctypes
            A_ctypes = (c_double * (n * n))(*A_np.flatten())
            P_ctypes = (c_int * n)(*range(n))

            # Call the C function and handle any potential exceptions
            try:
                c_plu(n, A_ctypes, P_ctypes)
                print("C function 'plu' executed successfully.")

                # Convert the result back to Python types
                P = list(P_ctypes)
                A_decomposed = np.array(A_ctypes).reshape(n, n)

                # Extract L and U from A_decomposed
                L = np.tril(A_decomposed, -1) + np.eye(n)
                U = np.triu(A_decomposed)

                return P, L.tolist(), U.tolist()
            
            except Exception as e:
                print("Error calling C function 'plu':", e)
                raise NoImplementationInC("C implementation not available or failed.")

        except OSError as e:
            print(f"Error loading C library 'libgauss.so': {e}")
            raise NoImplementationInC("C library could not be loaded.")

    else:
        # Python implementation of PLU decomposition
        P = list(range(n))
        L = np.zeros((n, n))
        U = A_np.copy()

        for k in range(n):
            # Pivot
            max_index = max(range(k, n), key=lambda i: abs(U[i][k]))
            if U[max_index, k] == 0:
                raise ValueError("Matrix is singular and cannot be decomposed.")
            if max_index != k:
                # Swap rows in U and P
                U[[k, max_index]] = U[[max_index, k]]
                P[k], P[max_index] = P[max_index], P[k]
                L[[k, max_index]] = L[[max_index, k]]

            # Compute entries of L and U
            for i in range(k + 1, n):
                L[i, k] = U[i, k] / U[k, k]
                U[i, k:] -= L[i, k] * U[k, k:]

        # Fill diagonal of L with 1s
        np.fill_diagonal(L, 1)

        return P, L.tolist(), U.tolist()

def lu(A):
    """Perform LU decomposition without pivoting.

    Args:
        A (list of list of floats): The matrix to decompose.

    Returns:
        tuple: (L, U) where
            L (list of list of floats): Lower triangular matrix with 1s on the diagonal.
            U (list of list of floats): Upper triangular matrix.
    """
    n = len(A)
    A_np = np.array(A, dtype=np.float64)
    L = np.zeros((n, n))
    U = A_np.copy()

    for k in range(n):
        # Check for zero pivot element
        if U[k, k] == 0:
            raise ValueError("Zero pivot encountered; matrix is singular or requires pivoting.")

        # Compute entries of L and U
        for i in range(k + 1, n):
            L[i, k] = U[i, k] / U[k, k]
            U[i, k:] -= L[i, k] * U[k, k:]

    # Fill diagonal of L with 1s
    np.fill_diagonal(L, 1)

    return L.tolist(), U.tolist()

# Test Code
A = [[2.0, 3.0, -1.0],
     [4.0, 1.0, 2.0],
     [-2.0, 7.0, 2.0]]

# Python version
use_c = False
P, L, U = plu(A, use_c=use_c)
print("Python PLU Decomposition:")
print("P:", P)
print("L:", L)
print("U:", U)

# C version
use_c = True
try:
    P, L, U = plu(A, use_c=use_c)
    print("\nC PLU Decomposition:")
    print("P:", P)
    print("L:", L)
    print("U:", U)
except NoImplementationInC as e:
    print(e)
