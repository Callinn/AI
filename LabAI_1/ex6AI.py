from collections import defaultdict


def find_majority_element(arr):
    n = len(arr)

    # Faza 1: găsirea unui candidat pentru elementul majoritar folosind Boyer-Moore
    candidate, count = None, 0
    for num in arr:
        if count == 0:
            candidate, count = num, 1
        elif num == candidate:
            count += 1
        else:
            count -= 1

    # Faza 2: Verificarea dacă candidatul este într-adevăr majoritar
    count = 0
    for num in arr:
        if num == candidate:
            count += 1
    return candidate if count > n // 2 else None


# Exemplu de utilizare
arr = [2, 8, 7, 2, 2, 5, 2, 3, 1, 2, 2]
print(find_majority_element(arr))  # Output: 2
