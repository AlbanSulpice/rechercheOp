import os
from collections import deque

def lire_graphe_sans_cout(nom_fichier):
    chemin = os.path.join("..", "prop", nom_fichier)
    with open(chemin, 'r') as f:
        lignes = f.readlines()

    n = int(lignes[0])
    capacites = [list(map(int, lignes[i + 1].split())) for i in range(n)]

    return n, capacites

def lire_graphe_avec_cout(nom_fichier):
    chemin = os.path.join("..", "prop", nom_fichier)
    with open(chemin, 'r') as f:
        lignes = f.readlines()

    n = int(lignes[0])
    capacites = [list(map(int, lignes[i + 1].split())) for i in range(n)]
    couts = [list(map(int, lignes[i + 1 + n].split())) for i in range(n)]

    return n, capacites, couts

def nom_sommet(i, n):
    if i == 0:
        return 's'
    elif i == n - 1:
        return 't'
    else:
        return chr(ord('a') + i - 1)


def afficher_matrice(matrice, titre="Matrice"):
    n = len(matrice)
    print(f"\n{titre} :")
    largeur = max(len(str(elem)) for ligne in matrice for elem in ligne)

    # En-tête
    header = [" "] + [nom_sommet(j, n) for j in range(n)]
    print(" ".join(f"{col:>{largeur}}" for col in header))

    # Lignes
    for i, ligne in enumerate(matrice):
        nom = nom_sommet(i, n)
        print(f"{nom:>{largeur}}", end=" ")
        print(" ".join(f"{val:>{largeur}}" for val in ligne))


def bfs(capacites, flots, s, t, parents):
    n = len(capacites)
    visites = [False] * n
    queue = deque()
    queue.append(s)
    visites[s] = True
    parents[s] = -1

    while queue:
        u = queue.popleft()
        for v in range(n):
            if not visites[v] and capacites[u][v] - flots[u][v] > 0:
                queue.append(v)
                parents[v] = u
                visites[v] = True
                if v == t:
                    return True
    return False

def ford_fulkerson(capacites, s, t, afficher=False):
    n = len(capacites)
    flots = [[0] * n for _ in range(n)]
    parents = [-1] * n
    max_flow = 0
    iteration = 1

    while bfs(capacites, flots, s, t, parents):
        chemin = []
        courant = t
        flot_chemin = float('inf')

        while courant != s:
            u = parents[courant]
            chemin.append((u, courant))
            flot_chemin = min(flot_chemin, capacites[u][courant] - flots[u][courant])
            courant = u
        chemin.reverse()

        for u, v in chemin:
            flots[u][v] += flot_chemin
            flots[v][u] -= flot_chemin

        max_flow += flot_chemin

        if afficher:
            print(f"\n Itération {iteration}")
            chaine_affichable = " → ".join(nom_sommet(u, n) for u, _ in chemin) + f" → {nom_sommet(t, n)}"
            print(f"Chaîne améliorante : {chaine_affichable}")
            print(f"→ Flot possible sur cette chaîne : {flot_chemin}")
            iteration += 1

    return max_flow, flots


def pousser_reetiquer(capacites, s, t, afficher=False):
    n = len(capacites)

    # Initialisation
    flots = [[0] * n for _ in range(n)]
    hauteurs = [0] * n
    exces = [0] * n

    hauteurs[s] = n  # hauteur source = n

    # Saturer les arêtes sortantes de la source
    for v in range(n):
        flots[s][v] = capacites[s][v]
        flots[v][s] = -capacites[s][v]
        exces[v] = capacites[s][v]
    exces[s] = -sum(capacites[s])

    # Liste des sommets à traiter (hors s et t)
    sommets = [i for i in range(n) if i != s and i != t]

    iteration = 1
    while any(exces[v] > 0 for v in sommets):
        for u in sommets:
            if exces[u] > 0:
                # Cherche un voisin v où pousser
                for v in range(n):
                    if capacites[u][v] - flots[u][v] > 0 and hauteurs[u] == hauteurs[v] + 1:
                        delta = min(exces[u], capacites[u][v] - flots[u][v])
                        flots[u][v] += delta
                        flots[v][u] -= delta
                        exces[u] -= delta
                        exces[v] += delta

                        if afficher:
                            print(f"\n Itération {iteration}")
                            print(f"Pousser {delta} de {nom_sommet(u, n)} vers {nom_sommet(v, n)}")
                        iteration += 1
                        break
                else:
                    # Pas de poussée possible → réétiqueter
                    min_hauteur = float('inf')
                    for v in range(n):
                        if capacites[u][v] - flots[u][v] > 0:
                            min_hauteur = min(min_hauteur, hauteurs[v])
                    if min_hauteur < float('inf'):
                        hauteurs[u] = min_hauteur + 1
                        if afficher:
                            print(f"\n Itération {iteration}")
                            print(f"Réétiqueter {nom_sommet(u, n)} à hauteur {hauteurs[u]}")
                        iteration += 1

    max_flow = sum(flots[s][v] for v in range(n))
    return max_flow, flots

def bellman(capacites, couts, flots, s):
    n = len(capacites)
    dist = [float('inf')] * n
    parent = [-1] * n
    dist[s] = 0

    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if capacites[u][v] - flots[u][v] > 0 and dist[v] > dist[u] + couts[u][v]:
                    dist[v] = dist[u] + couts[u][v]
                    parent[v] = u

    return dist, parent

def flot_cout_minimal(capacites, couts, s, t, flot_demande, afficher=False):
    n = len(capacites)
    flots = [[0] * n for _ in range(n)]
    total_cout = 0
    courant_flot = 0
    iteration = 1

    while courant_flot < flot_demande:
        dist, parent = bellman(capacites, couts, flots, s)

        if parent[t] == -1:
            print("Impossible d'envoyer tout le flot demandé")
            break

        # Déterminer le flot maximum possible sur ce chemin
        chemin = []
        v = t
        flot_chemin = float('inf')
        while v != s:
            u = parent[v]
            chemin.append((u, v))
            flot_chemin = min(flot_chemin, capacites[u][v] - flots[u][v])
            v = u
        chemin.reverse()

        # Ne pas envoyer plus que ce qu'il manque
        flot_envoye = min(flot_chemin, flot_demande - courant_flot)

        for u, v in chemin:
            flots[u][v] += flot_envoye
            flots[v][u] -= flot_envoye
            total_cout += flot_envoye * couts[u][v]

        courant_flot += flot_envoye

        if afficher:
            print(f"\n Itération {iteration}")
            chaine_affichable = " → ".join(nom_sommet(u, n) for u, _ in chemin) + f" → {nom_sommet(t, n)}"
            print(f"Chaîne de coût minimal : {chaine_affichable}")
            print(f"→ Flot envoyé sur cette chaîne : {flot_envoye}")
            print(f"→ Coût actuel : {total_cout}")
            iteration += 1

    return total_cout, flots