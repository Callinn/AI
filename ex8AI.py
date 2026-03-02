from collections import deque
"""8.Să se genereze toate numerele (în reprezentare binară) cuprinse între 1 și n. De ex. dacă n = 4, numerele sunt: 1, 10, 11, 100.

"""
# Citirea valorii n de la tastatură
n = int(input("Introduceți un număr întreg n: "))

# Inițializăm o coadă cu primul număr binar
queue = deque(["1"])

# Generăm și afișăm n numere binare
for _ in range(n):
    # Scoatem elementul din coadă
    current = queue.popleft()
    print(current)
    # Adăugăm la coadă următoarele două numere binare
    queue.append(current + "0")
    queue.append(current + "1")
