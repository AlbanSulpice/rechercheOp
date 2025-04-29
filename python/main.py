from fonction import lire_graphe_sans_cout, afficher_matrice, ford_fulkerson, pousser_reetiquer, executer_et_sauver_trace

# Traces pour les flots maximaux : prop1 à prop5 avec FF et PR
for i in range(1, 6):
    fichier = f"prop{i}.txt"
    print(f"--- Traitement {fichier} ---")

    n, capacites = lire_graphe_sans_cout(fichier)
    s = 0
    t = n - 1

    # Trace Ford-Fulkerson
    executer_et_sauver_trace(
        f"K3-trace{i}-FF.txt",
        lambda capacites=capacites, i=i: (
            afficher_matrice(capacites, f"Capacités (prop{i})"),
            ford_fulkerson(capacites, s, t, afficher=True)
        )
    )

    # Relecture des données pour PR
    n, capacites = lire_graphe_sans_cout(fichier)

    # Trace Pousser-Réétiqueter
    executer_et_sauver_trace(
        f"K3-trace{i}-PR.txt",
        lambda capacites=capacites, i=i: (
            afficher_matrice(capacites, f"Capacités (prop{i})"),
            pousser_reetiquer(capacites, s, t, afficher=True)
        )
    )
