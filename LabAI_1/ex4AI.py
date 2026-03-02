from collections import Counter


def cuvinte_unice(text):
    # Împărțim textul în cuvinte și le numărăm
    cuvinte = text.split()
    frecventa = Counter(cuvinte)

    # Extragem cuvintele care apar exact o singură dată
    cuvinte_unice = [cuvant for cuvant, count in frecventa.items() if count == 1]

    return cuvinte_unice


# Exemplu de utilizare
text = "ana are ana are mere rosii ana"
result = cuvinte_unice(text)
print(result)
