import re

"""
1. Să se determine ultimul (din punct de vedere alfabetic) cuvânt care poate apărea într-un text care conține mai multe cuvinte separate prin ” ” (spațiu). 
De ex. ultimul (dpdv alfabetic) cuvânt din ”Ana are mere rosii si galbene” este cuvântul "si".

O(m*k)
m este numărul de cuvinte din listă,
k este lungimea medie a unui cuvânt (pentru comparații lexicografice).
    :param lista: Lista de cuvinte dintr-un text.
    :return: Cuvântul cu cea mai mare valoare alfabetică.
"""
def alfabetic(lista):
    if not lista:
        return None
    return max(lista)

def test():
    # Exemplul din enunț
    assert alfabetic(["Ana", "are", "mere", "rosii", "si", "galbene"]) == "si"

    # Un singur cuvânt
    assert alfabetic(["Ana"]) == "Ana"

    # Cuvinte deja ordonate
    assert alfabetic(["a", "b", "c", "d"]) == "d"

    # Cuvinte cu litere mari/mici (ASCII comparison)
    assert alfabetic(["ana", "Ana"]) == "ana"

    # Listă goală
    assert alfabetic([]) is None


"""O(n)"""
if __name__ == '__main__':
    test()
    print("Toate testele au trecut cu succes!")

    text = input("Textul este: ")
    lista_text= re.split(" ", text)
    print(alfabetic(lista_text))