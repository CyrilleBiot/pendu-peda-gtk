import os, shutil
from random import choice
from operator import itemgetter
import unicodedata
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class GtkPendu(Gtk.Window):

    def installerConfigLocale():
        user = os.environ["USER"]
        repertoire = '/home/' + user + '/.primtux/pendu-peda'
        if not os.path.exists(repertoire):
            print("Le repertoire n'existe pas. On le créer")
            shutil.copytree('/usr/share/pendu-peda/data-files/',
                            '/home/' + user + '/.primtux/pendu-peda/data-files/')
        else:
            print("Le repertoire existe. Configuration OK.")
        repData = '/home/' + user + '/.primtux/pendu-peda/data-files'
        file = 'autre-liste-francais.txt'

        return repData, file

    def creerMatrice(repData):
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



    def initJeu(self, widget):
        print('Init Jeu')
        print(self.file)
        try:
            self.file
        except NameError:
            print("Chargement du fichier de défaut.")
            self.file = 'autre-liste-francais.txt'
        else:
            print("sure, it was defined : ", self.file)

        print('init ENCORE')
        fichier = open(str(self.repData) + '/' + str(self.file), "r")
        liste_mots = fichier.readlines()
        fichier.close()
        del liste_mots[0:3]  # Nettoyage de l'entete
        print(liste_mots)
        mot_choisi = choice(liste_mots).rstrip()
        mot_choisi = mot_choisi.upper()
        mot_choisi = ''.join((c for c in unicodedata.normalize('NFD', mot_choisi) if unicodedata.category(c) != 'Mn'))

        mot_partiel = " - " * len(mot_choisi)

        self.labelMotChoisi.set_text(mot_partiel)
        print(mot_choisi)
        self.mot_choisi = mot_choisi

        return self.mot_choisi


    def clickSurLettres(self, widget, lettre, bouton):
        bouton.set_sensitive(False)

        print(self.mot_choisi)
        print('lettre : ' , lettre)

        if lettre in self.mot_choisi:
            print('Y')

        else:
            print('no')







    repData, file = installerConfigLocale()
    matriceCM, matriceCE, matriceAUTRE = creerMatrice(repData)




    def selectionnerFichier(self, widget, file, theme):
        print("Selctionner Fichier fonction")
        self.notebook.set_current_page(0)
        self.labelFile.set_text(self.repData + '/' + file)
        self.labelTheme.set_text(theme)
        self.file = file
        self.initJeu(widget)

    def __init__(self):

        Gtk.Window.__init__(self, title="Le pendu Pédagogique")
        self.set_border_width(3)
        #self.set_default_size(800, 800)
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)
        self.connect



        # ONGLET 1
        # Creation d'une grille
        self.grid = Gtk.Grid()

        # L'alphabet
        boutonLettres = [0] * 26
        for i in range(26):
            boutonLettres[i] = Gtk.Button(label=chr(i + 65),  expand = True)
            boutonLettres[i].connect("clicked", self.clickSurLettres, chr(i + 65), boutonLettres[i])

            #bouton[i].set_property("width-request",3)
            #bouton[i].set_property("height-request",3)
            self.grid.attach(boutonLettres[i], i, 0, 1, 1)

        # Les boutons
        boutonRecommencer = Gtk.Button(label="Recommencer", expand=True)
        boutonQuitter = Gtk.Button(label="Quitter", expand=True)
        boutonRecommencer.connect("clicked", self.initJeu)

        self.grid.attach(boutonRecommencer,0, 1, 13, 1)
        self.grid.attach(boutonQuitter, 13, 1, 13, 1)

        # Le pied de page
        self.labelFile = Gtk.Label(self.file, expand=True)
        self.labelTheme = Gtk.Label(self.repData, expand=True)
        self.labelFile.set_halign(Gtk.Align.END)
        self.labelFile.set_direction(Gtk.TextDirection.RTL)
        self.labelTheme.set_halign(Gtk.Align.END)
        self.labelTheme.set_direction(Gtk.TextDirection.RTL)
        self.grid.attach(self.labelFile, 0, 2, 13, 1)
        self.grid.attach(self.labelTheme, 13, 2, 13, 1)

        # Zone de texte
        self.labelMotChoisi = Gtk.Label('mot choisi', expand=True)
        self.grid.attach(self.labelMotChoisi, 0, 3, 26, 4)


        # Affichage sur la grille
        self.notebook.append_page(self.grid)

        # ONGLET 2
        self.grid2 = Gtk.Grid()

        print(self.matriceAUTRE)
        print(self.matriceCE)
        print(self.matriceCM)

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
            boutonMatriceCM[i].connect("clicked", self.selectionnerFichier, self.matriceCM[i][3], self.matriceCM[i][2])
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
            boutonMatriceCE[i].connect("clicked", self.selectionnerFichier, self.matriceCE[i][3], self.matriceCE[i][2])
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
            boutonMatriceAUTRE[i].connect("clicked", self.selectionnerFichier, self.matriceAUTRE[i][3], self.matriceAUTRE[i][2])
            self.grid2.attach(boutonMatriceAUTRE[i], 5, i + 1, 1, 1)



        # Affichage sur la grille
        self.notebook.append_page(self.grid2)



        # ONGLET 3
        self.page3 = Gtk.Box()
        self.page3.set_border_width(10)
        self.page3.add(Gtk.Label('LABEL ONGLET 3'))
        self.notebook.append_page(
            self.page3,
            Gtk.Image.new_from_icon_name(
                "help-about",
                Gtk.IconSize.MENU
            )
        )
        """
        # ONGLET 4
        layout = Gtk.Layout()
        vadjustment = layout.get_vadjustment()
        hadjustment = layout.get_hadjustment()

        vscrollbar = Gtk.Scrollbar(orientation=Gtk.Orientation.VERTICAL,
                                   adjustment=vadjustment)
        grid = Gtk.Grid()


        self.notebook.append_page(grid)"""


win = GtkPendu()
win.connect("destroy", Gtk.main_quit)
win.show_all()
mot_choisi = win.initJeu(GtkPendu.file)
Gtk.main()
