"""Logique du jeu du pendu.

Ce fichier ne contient AUCUN affichage : uniquement les règles du jeu.
On peut donc le tester sans ouvrir de fenêtre.
"""

import random
import string

from mots import CATEGORIES, DIFFICULTES

ERREURS_MAX = 11  # 4 étapes pour la potence + 7 pour le bonhomme

# Résultats possibles quand le joueur propose une lettre
INVALIDE = "invalide"                # ce n'est pas une lettre de A à Z
DEJA_PROPOSEE = "deja_proposee"      # la lettre a déjà été jouée
CORRECTE = "correcte"                # la lettre est dans le mot
INCORRECTE = "incorrecte"            # la lettre n'est pas dans le mot
PARTIE_TERMINEE = "partie_terminee"  # la partie est finie, on ne joue plus


def choisir_mot(difficulte):
    """Choisit au hasard une catégorie, puis un mot adapté à la difficulté.

    Renvoie un couple (categorie, mot).
    """
    longueur_min, longueur_max = DIFFICULTES[difficulte]

    # On garde, pour chaque catégorie, seulement les mots de la bonne longueur
    mots_par_categorie = {}
    for categorie, mots in CATEGORIES.items():
        mots_valides = [mot for mot in mots if longueur_min <= len(mot) <= longueur_max]
        if mots_valides:  # on ignore une catégorie qui n'aurait aucun mot valide
            mots_par_categorie[categorie] = mots_valides

    categorie = random.choice(list(mots_par_categorie))
    mot = random.choice(mots_par_categorie[categorie])
    return categorie, mot


class PartiePendu:
    """Représente UNE partie de pendu : le mot, les lettres jouées, les erreurs."""

    def __init__(self, mot, categorie):
        self.mot = mot.upper()
        self.categorie = categorie
        self.lettres_proposees = []  # une liste pour garder l'ordre des propositions
        self.nb_erreurs = 0

    def proposer_lettre(self, saisie):
        """Traite une lettre proposée par le joueur et renvoie le résultat."""
        if self.est_terminee():
            return PARTIE_TERMINEE

        # .upper() : "a" et "A" sont traités de la même façon
        lettre = saisie.strip().upper()

        # On n'accepte qu'un seul caractère, compris entre A et Z
        if len(lettre) != 1 or lettre not in string.ascii_uppercase:
            return INVALIDE

        if lettre in self.lettres_proposees:
            return DEJA_PROPOSEE

        self.lettres_proposees.append(lettre)

        if lettre in self.mot:
            return CORRECTE

        self.nb_erreurs += 1
        return INCORRECTE

    def mot_affiche(self):
        """Renvoie le mot avec des tirets pour les lettres pas encore trouvées.

        Exemple : mot "PYTHON", lettres jouées P et O  ->  "P _ _ _ O _"
        """
        lettres_affichees = []
        for lettre in self.mot:
            if lettre in self.lettres_proposees:
                lettres_affichees.append(lettre)
            else:
                lettres_affichees.append("_")
        return " ".join(lettres_affichees)

    def erreurs_restantes(self):
        return ERREURS_MAX - self.nb_erreurs

    def est_gagnee(self):
        """Gagné si TOUTES les lettres du mot ont été proposées."""
        for lettre in self.mot:
            if lettre not in self.lettres_proposees:
                return False
        return True

    def est_perdue(self):
        return self.nb_erreurs >= ERREURS_MAX

    def est_terminee(self):
        return self.est_gagnee() or self.est_perdue()
