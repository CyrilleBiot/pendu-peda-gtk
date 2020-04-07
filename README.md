# pendu-peda-gtk
Pendu pédagogique GTK

Remplace le projet initial en TK.

## Installation : test depuis les sources
```
$ git clone https://github.com/CyrilleBiot/pendu-peda-gtk.git
Clonage dans 'pendu-peda-gtk'...
remote: Enumerating objects: 155, done.
remote: Counting objects: 100% (155/155), done.
remote: Compressing objects: 100% (119/119), done.
remote: Total 155 (delta 45), reused 136 (delta 29), pack-reused 0
Réception d'objets: 100% (155/155), 1.68 Mio | 397.00 Kio/s, fait.
Résolution des deltas: 100% (45/45), fait.

$ cd pendu-peda-gtk/

$ ./source/pendu-peda-gtk.py
```

## Installation paquet DEB
```
$ wget https://github.com/CyrilleBiot/pendu-peda-gtk/blob/master/pendu-peda-gtk_0.0.2%2Bnmu2_all.deb
$ su
# dpkg -i pendu-peda-gtk_0.0.2%2Bnmu2_all.deb
```

Toutes les informations détailles sont disponibles ici :
<a href="https://cbiot.fr/dokuwiki/doku.php?id=python:pendu-peda-gtk" target="_blank">Le Pendu Pedagogique GTK</a>

![alt text](https://cbiot.fr/dokuwiki/lib/exe/fetch.php?w=800&tok=ba8746&media=python:2020-03-10_11-45.png)
![alt text](https://cbiot.fr/dokuwiki/lib/exe/fetch.php?w=800&tok=08827a&media=python:2020-03-10_11-49.png)
![alt text](https://cbiot.fr/dokuwiki/lib/exe/fetch.php?w=800&tok=6f60b8&media=python:2020-03-12_16-10.png)
![alt text](https://cbiot.fr/dokuwiki/_media/python:2020-04-07_13-33.png)

## Changelog

pendu-peda-gtk (0.4) unstable; urgency=medium
 
  * Insert Themes

 -- ragnarok <ragnarok@fenrir.home>  Tue, 07 Apr 2020 13:24:17 +0200

pendu-peda-gtk (0.3+nmu1) UNRELEASED; urgency=medium

  * Clean Gtk.box code

 -- ragnarok <ragnarok@fenrir.home>  Thu, 12 Mar 2020 21:30:32 +0100

pendu-peda-gtk (0.3) unstable; urgency=medium

  * DEBUG mode since the git source dir. 
  * Fix size windows tab2 (create Frames)
  * Changed agressive red color
  * Fix bug Level print
  * Remove QUIT button


 -- ragnarok <ragnarok@fenrir.home>  Thu, 12 Mar 2020 15:55:59 +0100

pendu-peda-gtk (0.2) unstable; urgency=medium

  * Fix path install, size of screen, level, about dialog access

 -- ragnarok <ragnarok@fenrir.home>  Wed, 11 Mar 2020 15:30:43 +0100

pendu-peda-gtk (0.0.2+nmu2) unstable; urgency=medium

  * Fix bug Score 

 -- ragnarok <ragnarok@fenrir.home>  Tue, 10 Mar 2020 11:28:23 +0100

pendu-peda-gtk (0.0.2+nmu1) unstable; urgency=medium

  * Fix bugs. Add icon. Rebuild CSS. 

 -- ragnarok <ragnarok@fenrir.home>  Tue, 10 Mar 2020 11:06:31 +0100

pendu-peda-gtk (0.0.2) unstable; urgency=medium

  * Initial release. (Closes: #XXXXXX)

 -- ragnarok <ragnarok@fenrir.home>  Mon, 09 Mar 2020 10:40:20 +0100
