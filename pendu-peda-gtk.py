#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pendu-peda-gtk.py
Jeu du pendu, version pédagogique.
En lien avec les programmes officiels de l'école primaire.
  Source : https://github.com/CyrilleBiot/pendu-peda-gtk
  Source : https://cbiot.fr/

__author__ = "Cyrille BIOT <cyrille@cbiot.fr>"
__copyright__ = "Copyleft"
__credits__ = "Cyrille BIOT <cyrille@cbiot.fr>"
__license__ = "GPL"
__version__ = "0.0.1"
__date__ = "2020/03/03"
__maintainer__ = "Cyrille BIOT <cyrille@cbiot.fr>"
__email__ = "cyrille@cbiot.fr"
__status__ = "Devel"
"""

import os, shutil
from random import choice
from operator import itemgetter
import unicodedata
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class GtkPendu(Gtk.Window):

    def installer_config_locale():
        """
        Installe les fichiers de conf par défaut dans le répertoire de l'user
        afin que celui-ci puisse les incrémenter en fonction de ses besoins
        :return:
        repData : (string). le fichier de conf de l'user lançant le script
        file : (string). le fichier chargé par défaut
        """
        user = os.environ["USER"]
        repertoire = '/home/' + user + '/.primtux/pendu-peda'
        if not os.path.exists(repertoire):
            print("Le repertoire n'existe pas. On le crée.")
            shutil.copytree('/usr/share/pendu-peda/data-files/',
                            '/home/' + user + '/.primtux/pendu-peda/data-files/')
        else:
            print("Le repertoire existe. Configuration OK.")
        repData = '/home/' + user + '/.primtux/pendu-peda/data-files'
        file = 'autre-liste-francais.txt'

        return repData, file

    def creer_matrice(repData):
        """
        Scanne le répertoire de données et réalise le classement des fichiers de config
            - en fonction du niveau (CM / CM / AUTRE)
            - en fonction des thèmes
        S'appuie sur les 3 premières lignes des fichiers de conf
        :return:
            matriceCM, matriceCE, matriceAUTRE
            Type list
            Des listes contenant les tris des fichiers par thèmes et sous entrées
        """
        matrice = []
        matriceCM = []
        matriceCE = []
        matriceAUTRE = []

        # Recuperation des entetes
        for fichiers in os.listdir(repData):
            with open(str(repData) + '/' + str(fichiers)) as f:
                listing = []
                for i in range(3):
                    listing.append(f.readline().strip())
                listing.append(fichiers)
                matrice.append(listing)

        # Creation de 3 listes (une par niveau)
        for i in matrice:
            if 'CM' in (i[0]):
                matriceCM.append(i)
            elif 'CE' in i[0]:
                matriceCE.append(i)
            elif 'AUTRE' in i[0]:
                matriceAUTRE.append(i)
        # Tri de ces listes
        matriceCM = sorted(matriceCM, key=itemgetter(1))
        matriceCE = sorted(matriceCE, key=itemgetter(1))
        matriceAUTRE = sorted(matriceAUTRE, key=itemgetter(1))
        return matriceCM, matriceCE, matriceAUTRE

    def lancement_jeu(self, widget):
        """
        Fonction initialisant le jeu
        :param widget:
        :return:
        """
        self.gestion_bouton('on')


        # Chargement fichier par défaut ou du fichier sélectionné ?
        try:
            self.file
        except NameError:
            print("Chargement du fichier de défaut.")
            self.file = 'autre-liste-francais.txt'
        else:
            print("sure, it was defined : ", self.file)

        # Quelques vriables
        self.jeu_actif = True           # Si nouvelle partie (booleen)
        self.nb_echecs = 0              # Compte le nombre d'échecs (integer)
        self.image_pendu.set_from_file('/usr/share/pendu-peda/images/pendu_0.gif') # Image par défaut


        # Chargement du fichier et choix aléatoire d'un mot
        fichier = open(str(self.repData) + '/' + str(self.file), "r")
        liste_mots = fichier.readlines()
        fichier.close()
        del liste_mots[0:3]  # Nettoyage de l'entete
        self.mot_choisi = choice(liste_mots).rstrip()
        self.mot_choisi = self.mot_choisi.upper()
        self.mot_choisi = ''.join((c for c in unicodedata.normalize('NFD', self.mot_choisi) if unicodedata.category(c) != 'Mn'))

        # Créer d'un mot contenant le même nombre de lettres mais affichant des tirets
        # Mise à jour de son label
        self.mot_tiret = "-" * len(self.mot_choisi)
        self.labelMotChoisi.set_markup('<span color="#c0392b" weight="bold" size="xx-large" stretch="ultraexpanded">' + self.mot_tiret + "</span>")

        # DEBUG
        print(self.mot_choisi)
        print(self.score , '/', self.nb_parties)

    def gestion_bouton(self, etat):
        """
        Active / desactive les boutons de type Lettres
        :param etat:    'on' -> on active tous les boutons (lettres)
                        'off' -> la partie est finie les boutons sont desactivés
        :return:
        """
        for i in range(26):
            if etat == "on":
                self.boutonLettres[i].set_sensitive(True)
            else:
                self.boutonLettres[i].set_sensitive(False)

    def click_sur_lettres(self, widget, lettre, bouton):
        """
        Gestion d'un clic sur une lettre
        Infirme ou confirme sa présence dans le mot
        :param widget:
        :param lettre: la lettre sélectionnée
        :param bouton: le bouton associé à la lettre
        :return:
        """
        bouton.set_sensitive(False)

        if self.jeu_actif == True:

            if lettre in self.mot_choisi:
                print('Y')
                mot = ""
                i = 0
                while i < len(self.mot_choisi):
                    if self.mot_choisi[i] == lettre:
                        mot = mot + lettre
                        lettre_dans_mot = True
                    else:
                        mot = mot + self.mot_tiret[i]
                    i += 1
                self.mot_tiret = mot

                self.labelMotChoisi.set_markup(
                    '<span color="#c0392b" weight="bold" size="xx-large" stretch="ultraexpanded">'
                    + self.mot_tiret + "</span>")

                if self.mot_tiret == self.mot_choisi:
                    print("Vous avez gagné !!!")
                    self.jeu_actif = False
                    self.image_pendu.set_from_file('/usr/share/pendu-peda/images/pendu_10.gif')
                    self.gestion_bouton('off')
                    self.score += 1
                    self.nb_parties += 1
                    print(self.score, '/', self.nb_parties)

            else:
                self.nb_echecs += 1
                self.image_pendu.set_from_file('/usr/share/pendu-peda/images/' + 'pendu_' + str(self.nb_echecs)+'.gif')
                if self.nb_echecs == 7:  # trop d'erreurs. Fini.
                    print("PERDU !!!")
                    self.labelMotChoisi.set_markup("<big><big><big>" + self.mot_choisi + "</big></big></big>")
                    self.jeu_actif = False
                    self.gestion_bouton('off')
                    self.nb_parties += 1
                    print(self.score, '/', self.nb_parties)

        self.mise_a_jour_score(widget)

    def mise_a_jour_score(self, widget):
        """
        Fonction actualisant le label score / nb_parties
        :param widget:
        :return:
        """
        # Chargement fichier par défaut ou du fichier sélectionné ?
        print(self.score)
        print(self.nb_parties)
        self.labelScore.set_text(str(self.score) + '/' + str(self.nb_parties))



    def selectionner_fichier(self, widget, file, theme):
        """
        Fonction gérant la sélection d'un fichier de configuration spécifique
        disponible dans l'onglet 2
        Passe en paramètre le fichier (son nom) et le thème de ce fichier
        :param widget:
        :param file:
        :param theme:
        :return:
        """
        self.notebook.set_current_page(0)
        self.labelFile.set_text(self.repData + '/' + file)
        self.labelTheme.set_text(theme)
        self.lancement_jeu(widget)

    # -----------------------------------------------------------
    # Les données de base
    repData, file = installer_config_locale()
    matriceCM, matriceCE, matriceAUTRE = creer_matrice(repData)
    nb_echecs = 0
    score = 0
    nb_parties = 0

    def __init__(self):

        Gtk.Window.__init__(self, title="Le pendu Pédagogique")

        # Initialisation de la fenetre, creation d'un notebook
        self.set_border_width(3)
        self.set_default_size(800, 800)
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)
        self.connect

        # NOTEBOOK
        # --------
        # ONGLET 1

        # Creation d'une grille
        self.grid = Gtk.Grid()

        # L'alphabet
        self.boutonLettres = [0] * 26
        for i in range(26):
            self.boutonLettres[i] = Gtk.Button(label=chr(i + 65))
            self.boutonLettres[i].connect("clicked", self.click_sur_lettres, chr(i + 65), self.boutonLettres[i])
            self.grid.attach(self.boutonLettres[i], i, 0, 1, 1)

        # Les boutons
        boutonRecommencer = Gtk.Button(label="Recommencer")
        boutonQuitter = Gtk.Button(label="Quitter")
        boutonRecommencer.connect("clicked", self.lancement_jeu)
        boutonQuitter.connect("clicked",Gtk.main_quit)

        self.grid.attach(boutonRecommencer,0, 4, 13, 1)
        self.grid.attach(boutonQuitter, 13, 4, 13, 1)

        # L'image
        self.image_pendu = Gtk.Image.new_from_file('/usr/share/pendu-peda/images/' + 'pendu_0.gif')
        self.image_pendu.set_halign(Gtk.Align.END)
        self.grid.attach(self.image_pendu, 0,1,13,1)


        # Zone de texte
        self.labelMotChoisi = Gtk.Label('mot choisi')
        self.grid.attach(self.labelMotChoisi, 13, 1, 13, 1)

        # Score
        self.labelScore = Gtk.Label('Score : 0 / 0' + str(self.score) + str(self.nb_parties))
        self.grid.attach(self.labelScore, 0, 3, 26, 1)

        # Le pied de page
        self.labelFile = Gtk.Label(self.repData + '/' + self.file)
        self.labelTheme = Gtk.Label('# Dictionnaire général')
        self.labelFile.set_halign(Gtk.Align.START)
        self.labelTheme.set_halign(Gtk.Align.START)
        self.grid.attach(self.labelFile, 0, 5, 13, 1)
        self.grid.attach(self.labelTheme, 13, 5, 13, 1)

        # Affichage sur la grille
        self.notebook.append_page(self.grid)

        # --------
        # ONGLET 2
        # Creation d'une grille et des boutons associés
        self.grid2 = Gtk.Grid()
        textMatriceCM = [0] * int(len(self.matriceCM))
        boutonMatriceCM = [0] * int(len(self.matriceCM))
        textMatriceCE = [0] * int(len(self.matriceCE))
        boutonMatriceCE = [0] * int(len(self.matriceCE))
        textMatriceAUTRE = [0] * int(len(self.matriceAUTRE))
        boutonMatriceAUTRE = [0] * int(len(self.matriceAUTRE))

        # Colonne CM
        texteCM = Gtk.Label("NIVEAU CM")
        self.grid2.attach(texteCM, 0, 0, 2, 1)
        for i in range(len(self.matriceCM)):
            textMatriceCM[i] = Gtk.Label(self.matriceCM[i][2])
            self.grid2.attach(textMatriceCM[i], 0, i+1, 1, 1)
            textMatriceCM[i].set_halign(Gtk.Align.END)
            textMatriceCM[i].set_direction(Gtk.TextDirection.RTL)
            boutonMatriceCM[i] = Gtk.Button.new_with_label("GO")
            boutonMatriceCM[i].connect("clicked", self.selectionner_fichier, self.matriceCM[i][3], self.matriceCM[i][2])
            self.grid2.attach(boutonMatriceCM[i], 1, i+1, 1, 1)

        # Colonne CE
        texteCE = Gtk.Label("NIVEAU CE")
        self.grid2.attach(texteCE, 2, 0, 2, 1)
        for i in range(len(self.matriceCE)):
            textMatriceCE[i] = Gtk.Label(self.matriceCE[i][2])
            self.grid2.attach(textMatriceCE[i], 2, i + 1, 1, 1)
            textMatriceCE[i].set_halign(Gtk.Align.END)
            textMatriceCE[i].set_direction(Gtk.TextDirection.RTL)
            boutonMatriceCE[i] = Gtk.Button.new_with_label("GO")
            boutonMatriceCE[i].connect("clicked", self.selectionner_fichier, self.matriceCE[i][3], self.matriceCE[i][2])
            self.grid2.attach(boutonMatriceCE[i], 3, i+1, 1, 1)

        # Colonne AUTRE
        texteAUTRE = Gtk.Label("NIVEAU CE")
        self.grid2.attach(texteAUTRE, 4, 0, 2, 1)
        for i in range(len(self.matriceAUTRE)):
            textMatriceAUTRE[i] = Gtk.Label(self.matriceAUTRE[i][2])
            self.grid2.attach(textMatriceAUTRE[i], 4, i + 1, 1, 1)
            textMatriceAUTRE[i].set_halign(Gtk.Align.END)
            textMatriceAUTRE[i].set_direction(Gtk.TextDirection.RTL)
            boutonMatriceAUTRE[i] = Gtk.Button.new_with_label("GO")
            boutonMatriceAUTRE[i].connect("clicked", self.selectionner_fichier, self.matriceAUTRE[i][3], self.matriceAUTRE[i][2])
            self.grid2.attach(boutonMatriceAUTRE[i], 5, i + 1, 1, 1)

        # Affichage sur la grille avec un scroll
        s_win = Gtk.ScrolledWindow()
        s_win.add_with_viewport(self.grid2)
        self.add(s_win)
        self.set_default_size(800, 300)
        self.notebook.append_page(s_win)

        # --------
        # ONGLET 3
        messageOnglet3 = __doc__
        self.page3 = Gtk.Box()
        self.page3.set_border_width(10)
        self.page3.add(Gtk.Label('aze'))
        self.notebook.append_page(
            self.page3,
            Gtk.Image.new_from_icon_name(
                "help-about",
                Gtk.IconSize.MENU
            )
        )


def main():
    win = GtkPendu()
    win.move(20,20)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    win.lancement_jeu(GtkPendu.file)
    Gtk.main()


"""
 Boucle main()
"""
if __name__ == "__main__":
    # execute only if run as a script
    main()