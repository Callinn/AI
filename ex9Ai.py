'''
Considerându-se o matrice cu n x m elemente întregi
și o listă cu perechi formate din coordonatele a 2
căsuțe din matrice ((p,q) și (r,s)), să se calculeze
suma elementelor din sub-matricile identificate de fiecare pereche.
'''

# Time complexity: O(n * m + k)
# Space complexity: O(n * m)

def sums_matrix(matrix, pairs):
    if not matrix or not matrix[0]:
        return []

    n = len(matrix)
    m = len(matrix[0])

    # Construire matrice sume parțiale (n+1 x m+1)
    prefix = [[0 for _ in range(m + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            prefix[i][j] = (
                matrix[i - 1][j - 1]
                + prefix[i - 1][j]
                + prefix[i][j - 1]
                - prefix[i - 1][j - 1]
            )

    result = []

    for pair in pairs:
        # normalizare coordonate (robust la coordonate inversate)
        x1 = min(pair[0][0], pair[1][0])
        y1 = min(pair[0][1], pair[1][1])
        x2 = max(pair[0][0], pair[1][0])
        y2 = max(pair[0][1], pair[1][1])

        # deplasare pentru matricea prefix
        x1 += 1
        y1 += 1
        x2 += 1
        y2 += 1

        total = (
            prefix[x2][y2]
            - prefix[x1 - 1][y2]
            - prefix[x2][y1 - 1]
            + prefix[x1 - 1][y1 - 1]
        )

        result.append(total)

    return result


def test():
    # Exemplul din enunț
    assert sums_matrix([
        [0, 2, 5, 4, 1],
        [4, 8, 2, 3, 7],
        [6, 3, 4, 6, 2],
        [7, 3, 1, 8, 3],
        [1, 5, 7, 9, 4]],
        [[[1, 1], [3, 3]], [[2, 2], [4, 4]]]
    ) == [38, 44]

    # Submatrici mici
    assert sums_matrix([
        [0, 2, 3],
        [4, 8, 2],
        [6, 3, 4]],
        [[[1, 1], [1, 1]], [[0, 0], [1, 1]], [[0, 0], [0, 0]]]
    ) == [8, 14, 0]

    # Lista vida
    assert sums_matrix([
        [1, 2],
        [3, 4]],
        []
    ) == []

    # Coordonate inversate (test suplimentar de robustete)
    assert sums_matrix([
        [0, 2, 5],
        [4, 8, 2],
        [6, 3, 4]],
        [[[2, 2], [1, 1]]]
    ) == [17]  # suma elementelor din submatricea (1,1)-(2,2)

    # Matrice 1x1
    assert sums_matrix([[5]], [[[0, 0], [0, 0]]]) == [5]


if __name__ == '__main__':
    test()