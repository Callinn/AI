
"""
8.Să se genereze toate numerele (în reprezentare binară) cuprinse între 1 și n. De ex. dacă n = 4, numerele sunt: 1, 10, 11, 100.

O(log(n)*n)
    :param int: numar intreg.
    :return: lista cu toate numerele de la 1 la nr in baza 2.
"""
if __name__ == '__main__':
    nr = int(input("Introdu un nr: "))
    list=[]
    for i in range(1,nr+1):
        list.append(bin(i)[2:])
    print(list)

