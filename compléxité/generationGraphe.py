import random

def generer_graphe(n):
    """
    Génère un graphe aléatoire avec :
    - n sommets
    - E(n² / 2) arêtes non nulles
    - Capacités entre 1 et 100
    - Coûts entre 1 et 100
    Retourne deux matrices : capacites, couts
    """
    capacites = [[0 for _ in range(n)] for _ in range(n)]
    couts = [[0 for _ in range(n)] for _ in range(n)]

    nb_aretes = (n * n) // 2  # E(n² / 2)

    # Liste de tous les couples (i, j) avec i ≠ j
    couples = [(i, j) for i in range(n) for j in range(n) if i != j]

    # Choisir nb_aretes couples aléatoires
    aretes_choisies = random.sample(couples, min(nb_aretes, len(couples)))

    for (i, j) in aretes_choisies:
        capacites[i][j] = random.randint(1, 100)
        couts[i][j] = random.randint(1, 100)

    return capacites, couts

def afficher_matrice(matrice, titre="Matrice"):
    n = len(matrice)
    print(f"\n{titre} :")
    for ligne in matrice:
        print(" ".join(f"{val:3}" for val in ligne))

if __name__ == "__main__":
    n = 5  # Test rapide
    cap, cout = generer_graphe(n)
    afficher_matrice(cap, "Capacités")
    afficher_matrice(cout, "Coûts")
