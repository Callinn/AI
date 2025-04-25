import re
import webbrowser
import pandas as pd
import unicodedata


#Descriere: Numara propozitiile dintr-un fisier text.
#Input: `file_path` - calea către fișierul text.
#Output: Numărul de propoziții din text.
def numar_propozitii(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    # Folosim regex pentru a împărți textul în propoziții
    propozitii = re.split(r'[.!?]', text)
    # Eliminăm propozițiile goale
    propozitii = [propozitie.strip() for propozitie in propozitii if propozitie.strip()]
    return len(propozitii)

#Descriere: Numara cuvintele dintr-un fisier text.
#Input: `file_path` - calea către fișierul text.
#Output: Numărul de cuvinte din text.
def numar_cuvinte(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    cuvinte = text.split()
    return len(cuvinte)

#Descriere: Numara cuvintele diferite dintr-un fisier text.
#Input: `file_path` - calea către fișierul text.
#Output: Numărul de cuvinte diferite din text.
def numar_cuvinte_diferite(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    text = text.lower().replace('.', '').replace(',', '').replace('!', '').replace('?', '').replace(':', '').replace(';', '')
    cuvinte = text.split()
    cuvinte_unice = set(cuvinte)
    return len(cuvinte_unice)

#Descriere: Gaseste cel mai scurt si cel mai lung cuvant dintr-un fisier text.
#Input: `file_path` - calea către fișierul text.
#Output:
#`cel_mai_scurt` - cel mai scurt cuvânt din text.
# `cel_mai_lung` - cel mai lung cuvânt din text.
def cel_mai_scurt_si_lung_cuvant(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    text = text.lower().replace('.', '').replace(',', '').replace('!', '').replace('?', '').replace(':', '').replace(';', '')
    cuvinte = text.split()

    cel_mai_scurt = min(cuvinte, key=len)
    cel_mai_lung = max(cuvinte, key=len)
    return cel_mai_scurt, cel_mai_lung


#solutie 100% copilot
def elimina_diacritice(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    text_fara_diacritice = ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))
    return text_fara_diacritice

#solutia mea :)
#def elimina_diacritice(text):
#    rezultat = ""
#    for caracter in text:
#        if caracter == 'ă' or caracter == 'â':
#            rezultat += 'a'
#        elif caracter == 'î':
#            rezultat += 'i'
#        elif caracter == 'ș':
#            rezultat += 's'
#        elif caracter == 'ț':
#            rezultat += 't'
#        elif caracter == 'Ă' or caracter == 'Â':
#            rezultat += 'A'
#        elif caracter == 'Î':
#            rezultat += 'I'
#        elif caracter == 'Ș':
#            rezultat += 'S'
#        elif caracter == 'Ț':
#            rezultat += 'T'
#        else:
#            rezultat += caracter
#    return rezultat
#
#def elimina_diacritice_din_fisier(file_path):
#    with open(file_path, 'r', encoding='utf-8') as file:
#        text = file.read()
#
#    return elimina_diacritice(text)


#Descriere: Elimină repetițiile de litere dintr-un cuvânt, păstrând maximum două apariții consecutive ale aceleiași litere.
#Input: `cuvant` - cuvântul din care se elimină repetițiile.
#Output: Cuvântul fără repetiții excesive.
def elimina_repetitii(cuvant):
    rezultat = []
    count = 1
    for i in range(1, len(cuvant)):
        if cuvant[i] == cuvant[i - 1]:
            count += 1
            if count <= 2:
                rezultat.append(cuvant[i])
        else:
            count = 1
            rezultat.append(cuvant[i])
    return cuvant[0] + ''.join(rezultat)


file_path = 'data/texts.txt'
numar = numar_propozitii(file_path)
print(f"Numărul de propoziții din text este: {numar}")

numar = numar_cuvinte(file_path)
print(f"Numărul de cuvinte din text este: {numar}")

numar_unic = numar_cuvinte_diferite(file_path)
print(f"Numărul de cuvinte diferite din text este: {numar_unic}")

cel_mai_scurt, cel_mai_lung = cel_mai_scurt_si_lung_cuvant(file_path)
print(f"Cel mai scurt cuvânt este: {cel_mai_scurt}")
print(f"Cel mai lung cuvânt este: {cel_mai_lung}")

text_fara_diacritice = elimina_diacritice(file_path)
print(text_fara_diacritice)

cel_mai_lung = elimina_repetitii(cel_mai_lung)
url = f"https://dexonline.ro/definitie/{cel_mai_lung}"
webbrowser.open(url)
