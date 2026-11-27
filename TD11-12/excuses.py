# Générateur d'excuses aléatoires
# Une excuse = qui + action + quoi
# Exemple : "Mon chat a mangé mon TD."

import random  # module qui permet de choisir des éléments au hasard


# 1) Les listes de mots possibles
qui = ["Mon chat", "Le bus", "Un voisin", "Mon petit frère", "Le prof", "Un extraterrestre"]
action = ["a mangé", "a caché", "a supprimé", "a cassé", "a perdu", "a volé"]
quoi = ["mon ordinateur", "mes clés", "mon TD", "mon cahier", "ma clé USB", "mon réveil"]


# 2) Une fonction qui fabrique une excuse
def generer_excuse():
    # random.choice prend un élément au hasard dans une liste
    sujet = random.choice(qui)
    verbe = random.choice(action)
    objet = random.choice(quoi)

    # On colle les 3 morceaux pour faire une phrase
    excuse = sujet + " " + verbe + " " + objet + "."
    return excuse


# 3) Le programme principal
print("=== Générateur d'excuses ===")

continuer = "o"
while continuer == "o":
    print()
    print("Excuse :", generer_excuse())
    print()
    continuer = input("Une autre excuse ? (o/n) : ")
    continuer = continuer.strip().lower()  # enlève les espaces et met en minuscule

print("Bon courage !")
