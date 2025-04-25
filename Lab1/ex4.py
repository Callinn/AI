import re


"""
    :param lista: Lista de cuvinte dintr-un text.
    :return: afiseaza cuvintele cu aparitie unica in text
    
    O(n+n)
"""
if __name__ == '__main__':
    text = input("Textul este: ")
    lista_text= re.split(" ", text)
    for elem in lista_text:
        if lista_text.count(elem) == 1:
            print(elem)