from collections import deque
def nom_sommet(i, n):
    if i == 0:
        return 's'
    elif i == n - 1:
        return 't'
    else:
        return chr(ord('a') + i - 1)  # a, b, c, ...

def bfs_augmentant(capacites, flots, s, t, parents):
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


def afficher_parcours(parents, s, n):
    chemins_parents = []
    for i in range(n):
        if parents[i] != -1 and i != s:
            chemins_parents.append(f"Π({nom_sommet(i, n)}) = {nom_sommet(parents[i], n)}")
    print(" ; ".join(chemins_parents))

def graphe_residuel(capacites, flots):
    n = len(capacites)
    return [[capacites[i][j] - flots[i][j] for j in range(n)] for i in range(n)]