#include <iostream>
#include <vector>

using Matrix = std::vector<std::vector<double>>;
// T(n) = 8·T(n/2) + O(n²)
// Helper: Add two matrices
Matrix add(const Matrix& A, const Matrix& B) {
    int n = A.size(), m = A[0].size();
    Matrix C(n, std::vector<double>(m));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            C[i][j] = A[i][j] + B[i][j];
    return C;
}

// Helper: Extract a submatrix from row r, col c of size sz x sz
Matrix submatrix(const Matrix& M, int r, int c, int sz) {
    Matrix S(sz, std::vector<double>(sz));
    for (int i = 0; i < sz; i++)
        for (int j = 0; j < sz; j++)
            S[i][j] = M[r + i][c + j];
    return S;
}

// Helper: Place submatrix S into M at position (r, c)
void place(Matrix& M, const Matrix& S, int r, int c) {
    for (int i = 0; i < (int)S.size(); i++)
        for (int j = 0; j < (int)S[0].size(); j++)
            M[r + i][c + j] = S[i][j];
}

// Recursive matrix multiplication (n must be a power of 2)
Matrix multiply_recursive(const Matrix& A, const Matrix& B) {
    int n = A.size();

    // Base case
    if (n == 1)
        return {{ A[0][0] * B[0][0] }};

    int half = n / 2;

    // Partition A and B into quadrants
    Matrix A11 = submatrix(A,    0,    0, half);
    Matrix A12 = submatrix(A,    0, half, half);
    Matrix A21 = submatrix(A, half,    0, half);
    Matrix A22 = submatrix(A, half, half, half);

    Matrix B11 = submatrix(B,    0,    0, half);
    Matrix B12 = submatrix(B,    0, half, half);
    Matrix B21 = submatrix(B, half,    0, half);
    Matrix B22 = submatrix(B, half, half, half);

    // C = A * B using 8 recursive multiplications
    // C11 = A11*B11 + A12*B21
    // C12 = A11*B12 + A12*B22
    // C21 = A21*B11 + A22*B21
    // C22 = A21*B12 + A22*B22
    Matrix C11 = add(multiply_recursive(A11, B11), multiply_recursive(A12, B21));
    Matrix C12 = add(multiply_recursive(A11, B12), multiply_recursive(A12, B22));
    Matrix C21 = add(multiply_recursive(A21, B11), multiply_recursive(A22, B21));
    Matrix C22 = add(multiply_recursive(A21, B12), multiply_recursive(A22, B22));

    // Assemble result
    Matrix C(n, std::vector<double>(n));
    place(C, C11,    0,    0);
    place(C, C12,    0, half);
    place(C, C21, half,    0);
    place(C, C22, half, half);

    return C;
}
