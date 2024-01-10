import numpy as np


np.random.seed(42)
matrix = np.random.randint(low= -10, high= 10, size = (4,4))

if matrix.shape[0] != matrix.shape[1]:
    raise ValueError("shape error")

matrix = matrix.astype(float)

dimension = matrix.shape[0]

for col in range(1,dimension):

    if matrix[col, col] == 0:
        continue

    else:
        for line in range(0, col):  # col - 1, -1, -1

            factor = matrix[line, col] / matrix[col, col]
            matrix[line, col:] -= factor * matrix[col, col:]

print(matrix)

det = np.prod(np.diag(matrix))