"""O(n^2)
6. Pentru un șir cu n numere întregi care conține și duplicate,
să se determine elementul majoritar (care apare de mai mult de n / 2 ori).
De ex. 2 este elementul majoritar în șirul [2,8,7,2,2,5,2,3,1,2,2].
"""


def element_majoritar(lista):
    for i in lista:
        if len(lista) / 2 < lista.count(i):
            return i
    return None


def test():
    # Exemplul din enunț
    assert element_majoritar([2, 8, 7, 2, 2, 5, 2, 3, 1, 2, 2]) == 2

    # Alt exemplu
    assert element_majoritar([1, 1, 1, 2, 3]) == 1

    # Fără element majoritar
    assert element_majoritar([1, 2, 3, 4]) is None

    # Un singur element
    assert element_majoritar([5]) == 5

    # Listă goală
    assert element_majoritar([]) is None


if __name__ == '__main__':
    test()
    print("Toate testele au trecut cu succes!")

    text = input("Introduceți numerele separate prin spațiu: ")

    if text.strip() == "":
        lista = []
    else:
        lista = list(map(int, text.split()))

    rezultat = element_majoritar(lista)

    if rezultat is None:
        print("Nu există element majoritar.")
    else:
        print("Elementul majoritar este:", rezultat)