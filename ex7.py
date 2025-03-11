"""O(k*n)
    :param k-int: al catelea cel mai mare nr din lista
    :return: se afiseaza numarul respectiv.
"""
if __name__ == '__main__':
    k = int(input("Al catelea cel mai mare numar?"))
    lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    while k > 1:
        maxim = max(lista)
        lista=[num for num in lista if num!=maxim ]
        k=k-1
    print(max(lista))