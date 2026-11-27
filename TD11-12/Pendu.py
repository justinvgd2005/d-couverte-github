"""Jeu du pendu - interface graphique avec Tkinter.

Lancer le jeu :  python Pendu.py

Organisation du projet :
    mots.py          -> les mots par catégorie et les niveaux de difficulté
    logique_pendu.py -> les règles du jeu (sans affichage)
    Pendu.py         -> l'interface graphique (ce fichier)
"""

import string
import tkinter as tk

from logique_pendu import (
    ERREURS_MAX, INVALIDE, DEJA_PROPOSEE, CORRECTE,
    PartiePendu, choisir_mot,
)
from mots import CATEGORIES, DIFFICULTES

# ---------------------------------------------------------------------------
# Constantes d'apparence (toutes regroupées ici pour les modifier facilement)
# ---------------------------------------------------------------------------
COULEUR_FOND = "#1e1e2e"
COULEUR_TEXTE = "#f5f5f5"
COULEUR_SECONDAIRE = "#a6a6c0"
COULEUR_ACCENT = "#7c6cf2"
COULEUR_SUCCES = "#4caf7a"
COULEUR_ERREUR = "#e05d5d"
COULEUR_TOUCHE = "#3a3a55"

POLICE = "Segoe UI"
POLICE_MOT = "Consolas"  # police à chasse fixe : toutes les lettres ont la même largeur

POINTS_VICTOIRE = 10

# ---------------------------------------------------------------------------
# Dessin du pendu
# Chaque forme est un couple (type, coordonnées). Décrire le dessin par des
# données évite d'écrire 7 fonctions de dessin presque identiques.
# ---------------------------------------------------------------------------
# Une étape par erreur : l'étape n°1 est dessinée à la 1re erreur, etc.
# La potence se construit d'abord, puis le bonhomme apparaît.
ETAPES_POTENCE = [
    [("ligne", (20, 265, 180, 265))],                       # 1 : sol
    [("ligne", (60, 265, 60, 20))],                         # 2 : poteau
    [("ligne", (60, 20, 150, 20)), ("ligne", (60, 60, 100, 20))],  # 3 : traverse + renfort
    [("ligne", (150, 20, 150, 50))],                        # 4 : corde
]
ETAPES_BONHOMME = [
    [("cercle", (130, 50, 170, 90))],                       # 5 : tête
    [("ligne", (150, 90, 150, 170))],                       # 6 : corps
    [("ligne", (150, 110, 120, 145))],                      # 7 : bras gauche
    [("ligne", (150, 110, 180, 145))],                      # 8 : bras droit
    [("ligne", (150, 170, 125, 215))],                      # 9 : jambe gauche
    [("ligne", (150, 170, 175, 215))],                      # 10 : jambe droite
    [("ligne", (138, 62, 146, 70)), ("ligne", (146, 62, 138, 70)),
     ("ligne", (154, 62, 162, 70)), ("ligne", (162, 62, 154, 70))],  # 11 : yeux en croix
]
ETAPES_PENDU = ETAPES_POTENCE + ETAPES_BONHOMME

# Sécurité : il faut exactement une étape de dessin par erreur possible
assert len(ETAPES_PENDU) == ERREURS_MAX, "ETAPES_PENDU et ERREURS_MAX ne correspondent pas"


