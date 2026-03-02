def find_kth_largest(nums, k):
    """
    Funcția determină al k-lea cel mai mare element dintr-un șir de numere distincte.

    :param nums: lista de numere
    :param k: indexul elementului căutat (k < n)
    :return: al k-lea cel mai mare element din listă
    """
    # Eliminăm duplicatele și sortăm lista descrescător
    nums_sorted = sorted(set(nums), reverse=True)

    # Returnăm elementul de la poziția k-1
    return nums_sorted[k - 1]


# Citirea datelor de la tastatură
n = int(input("Introduceti numarul de elemente: "))
nums = []
for _ in range(n):
    num = int(input("Introduceti un numar: "))
    nums.append(num)

k = int(input("Introduceti valoarea k (k < n): "))

# Verificăm dacă k este valid
if k < n:
    kth_largest = find_kth_largest(nums, k)
    print(f"Al {k}-lea cel mai mare element este: {kth_largest}")
else:
    print("Valoarea lui k trebuie să fie mai mică decât n.")
