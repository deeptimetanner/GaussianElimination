#include <math.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <fenv.h>
#include "gauss_solve.h"
#include "helpers.h"
#include "gauss_solve.h"

// Size of the matrix
#define N 3

typedef void (*sighandler_t)(int); // Typedef for signal handler

// Signal handler for floating-point exceptions
void fpe_handler(int sig) {
    if (sig == SIGFPE) {
        printf("Floating point exception occurred, ignoring...\n");
    }
}

// Test for the PLU decomposition and other matrix operations
void test_plu() {
    double A[N][N] = {
        {2, 3, -1},
        {4, 1, 2},
        {-2, 7, 2}
    };
    int P[N];

    printf("Testing PLU decomposition:\n");
    plu(N, A, P);

    printf("Permutation vector P:\n");
    for (int i = 0; i < N; i++) {
        printf("%d ", P[i]);
    }
    printf("\n");

    printf("Matrix A after PLU decomposition (L and U stored in-place):\n");
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            printf("%f ", A[i][j]);
        }
        printf("\n");
    }
}

// Other test functions for the gauss_solve library
void test_gauss_solve() {
    const double A0[N][N] = {
        {2, 3, -1},
        {4, 1, 2},
        {-2, 7, 2}
    };
    const double b0[N] = {5, 6, 3};
    double A[N][N], b[N];

    memcpy(A, A0, sizeof(A0));
    memcpy(b, b0, sizeof(b0));

    gauss_solve_in_place(N, A, b);

    printf("Solution vector x:\n");
    for (int i = 0; i < N; i++) {
        printf("%f ", b[i]);
    }
    printf("\n");
}

int main() {
    // Setting up a signal handler for floating-point exceptions (if needed)
    sighandler_t old_handler = signal(SIGFPE, fpe_handler);

    // Run tests
    test_plu();
    test_gauss_solve();

    // Restore the old signal handler (optional cleanup)
    signal(SIGFPE, old_handler);

    return EXIT_SUCCESS;
}
