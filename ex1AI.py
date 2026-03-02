"""Date de intrare:
Un șir de caractere care conține mai multe cuvinte separate prin spații.
Date de ieșire:
Un șir de caractere care reprezintă ultimul cuvânt din punct de vedere alfabetic.

"""


text = input("Introduceți textul: ")
cuvinte = text.split()  # Separăm cuvintele după spațiu
ultimul_cuvant = max(cuvinte)  # Determinăm ultimul cuvânt dpdv alfabetic
print("Ultimul cuvânt alfabetic este:", ultimul_cuvant)
