import time
import os

import random
from fonction import *
from generationGraphe import generer_graphe

def mesurer_temps(n, nb_tests=100):
    temps_ff = []
    temps_pr = []
    temps_min = []

    for test in range(nb_tests):
        # Générer un graphe aléatoire
        capacites, couts = generer_graphe(n)
        s = 0
        t = n - 1

        # ----- Ford-Fulkerson -----
        flots_ff = [[0] * n for _ in range(n)]
        parents = [-1] * n
        start = time.perf_counter()
        ford_fulkerson(capacites, s, t, afficher=False)
        end = time.perf_counter()
        temps_ff.append(end - start)

        # ----- Pousser-Réétiqueter -----
        start = time.perf_counter()
        pousser_reetiquer(capacites, s, t, afficher=False)
        end = time.perf_counter()
        temps_pr.append(end - start)

        # ----- Flot à coût minimal -----
        flot_demande = 5  # valeur arbitraire fixe pour simplifier
        start = time.perf_counter()
        flot_cout_minimal(capacites, couts, s, t, flot_demande, afficher=False)
        end = time.perf_counter()
        temps_min.append(end - start)

        if test % 10 == 0:
            print(f"Test {test} terminé pour n={n}")

    return temps_ff, temps_pr, temps_min

def main():
    tailles = [10, 20, 40, 100, 400]  # (attention : 4000, 10000 = très long)
    nb_tests = 100

    resultats = {}

    for n in tailles:
        print(f"\n=== Traitement pour n = {n} ===")
        ff, pr, min_ = mesurer_temps(n, nb_tests=nb_tests)
        resultats[n] = {
            "FF": ff,
            "PR": pr,
            "MIN": min_
        }

    # Sauvegarde brute (exemple simple)
    with open("resultats_complexite.txt", "w") as f:
        for n in resultats:
            f.write(f"n={n}\n")
            f.write(f"FF : {resultats[n]['FF']}\n")
            f.write(f"PR : {resultats[n]['PR']}\n")
            f.write(f"MIN : {resultats[n]['MIN']}\n")
            f.write("\n")

if __name__ == "__main__":
    main()
