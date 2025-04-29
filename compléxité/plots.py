import matplotlib
matplotlib.use("TkAgg")  # ou "Qt5Agg" si problème
import matplotlib.pyplot as plt
import os
os.makedirs("plots", exist_ok=True)

def charger_resultats(fichier):
    resultats = {}
    with open(fichier, "r") as f:
        lignes = f.readlines()
        n = None
        for ligne in lignes:
            ligne = ligne.strip()
            if ligne.startswith("n="):
                n = int(ligne[2:])
                resultats[n] = {}
            elif ligne.startswith("FF"):
                resultats[n]["FF"] = eval(ligne[4:])
            elif ligne.startswith("PR"):
                resultats[n]["PR"] = eval(ligne[4:])
            elif ligne.startswith("MIN"):
                resultats[n]["MIN"] = eval(ligne[5:])
    return resultats

def tracer_nuage(resultats, algo, couleur):
    plt.figure(figsize=(10, 6))
    for n in sorted(resultats):
        y = resultats[n][algo]
        x = [n] * len(y)
        plt.scatter(x, y, label=f"n={n}", alpha=0.4, color=couleur, s=10)
    plt.xlabel("Taille du graphe (n)")
    plt.ylabel(f"Temps d'exécution ({algo})")
    plt.title(f"Nuage de points pour {algo}")
    plt.grid(True)
    plt.savefig(f"plots/nuage_{algo}.png")


def tracer_courbe_max(resultats, algo, couleur):
    x = []
    y = []
    for n in sorted(resultats):
        x.append(n)
        y.append(max(resultats[n][algo]))
    plt.plot(x, y, label=f"{algo} (max)", marker="o", color=couleur)

def tracer_complexite_pire_cas(resultats):
    n_vals = sorted(resultats.keys())
    ff_max = [max(resultats[n]["FF"]) for n in n_vals]
    pr_max = [max(resultats[n]["PR"]) for n in n_vals]
    min_max = [max(resultats[n]["MIN"]) for n in n_vals]

    plt.figure(figsize=(10, 6))
    plt.plot(n_vals, ff_max, label="θFF(n)", marker="o", color="blue")
    plt.plot(n_vals, pr_max, label="θPR(n)", marker="o", color="green")
    plt.plot(n_vals, min_max, label="θMIN(n)", marker="o", color="red")
    plt.xlabel("Taille du graphe (n)")
    plt.ylabel("Temps d'exécution maximal")
    plt.title("Complexité dans le pire des cas — Enveloppe supérieure")
    plt.legend()
    plt.grid(True)
    plt.savefig("plots/complexite_pire_cas.png")


def tracer_comparaison_ff_pr(resultats):
    n_vals = sorted(resultats.keys())
    ff_max = [max(resultats[n]["FF"]) for n in n_vals]
    pr_max = [max(resultats[n]["PR"]) for n in n_vals]

    plt.figure(figsize=(10, 6))
    plt.plot(n_vals, ff_max, label="θFF(n)", marker="o", color="blue")
    plt.plot(n_vals, pr_max, label="θPR(n)", marker="o", color="green")
    plt.xlabel("Taille du graphe (n)")
    plt.ylabel("Temps d'exécution maximal")
    plt.title("Comparaison des complexités FF vs PR")
    plt.legend()
    plt.grid(True)
    plt.savefig("plots/comparaison_FF_PR.png")

def main():
    resultats = charger_resultats("resultats_complexite.txt")

    os.makedirs("plots", exist_ok=True)

    tracer_nuage(resultats, "FF", "blue")
    tracer_nuage(resultats, "PR", "green")
    tracer_nuage(resultats, "MIN", "red")

    plt.figure(figsize=(10, 6))
    tracer_courbe_max(resultats, "FF", "blue")
    tracer_courbe_max(resultats, "PR", "green")
    tracer_courbe_max(resultats, "MIN", "red")
    plt.xlabel("Taille du graphe (n)")
    plt.ylabel("Temps d'exécution maximal")
    plt.title("Courbes d'enveloppe max (θFF, θPR, θMIN)")
    plt.legend()
    plt.grid(True)
    plt.savefig("plots/courbes_enveloppe_max.png")

    tracer_comparaison_ff_pr(resultats)
    tracer_complexite_pire_cas(resultats)


if __name__ == "__main__":
    main()
