import re

"""
O(m*k)
m este numărul de cuvinte din listă,
k este lungimea medie a unui cuvânt (pentru comparații lexicografice).
    :param lista: Lista de cuvinte dintr-un text.
    :return: Cuvântul cu cea mai mare valoare alfabetică.
"""
def alfabetic(lista):
    return max(lista)


"""O(n)"""
if __name__ == '__main__':
    text = input("Textul este: ")
    lista_text= re.split(" ", text)
    print(alfabetic(lista_text))