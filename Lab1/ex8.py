
"""O(log(n)*n)
    :param int: numar intreg.
    :return: lista cu toate numerele de la 1 la nr in baza 2.
"""
if __name__ == '__main__':
    nr = int(input("Introdu un nr: "))
    list=[]
    for i in range(1,nr+1):
        list.append(bin(i)[2:])
    print(list)