class ApplicationPendu:
    """Fenêtre du jeu : écran d'accueil + écran de jeu."""

    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("Jeu du pendu")
        self.fenetre.configure(bg=COULEUR_FOND)
        self.fenetre.resizable(False, False)

        # État du jeu
        self.partie = None
        self.score = 0
        self.victoires = 0
        self.parties_jouees = 0
        self.difficulte = tk.StringVar(value="Moyen")
        self.boutons_lettres = {}  # lettre -> bouton du clavier virtuel

        # Construction des deux écrans
        self.ecran_accueil = self.creer_ecran_accueil()
        self.ecran_jeu = self.creer_ecran_jeu()
        self.ecran_actif = None
        self.fixer_taille_fenetre()
        self.afficher_ecran(self.ecran_accueil)

        # Le clavier physique fonctionne aussi
        self.fenetre.bind("<Key>", self.gerer_touche_clavier)

    # ------------------------------------------------------------------
    # Petits outils réutilisables (évitent de répéter le même code)
    # ------------------------------------------------------------------
    def creer_label(self, parent, texte="", taille=12, couleur=COULEUR_TEXTE,
                    gras=False, police=POLICE):
        style = "bold" if gras else "normal"
        return tk.Label(parent, text=texte, font=(police, taille, style),
                        fg=couleur, bg=COULEUR_FOND)

    def creer_bouton(self, parent, texte, commande, couleur=COULEUR_ACCENT,
                     taille=13, largeur=None):
        return tk.Button(parent, text=texte, command=commande, width=largeur,
                         font=(POLICE, taille, "bold"), fg=COULEUR_TEXTE,
                         bg=couleur, activebackground=COULEUR_SECONDAIRE,
                         activeforeground=COULEUR_FOND, relief="flat",
                         cursor="hand2", padx=12, pady=6,
                         disabledforeground=COULEUR_TEXTE)

    def texte_score(self):
        return (f"Score : {self.score} pts   |   "
                f"Victoires : {self.victoires} / {self.parties_jouees}")

    def fixer_taille_fenetre(self):
        """Donne à la fenêtre une taille fixe, assez grande pour tout afficher.

        Plutôt que d'écrire une taille "en dur" (qui dépend de l'écran et du
        zoom Windows), on demande à Tkinter la place nécessaire, en prévoyant
        le mot le plus long possible et un long message.
        """
        mot_le_plus_long = max((mot for mots in CATEGORIES.values() for mot in mots), key=len)
        self.label_mot.configure(text=" ".join(mot_le_plus_long))
        self.label_message.configure(text="Saisie invalide : tape une lettre de A à Z.")
        self.label_infos.configure(text="Catégorie : Informatique   |   Difficulté : Difficile")
        self.label_score_jeu.configure(text=self.texte_score() + "000")

        self.fenetre.update_idletasks()  # calcule la taille des éléments
        largeur = max(self.ecran_accueil.winfo_reqwidth(), self.ecran_jeu.winfo_reqwidth())
        hauteur = max(self.ecran_accueil.winfo_reqheight(), self.ecran_jeu.winfo_reqheight())
        # + marges utilisées dans afficher_ecran (padx=20, pady=15 de chaque côté)
        self.fenetre.geometry(f"{largeur + 40}x{hauteur + 30}")

    def afficher_ecran(self, ecran):
        """Cache l'écran actuel et affiche celui demandé."""
        if self.ecran_actif is not None:
            self.ecran_actif.pack_forget()
        ecran.pack(fill="both", expand=True, padx=20, pady=15)
        self.ecran_actif = ecran

    # ------------------------------------------------------------------
    # Écran d'accueil
    # ------------------------------------------------------------------
    def creer_ecran_accueil(self):
        ecran = tk.Frame(self.fenetre, bg=COULEUR_FOND)

        self.creer_label(ecran, "JEU DU PENDU", taille=40, gras=True,
                         couleur=COULEUR_ACCENT).pack(pady=(90, 5))
        self.creer_label(ecran, "Retrouve le mot caché avant d'être pendu !",
                         taille=13, couleur=COULEUR_SECONDAIRE).pack(pady=(0, 50))

        self.creer_label(ecran, "Choisis la difficulté :", taille=14).pack(pady=(0, 10))

        # Un bouton radio par niveau, créé automatiquement à partir de DIFFICULTES
        cadre_niveaux = tk.Frame(ecran, bg=COULEUR_FOND)
        cadre_niveaux.pack()
        for niveau, (longueur_min, longueur_max) in DIFFICULTES.items():
            if longueur_max > 15:
                description = f"{longueur_min}+ lettres"
            else:
                description = f"{longueur_min} à {longueur_max} lettres"
            tk.Radiobutton(
                cadre_niveaux, text=f"{niveau}\n{description}", value=niveau,
                variable=self.difficulte, indicatoron=False, width=14,
                font=(POLICE, 12, "bold"), fg=COULEUR_TEXTE, bg=COULEUR_TOUCHE,
                selectcolor=COULEUR_ACCENT, activebackground=COULEUR_SECONDAIRE,
                relief="flat", cursor="hand2", pady=8,
            ).pack(side="left", padx=8)

        self.creer_bouton(ecran, "Nouvelle partie", self.nouvelle_partie,
                          taille=16).pack(pady=45)

        self.label_score_accueil = self.creer_label(
            ecran, self.texte_score(), couleur=COULEUR_SECONDAIRE)
        self.label_score_accueil.pack()

        return ecran

    # ------------------------------------------------------------------
    # Écran de jeu
    # ------------------------------------------------------------------
    def creer_ecran_jeu(self):
        ecran = tk.Frame(self.fenetre, bg=COULEUR_FOND)

        # --- Barre du haut : catégorie / difficulté à gauche, score à droite
        barre_haut = tk.Frame(ecran, bg=COULEUR_FOND)
        barre_haut.pack(fill="x")
        self.label_infos = self.creer_label(barre_haut, taille=13, gras=True)
        self.label_infos.pack(side="left")
        self.label_score_jeu = self.creer_label(barre_haut, couleur=COULEUR_SECONDAIRE)
        self.label_score_jeu.pack(side="right")

        # --- Zone centrale : dessin à gauche, informations à droite
        zone_centrale = tk.Frame(ecran, bg=COULEUR_FOND)
        zone_centrale.pack(fill="x", pady=10)

        self.canvas = tk.Canvas(zone_centrale, width=200, height=280,
                                bg=COULEUR_FOND, highlightthickness=0)
        self.canvas.pack(side="left", padx=(20, 40))

        colonne_infos = tk.Frame(zone_centrale, bg=COULEUR_FOND)
        colonne_infos.pack(side="left", fill="both", expand=True)

        self.label_erreurs = self.creer_label(colonne_infos, taille=16, gras=True)
        self.label_erreurs.pack(anchor="w", pady=(40, 15))

        self.creer_label(colonne_infos, "Lettres déjà proposées :",
                         couleur=COULEUR_SECONDAIRE).pack(anchor="w")
        self.label_lettres = self.creer_label(colonne_infos, taille=14,
                                              police=POLICE_MOT)
        self.label_lettres.pack(anchor="w", pady=(0, 25))

        self.label_message = self.creer_label(colonne_infos, taille=15, gras=True)
        self.label_message.configure(wraplength=480, justify="left")
        self.label_message.pack(anchor="w")

        # --- Le mot à deviner
        self.label_mot = self.creer_label(ecran, taille=30, gras=True,
                                          police=POLICE_MOT)
        self.label_mot.pack(pady=(5, 15))

        # --- Clavier virtuel : 2 lignes de 13 lettres
        clavier = tk.Frame(ecran, bg=COULEUR_FOND)
        clavier.pack()
        for position, lettre in enumerate(string.ascii_uppercase):
            # "lambda l=lettre" fige la lettre de CE bouton (sinon tous
            # les boutons utiliseraient la dernière lettre de la boucle : Z)
            bouton = self.creer_bouton(clavier, lettre,
                                       lambda l=lettre: self.jouer_lettre(l),
                                       couleur=COULEUR_TOUCHE, taille=12, largeur=2)
            bouton.grid(row=position // 13, column=position % 13, padx=3, pady=3)
            self.boutons_lettres[lettre] = bouton

        # --- Boutons du bas
        barre_bas = tk.Frame(ecran, bg=COULEUR_FOND)
        barre_bas.pack(pady=20)
        self.bouton_rejouer = self.creer_bouton(barre_bas, "Recommencer",
                                                self.nouvelle_partie)
        self.bouton_rejouer.pack(side="left", padx=10)
        self.creer_bouton(barre_bas, "Menu", self.retour_menu,
                          couleur=COULEUR_TOUCHE).pack(side="left", padx=10)

        return ecran

    # ------------------------------------------------------------------
    # Déroulement d'une partie
    # ------------------------------------------------------------------
    def nouvelle_partie(self):
        """Tire un nouveau mot et remet l'écran de jeu à zéro."""
        categorie, mot = choisir_mot(self.difficulte.get())
        self.partie = PartiePendu(mot, categorie)

        for bouton in self.boutons_lettres.values():
            bouton.configure(state="normal", bg=COULEUR_TOUCHE)

        self.label_infos.configure(
            text=f"Catégorie : {categorie}   |   Difficulté : {self.difficulte.get()}")
        self.label_mot.configure(fg=COULEUR_TEXTE)
        self.afficher_message("Choisis une lettre (clic ou clavier).", COULEUR_SECONDAIRE)
        self.bouton_rejouer.configure(text="Recommencer")

        self.mettre_a_jour_affichage()
        self.afficher_ecran(self.ecran_jeu)

    def jouer_lettre(self, saisie):
        """Appelée par le clavier virtuel ET par le clavier physique."""
        if self.partie is None or self.partie.est_terminee():
            return

        resultat = self.partie.proposer_lettre(saisie)
        lettre = saisie.upper()

        if resultat == INVALIDE:
            self.afficher_message("Saisie invalide : tape une lettre de A à Z.",
                                  COULEUR_ERREUR)
            return
        if resultat == DEJA_PROPOSEE:
            self.afficher_message(f"Tu as déjà proposé la lettre {lettre} !",
                                  COULEUR_ERREUR)
            return

        # La lettre est nouvelle : on colore et désactive sa touche
        if resultat == CORRECTE:
            couleur = COULEUR_SUCCES
            self.afficher_message(f"Bien joué, {lettre} est dans le mot !", COULEUR_SUCCES)
        else:  # INCORRECTE
            couleur = COULEUR_ERREUR
            self.afficher_message(f"Raté, {lettre} n'est pas dans le mot.", COULEUR_ERREUR)
        self.boutons_lettres[lettre].configure(state="disabled", bg=couleur)

        self.mettre_a_jour_affichage()
        if self.partie.est_terminee():
            self.terminer_partie()

    def terminer_partie(self):
        """Affiche le résultat, révèle le mot et met à jour le score."""
        self.parties_jouees += 1

        if self.partie.est_gagnee():
            self.score += POINTS_VICTOIRE
            self.victoires += 1
            self.afficher_message(f"VICTOIRE ! +{POINTS_VICTOIRE} points",
                                  COULEUR_SUCCES)
            couleur_mot = COULEUR_SUCCES
        else:
            self.afficher_message(f"PERDU ! Le mot était : {self.partie.mot}",
                                  COULEUR_ERREUR)
            couleur_mot = COULEUR_ERREUR

        # Révélation du mot complet (lettres séparées par des espaces)
        self.label_mot.configure(text=" ".join(self.partie.mot), fg=couleur_mot)

        # Plus aucune lettre ne peut être jouée
        for bouton in self.boutons_lettres.values():
            bouton.configure(state="disabled")

        self.bouton_rejouer.configure(text="Rejouer")
        self.mettre_a_jour_score()

    def retour_menu(self):
        self.mettre_a_jour_score()
        self.afficher_ecran(self.ecran_accueil)

    def gerer_touche_clavier(self, evenement):
        """Transmet les touches du clavier physique au jeu (écran de jeu seulement)."""
        if self.ecran_actif is not self.ecran_jeu:
            return
        # Les touches sans caractère visible (Maj, Ctrl, flèches...) sont ignorées
        if not evenement.char or not evenement.char.isprintable():
            return
        self.jouer_lettre(evenement.char)

    # ------------------------------------------------------------------
    # Mise à jour de l'affichage
    # ------------------------------------------------------------------
    def afficher_message(self, texte, couleur):
        self.label_message.configure(text=texte, fg=couleur)

    def mettre_a_jour_score(self):
        self.label_score_jeu.configure(text=self.texte_score())
        self.label_score_accueil.configure(text=self.texte_score())

    def mettre_a_jour_affichage(self):
        """Redessine tout ce qui dépend de l'état de la partie."""
        self.label_mot.configure(text=self.partie.mot_affiche())

        restantes = self.partie.erreurs_restantes()
        couleur = COULEUR_ERREUR if restantes <= 2 else COULEUR_TEXTE
        self.label_erreurs.configure(
            text=f"Erreurs restantes : {restantes} / {ERREURS_MAX}", fg=couleur)

        lettres = self.partie.lettres_proposees
        self.label_lettres.configure(text=" ".join(lettres) if lettres else "aucune")

        self.dessiner_pendu()
        self.mettre_a_jour_score()

    def dessiner_formes(self, formes, couleur):
        """Dessine une liste de formes (lignes ou cercles) sur le canvas."""
        for type_forme, coordonnees in formes:
            if type_forme == "cercle":
                self.canvas.create_oval(*coordonnees, outline=couleur, width=4)
            else:
                self.canvas.create_line(*coordonnees, fill=couleur, width=4,
                                        capstyle="round")

    def dessiner_pendu(self):
        """Efface le canvas puis dessine une étape par erreur commise."""
        self.canvas.delete("all")

        couleur_bonhomme = COULEUR_ERREUR if self.partie.est_perdue() else COULEUR_TEXTE
        for numero, etape in enumerate(ETAPES_PENDU[:self.partie.nb_erreurs]):
            # La potence en gris, le bonhomme en blanc (ou rouge si perdu)
            if numero < len(ETAPES_POTENCE):
                couleur = COULEUR_SECONDAIRE
            else:
                couleur = couleur_bonhomme
            self.dessiner_formes(etape, couleur)


def main():
    fenetre = tk.Tk()
    ApplicationPendu(fenetre)
    fenetre.mainloop()


# Ce bloc n'est exécuté que si on lance directement "python Pendu.py"
if __name__ == "__main__":
    main()
