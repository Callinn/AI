"""
7.Să se determine al k-lea cel mai mare element al unui șir de numere cu n elemente (k < n). De ex. al 2-lea cel mai mare element din șirul [7,4,6,3,9,1] este 7.
O(k*n)
    :param k-int: al catelea cel mai mare nr din lista
    :return: se afiseaza numarul respectiv.
"""
def al_k_lea_cel_mai_mare(lista, k):
    if not lista or k <= 0 or k > len(lista):
        return None

    lista = lista.copy()

    while k > 1:
        maxim = max(lista)
        lista = [num for num in lista if num != maxim]
        k -= 1

        if not lista:
            return None

    return max(lista)


def test():
    # Exemplul din enunț
    assert al_k_lea_cel_mai_mare([7,4,6,3,9,1], 2) == 7

    # Primul cel mai mare
    assert al_k_lea_cel_mai_mare([1,2,3,4], 1) == 4

    # Ultimul cel mai mare
    assert al_k_lea_cel_mai_mare([1,2,3,4], 4) == 1

    # k invalid
    assert al_k_lea_cel_mai_mare([1,2,3], 0) is None
    assert al_k_lea_cel_mai_mare([1,2,3], 5) is None

    # Listă goală
    assert al_k_lea_cel_mai_mare([], 1) is None


if __name__ == '__main__':
    test()
    print("Toate testele au trecut cu succes!")

    k = int(input("Al catelea cel mai mare numar? "))
    text = input("Introduceți numerele separate prin spațiu: ")

    if text.strip() == "":
        lista = []
    else:
        lista = list(map(int, text.split()))

    rezultat = al_k_lea_cel_mai_mare(lista, k)

    if rezultat is None:
        print("Valoare invalida sau lista vida.")
    else:
        print(f"Al {k}-lea cel mai mare element este:", rezultat)