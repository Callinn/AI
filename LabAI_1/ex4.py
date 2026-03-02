import re

"""
4. Să se determine cuvintele unui text care apar exact o singură dată în acel text. 
De ex. cuvintele care apar o singură dată în 
"ana are ana are mere rosii ana" 
sunt: 'mere' și 'rosii'.

Complexitate:
O(n^2) (din cauza count)
"""

def cuvinte_unice(lista_text):
    rezultat = []
    for elem in lista_text:
        if lista_text.count(elem) == 1:
            rezultat.append(elem)
    return rezultat


def test():
    # Exemplul din enunț
    assert cuvinte_unice(
        ["ana", "are", "ana", "are", "mere", "rosii", "ana"]
    ) == ["mere", "rosii"]

    # Toate unice
    assert cuvinte_unice(["a", "b", "c"]) == ["a", "b", "c"]

    # Niciun unic
    assert cuvinte_unice(["a", "a", "b", "b"]) == []

    # Un singur cuvânt
    assert cuvinte_unice(["ana"]) == ["ana"]

    # Listă goală
    assert cuvinte_unice([]) == []


if __name__ == '__main__':
    test()
    print("Toate testele au trecut cu succes!")

    text = input("Textul este: ")
    lista_text = re.split(" ", text)

    rezultat = cuvinte_unice(lista_text)

    if not rezultat:
        print("Nu există cuvinte cu apariție unică.")
    else:
        print("Cuvintele cu apariție unică sunt:")
        for elem in rezultat:
            print(elem)