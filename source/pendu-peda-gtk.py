#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pendu-peda-gtk.py
Jeu du pendu, version pédagogique.
Recodé en GTK

En lien avec les programmes officiels de l'école primaire.
  Source : https://github.com/CyrilleBiot/pendu-peda-gtk
  Source : https://cbiot.fr/

__author__ = "Cyrille BIOT <cyrille@cbiot.fr>"
__copyright__ = "Copyleft"
__credits__ = "Cyrille BIOT <cyrille@cbiot.fr>"
__license__ = "GPL"
__version__ = "0.2"
__date__ = "2020/03/11"
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
from gi.repository import Gtk, Gdk, GdkPixbuf

def gtk_style():
    """
    Fonction definition de CSS de l'application
    Le fichier css : pendu-peda-gtk.css
    :return:
    """
    fileCSS = "./pendu-peda-gtk.css"
    style_provider = Gtk.CssProvider()
    style_provider.load_from_path(fileCSS)

    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

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
        repertoire = '/home/' + user + '/.config/primtux/pendu-peda-gtk'
        if not os.path.exists(repertoire):
            print("Le repertoire n'existe pas. On le crée.")
            shutil.copytree('/usr/share/pendu-peda-gtk/data-files/',
                            '/home/' + user + '/.config/primtux/pendu-peda-gtk/data-files/')
        else:
            print("Le repertoire existe. Configuration OK.")
        repData = '/home/' + user + '/.config/primtux/pendu-peda-gtk/data-files'
        file = 'autre-liste-francais.txt'
        theme = "# Dictionnaire général"

        return repData, file, theme

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
        self.jeu_actif = True  # Si nouvelle partie (booleen)
        self.nb_echecs = 0  # Compte le nombre d'échecs (integer)
        self.image_pendu.set_from_file(
            '/usr/share/pendu-peda-gtk/images/' + self.niveau + '/pendu_0.gif')  # Image par défaut

        # Chargement du fichier et choix aléatoire d'un mot
        fichier = open(str(self.repData) + '/' + str(self.file), "r")
        liste_mots = fichier.readlines()
        fichier.close()
        del liste_mots[0:3]  # Nettoyage de l'entete
        self.mot_choisi = choice(liste_mots).rstrip()
        self.mot_choisi = self.mot_choisi.upper()
        self.mot_choisi = ''.join(
            (c for c in unicodedata.normalize('NFD', self.mot_choisi) if unicodedata.category(c) != 'Mn'))

        # Créer d'un mot contenant le même nombre de lettres mais affichant des tirets
        # Mise à jour de son label
        self.mot_tiret = "-" * len(self.mot_choisi)
        self.labelMotChoisi.set_markup(self.mot_tiret)

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
                self.boutonLettres[i].set_name('bouton-lettres')
            else:
                self.boutonLettres[i].set_sensitive(False)
                self.boutonLettres[i].set_name('bouton-lettres-inactif')

    def clic_sur_lettres(self, widget, lettre, bouton):
        """
        Gestion d'un clic sur une lettre
        Infirme ou confirme sa présence dans le mot
        :param widget:
        :param lettre: la lettre sélectionnée
        :param bouton: le bouton associé à la lettre
        :return:
        """
        bouton.set_sensitive(False)
        bouton.set_name('bouton-lettres-inactif')

        # Gestion du niveau
        if self.niveau == '001':
            max_essais = 7
        else:
            max_essais = 10

        if self.jeu_actif == True:
            if lettre in self.mot_choisi:
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

                self.labelMotChoisi.set_markup(self.mot_tiret)

                if self.mot_tiret == self.mot_choisi:
                    self.jeu_actif = False
                    self.image_pendu.set_from_file('/usr/share/pendu-peda-gtk/images/' + self.niveau + '/pendu_gagne.gif')
                    self.gestion_bouton('off')
                    self.score += 1
                    self.nb_parties += 1

            else:
                self.nb_echecs += 1
                self.image_pendu.set_from_file(
                    '/usr/share/pendu-peda-gtk/images/' + self.niveau + '/pendu_' + str(self.nb_echecs) + '.gif')
                if self.nb_echecs == max_essais:  # trop d'erreurs. Fini.
                    self.labelMotChoisi.set_markup(self.mot_choisi)
                    self.jeu_actif = False
                    self.gestion_bouton('off')
                    self.nb_parties += 1

        self.mise_a_jour_score(widget, self.score, self.nb_parties)

    def mise_a_jour_score(self, widget, score, nb_parties):
        """
        Fonction actualisant le label score / nb_parties
        :param widget:
        :return:
        """
        # Chargement fichier par défaut ou du fichier sélectionné ?
        self.labelScore.set_markup('Score : ' + str(score) + '/' + str(nb_parties))

    def fct_bouton_radio(self, widget, file, theme):
        """
        Function qui gere le button_radio (toggle)
        :param widget:
        :param file: Nom du Fichier
        :param theme: Theme ud Fichier
        :return:
        """
        self.file = file
        self.theme = theme

    def bouton_radio_niveau(self, widget, niveau):
        """
        Function qui gere le button_radio (toggle) du
        sélectionneur de niveau
        :param widget:
        :param niveau: niveau choisi
        :return:
        """
        self.niveau = niveau

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
        self.labelFile.set_markup(self.repData + '/' + file)
        self.labelTheme.set_markup(self.file)
        self.labelFile.set_markup(self.theme)
        self.labelNiveau.set_markup('# Niveau : ' + self.niveau)
        self.lancement_jeu(widget)

    def cliquer_sur_bouton_a_propos(self, widget):
        """
        Fonction de la Boite de Dialogue About
        :param widget:
        :return:
        """
        # Recuperation n° de version
        print(__doc__)
        lignes = __doc__.split("\n")
        for l in lignes:
            if '__version__' in l:
                version = l[15:-1]
            if '__date__' in l:
                dateGtKBox = l[12:-1]

        authors = ["Cyrille BIOT"]
        documenters = ["Cyrille BIOT"]
        self.dialog = Gtk.AboutDialog()
        logo = GdkPixbuf.Pixbuf.new_from_file("./pendu-peda.png")
        if logo != None:
            self.dialog.set_logo(logo)
        else:
            print("A GdkPixbuf Error has occurred.")
        self.dialog.set_name("Gtk.AboutDialog")
        self.dialog.set_version(version)
        self.dialog.set_copyright("(C) 2020 Cyrille BIOT")
        self.dialog.set_comments("Le Pendu Pédagogique.\n\n" \
                                "[" + dateGtKBox + "]")
        self.dialog.set_license("GNU General Public License (GPL), version 3.\n"
    "This program is free software: you can redistribute it and/or modify\n"
    "it under the terms of the GNU General Public License as published by\n"
    "the Free Software Foundation, either version 3 of the License, or\n"
    "(at your option) any later version.\n"
    "\n"
    "This program is distributed in the hope that it will be useful,\n"
    "but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
    "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
    "GNU General Public License for more details.\n"
    "You should have received a copy of the GNU General Public License\n"
    "along with this program.  If not, see <https://www.gnu.org/licenses/>\n")
        self.dialog.set_website("https://cbiot.fr")
        self.dialog.set_website_label("cbiot.fr")
        self.dialog.set_website("https://github.com/CyrilleBiot/pendu-peda-gtk")
        self.dialog.set_website_label("GIT Le pendu pédagogique GTK")
        self.dialog.set_authors(authors)
        self.dialog.set_documenters(documenters)
        self.dialog.set_translator_credits("Cyrille BIOT")
        self.dialog.connect("response", self.cliquer_sur_bouton_a_propos_reponse)
        self.dialog.run()

    def cliquer_sur_bouton_a_propos_reponse(self, widget, response):
        """
        Fonction fermant la boite de dialogue About
        :param widget:
        :param response:
        :return:
        """
        self.dialog.destroy()
        self.notebook.set_current_page(0)

    # -----------------------------------------------------------
    # Les données de base
    repData, file, theme = installer_config_locale()
    matriceCM, matriceCE, matriceAUTRE = creer_matrice(repData)
    nb_echecs = 0
    score = 0
    nb_parties = 0
    niveau = "001"

    def __init__(self):

        Gtk.Window.__init__(self, title="Le pendu Pédagogique")
        self.set_icon_from_file("./pendu-peda.png")

        # Initialisation de la fenetre, creation d'un notebook
        self.set_border_width(3)
        self.set_default_size(800, 600)
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
            self.boutonLettres[i].set_name('bouton-lettres')
            self.boutonLettres[i].connect("clicked", self.clic_sur_lettres, chr(i + 65), self.boutonLettres[i])
            self.grid.attach(self.boutonLettres[i], i, 0, 1, 1)

        # Les boutons
        boutonRecommencer = Gtk.Button(label="Recommencer")
        boutonQuitter = Gtk.Button(label="Quitter")
        boutonRecommencer.connect("clicked", self.lancement_jeu)
        boutonQuitter.connect("clicked", Gtk.main_quit)

        self.grid.attach(boutonRecommencer, 0, 3, 13, 1)
        self.grid.attach(boutonQuitter, 13, 3, 13, 1)

        # L'image
        self.image_pendu = Gtk.Image.new_from_file('/usr/share/pendu-peda-gtk/images/' + self.niveau + '/pendu_0.gif')
        self.image_pendu.set_halign(Gtk.Align.END)
        self.image_pendu.set_name('img')
        self.grid.attach(self.image_pendu, 0, 1, 13, 1)

        # Zone de texte
        self.labelMotChoisi = Gtk.Label('mot choisi')
        self.labelMotChoisi.set_name('mot_choisi')
        self.grid.attach(self.labelMotChoisi, 13, 1, 13, 1)

        # Score
        self.labelScore = Gtk.Label('Score : ' + str(self.score) + '/' + str(self.nb_parties))
        self.labelScore.set_name('labelScore')
        self.grid.attach(self.labelScore, 0, 2, 26, 1)

        # Le pied de page
        self.labelFile = Gtk.Label(self.repData + '/' + self.file)
        self.labelTheme = Gtk.Label('# Dictionnaire général')
        self.labelNiveau = Gtk.Label('# Niveau : 001')
        self.labelFile.set_halign(Gtk.Align.START)
        self.labelTheme.set_halign(Gtk.Align.START)
        self.labelTheme.set_halign(Gtk.Align.START)
        self.grid.attach(self.labelFile, 0, 4, 11, 1)
        self.grid.attach(self.labelTheme, 11, 4, 11, 1)
        self.grid.attach(self.labelNiveau, 22, 4, 4, 1)

        # Affichage sur la grille
        self.notebook.append_page(self.grid, Gtk.Label('Jeu'))

        # --------
        # ONGLET 2
        # Creation d'une grille et des boutons associés
        self.grid2 = Gtk.Grid(column_spacing=50,
                              row_spacing=1)
        self.grid2.set_name('onglet23')
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
            self.grid2.attach(textMatriceCM[i], 0, i + 1, 1, 1)
            textMatriceCM[i].set_halign(Gtk.Align.END)
            textMatriceCM[i].set_direction(Gtk.TextDirection.RTL)
            if i == 0:
                boutonMatriceCM[i] = Gtk.RadioButton.new(None)
            else:
                boutonMatriceCM[i] = Gtk.RadioButton.new_from_widget(boutonMatriceCM[0])
            #boutonMatriceCM[i].connect("clicked", self.selectionner_fichier, self.matriceCM[i][3], self.matriceCM[i][2])
            boutonMatriceCM[i].connect("toggled", self.fct_bouton_radio, self.matriceCM[i][3], self.matriceCM[i][2])
            boutonMatriceCM[i].set_name('okMatrice')
            self.grid2.attach(boutonMatriceCM[i], 1, i + 1, 1, 1)

        # Colonne CE
        texteCE = Gtk.Label("NIVEAU CE")
        self.grid2.attach(texteCE, 2, 0, 2, 1)
        for i in range(len(self.matriceCE)):
            textMatriceCE[i] = Gtk.Label(self.matriceCE[i][2])
            self.grid2.attach(textMatriceCE[i], 2, i + 1, 1, 1)
            textMatriceCE[i].set_halign(Gtk.Align.END)
            textMatriceCE[i].set_direction(Gtk.TextDirection.RTL)
            #boutonMatriceCE[i] = Gtk.Button.new_with_label("GO")
            #boutonMatriceCE[i].connect("clicked", self.selectionner_fichier, self.matriceCE[i][3], self.matriceCE[i][2])
            boutonMatriceCE[i] = Gtk.RadioButton.new_from_widget(boutonMatriceCM[0])
            boutonMatriceCE[i].connect("toggled", self.fct_bouton_radio, self.matriceCE[i][3], self.matriceCE[i][2])
            boutonMatriceCE[i].set_name('okMatrice')
            self.grid2.attach(boutonMatriceCE[i], 3, i + 1, 1, 1)

        # Colonne AUTRE
        texteAUTRE = Gtk.Label("AUTRES")
        self.grid2.attach(texteAUTRE, 4, 0, 2, 1)
        for i in range(len(self.matriceAUTRE)):
            textMatriceAUTRE[i] = Gtk.Label(self.matriceAUTRE[i][2])
            self.grid2.attach(textMatriceAUTRE[i], 4, i + 1, 1, 1)
            textMatriceAUTRE[i].set_halign(Gtk.Align.END)
            textMatriceAUTRE[i].set_direction(Gtk.TextDirection.RTL)
            #boutonMatriceAUTRE[i] = Gtk.Button.new_with_label("GO")
            #boutonMatriceAUTRE[i].connect("clicked", self.selectionner_fichier, self.matriceAUTRE[i][3], self.matriceAUTRE[i][2])
            boutonMatriceAUTRE[i] = Gtk.RadioButton.new_from_widget(boutonMatriceCM[0])
            boutonMatriceAUTRE[i].connect("toggled", self.fct_bouton_radio, self.matriceAUTRE[i][3], self.matriceAUTRE[i][2])
            boutonMatriceAUTRE[i].set_name('okMatrice')
            self.grid2.attach(boutonMatriceAUTRE[i], 5, i + 1, 1, 1)

        # Colonne 4

        # Lanceur de sélection
        texteLancerJeu = Gtk.Label('Lancer le thème sélectionné')
        boutonLancerJeu = Gtk.Button("C'EST PARTI ! ! ! ",)
        texteLancerJeu.set_name('bold')
        boutonLancerJeu.connect("clicked", self.selectionner_fichier, self.file, self.theme)
        self.grid2.attach(texteLancerJeu, 6, 5, 1, 2)
        self.grid2.attach(boutonLancerJeu, 6, 7, 1, 2)

        # Sélecteur de niveau
        texteSelectNiveau = Gtk.Label('Choisir votre niveau')
        texteSelectNiveau.set_name('bold')
        self.grid2.attach(texteSelectNiveau, 6, 0, 1, 2)

        boutonRadioNiveau1 = Gtk.RadioButton.new_with_label(None, '[normal]')
        boutonRadioNiveau2 = Gtk.RadioButton.new_with_label_from_widget(boutonRadioNiveau1, '[facile]')
        boutonRadioNiveau1.connect("toggled", self.bouton_radio_niveau, '001')
        boutonRadioNiveau2.connect("toggled", self.bouton_radio_niveau, '002')
        self.grid2.attach(boutonRadioNiveau2, 6, 2, 1, 1)
        self.grid2.attach(boutonRadioNiveau1, 6, 3, 1, 2)

        # Affichage sur la grille avec un scroll
        s_win = Gtk.ScrolledWindow()
        s_win.add_with_viewport(self.grid2)
        self.add(s_win)
        self.set_default_size(800, 300)
        self.notebook.append_page(s_win, Gtk.Label('Configuration'))

        # --------
        # ONGLET 3
        # A propos
        about = Gtk.HBox()
        logo = Gtk.Image.new_from_file("./pendu-peda.png")
        if logo != None:
            about.add(logo)
        else:
            print("A GdkPixbuf Error has occurred.")
        logo.connect('map', self.cliquer_sur_bouton_a_propos)
        self.notebook.append_page(about, Gtk.Image.new_from_icon_name(
                "help-about",
                Gtk.IconSize.MENU
            ))

def main():
    """
    La boucle de lancement
    :return:
    """
    gtk_style()
    win = GtkPendu()
    win.move(20, 20)
    win.connect("destroy", Gtk.main_quit)
    win.lancement_jeu(GtkPendu.file)
    win.show_all()
    Gtk.main()


"""
 Boucle main()
"""
if __name__ == "__main__":
    # execute only if run as a script
    main()
