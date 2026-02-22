// Strassen: only 7 recursive multiplications instead of 8
// T(n) = 7·T(n/2) + O(n²)
Matrix multiply_strassen(const Matrix& A, const Matrix& B) {
    int n = A.size();

    if (n == 1)
        return {{ A[0][0] * B[0][0] }};

    int half = n / 2;

    Matrix A11 = submatrix(A,    0,    0, half);
    Matrix A12 = submatrix(A,    0, half, half);
    Matrix A21 = submatrix(A, half,    0, half);
    Matrix A22 = submatrix(A, half, half, half);

    Matrix B11 = submatrix(B,    0,    0, half);
    Matrix B12 = submatrix(B,    0, half, half);
    Matrix B21 = submatrix(B, half,    0, half);
    Matrix B22 = submatrix(B, half, half, half);

    // 7 Strassen products
    Matrix M1 = multiply_strassen(add(A11, A22), add(B11, B22));
    Matrix M2 = multiply_strassen(add(A21, A22), B11);
    Matrix M3 = multiply_strassen(A11,            subtract(B12, B22));
    Matrix M4 = multiply_strassen(A22,            subtract(B21, B11));
    Matrix M5 = multiply_strassen(add(A11, A12), B22);
    Matrix M6 = multiply_strassen(subtract(A21, A11), add(B11, B12));
    Matrix M7 = multiply_strassen(subtract(A12, A22), add(B21, B22));

    // Combine
    Matrix C11 = add(subtract(add(M1, M4), M5), M7);
    Matrix C12 = add(M3, M5);
    Matrix C21 = add(M2, M4);
    Matrix C22 = add(subtract(add(M1, M3), M2), M6);

    Matrix C(n, std::vector<double>(n));
    place(C, C11,    0,    0);
    place(C, C12,    0, half);
    place(C, C21, half,    0);
    place(C, C22, half, half);
    return C;
}
