from fonction import (
    lire_graphe_sans_cout,
    lire_graphe_avec_cout,
    afficher_matrice,
    afficher_matrice_flot,
    ford_fulkerson,
    pousser_reetiquer,
    flot_cout_minimal
)

def menu():
    print("===== DÉMO INTERACTIVE - PROBLÈMES DE FLOT =====")
    while True:
        try:
            numero = int(input("Numéro du problème à traiter (1 à 10, 0 pour quitter) : "))
            if numero == 0:
                break
            elif 1 <= numero <= 5:
                algo = input("Choisir l’algorithme (FF pour Ford-Fulkerson, PR pour Pousser-Réétiqueter) : ").strip().upper()
                fichier = f"prop{numero}.txt"
                n, capacites = lire_graphe_sans_cout(fichier)
                s = 0
                t = n - 1
                print(f"\nProblème {numero} — Capacités :")
                afficher_matrice(capacites)
                if algo == "FF":
                    ford_fulkerson(capacites, s, t, afficher=True)
                elif algo == "PR":
                    pousser_reetiquer(capacites, s, t, afficher=True)
                else:
                    print("Algorithme non reconnu.")
            elif 6 <= numero <= 10:
                fichier = f"prop{numero}.txt"
                n, capacites, couts = lire_graphe_avec_cout(fichier)
                s = 0
                t = n - 1
                print(f"\nProblème {numero} — Capacités :")
                afficher_matrice(capacites)
                print(f"\nCoûts :")
                afficher_matrice(couts)
                flot = int(input("Entrer la valeur du flot à envoyer : "))
                total_cout, flots = flot_cout_minimal(capacites, couts, s, t, flot, afficher=True)
                afficher_matrice_flot(flots, capacites, "Affichage du flot")
                print(f"\nValeur du flot demandé : {flot}")
                print(f"Coût total : {total_cout}")
            else:
                print("Numéro de problème invalide.")
        except Exception as e:
            print(f"Erreur : {e}")
        print("\n----------------------------------------\n")

if __name__ == "__main__":
    menu()
