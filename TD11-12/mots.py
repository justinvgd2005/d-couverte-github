"""Données du jeu du pendu : les mots par catégorie et les niveaux de difficulté.

Les mots sont écrits en MAJUSCULES et SANS ACCENTS pour que le joueur
n'ait que les 26 lettres de A à Z à utiliser.
"""

# Dictionnaire : nom de la catégorie -> liste de mots
CATEGORIES = {
    "Informatique": [
        "CODE", "BUG", "PIXEL", "OCTET", "ECRAN", "SOURIS", "PYTHON", "BOUCLE",
        "CLAVIER", "SERVEUR", "LOGICIEL", "FONCTION", "VARIABLE", "INTERNET",
        "ALGORITHME", "PROCESSEUR", "ORDINATEUR", "COMPILATEUR",
        "INFORMATIQUE", "PROGRAMMATION",
    ],
    "Animaux": [
        "CHAT", "LION", "TIGRE", "ZEBRE", "LAPIN", "CHEVAL", "GIRAFE",
        "DAUPHIN", "ELEPHANT", "PANTHERE", "PINGOUIN", "KANGOUROU", "CROCODILE",
        "RHINOCEROS", "SALAMANDRE", "HIPPOPOTAME", "ORNITHORYNQUE",
    ],
    "Pays": [
        "INDE", "CHILI", "PEROU", "JAPON", "CHINE", "FRANCE", "CANADA",
        "ESPAGNE", "MEXIQUE", "BELGIQUE", "PORTUGAL", "ALLEMAGNE", "AUSTRALIE",
        "MADAGASCAR", "MOZAMBIQUE", "PHILIPPINES", "AFGHANISTAN",
    ],
    "Sport": [
        "JUDO", "BOXE", "GOLF", "RUGBY", "TENNIS", "KARATE", "ESCRIME",
        "FOOTBALL", "HANDBALL", "CYCLISME", "NATATION", "BADMINTON",
        "BASKETBALL", "VOLLEYBALL", "ATHLETISME", "EQUITATION", "GYMNASTIQUE",
    ],
}

# Niveau de difficulté -> (longueur minimale, longueur maximale) du mot
DIFFICULTES = {
    "Facile": (3, 6),
    "Moyen": (7, 9),
    "Difficile": (10, 30),
}
