====================
genweb.ens
====================

Paquet `genweb` per a la gestió d'entitats i càrrecs.

Com funciona
============

Tipus de contingut disponibles:

- ``genweb.ens.acord`` (Acord òrgan de govern)
- ``genweb.ens.acta_reunio`` (Acta de reunió)
- ``genweb.ens.carrec`` (Càrrec)
- ``genweb.ens.carrec_upc`` (Càrrec UPC)
- ``genweb.ens.conveni`` (Conveni)
- ``genweb.ens.document_interes`` (Document d'interès)
- ``genweb.ens.ens`` (Ens)
- ``genweb.ens.escriptura_publica`` (Escriptura pública)
- ``genweb.ens.estatut`` (Estatu)
- ``genweb.ens.organ`` (Òrgan)
- ``genweb.ens.persona_contacte`` (Persona de contacte)
- ``genweb.ens.persona_directiu`` (Càrrec directiu)
- ``genweb.ens.representant`` (Representant UPC)
- ``genweb.ens.unitat`` (Unitat UPC)

Vistes disponibles:

- ``homepage``
- ``ens_search_results``
- ``carrec_search``
- ``carrec_search_results``
- ``taula_identificativa``
- ``taula_identificativa_csv``

La vista homepage
-----------------

La vista ``homepage`` conté un cercador de contingut de tipus
``genweb.ens.ens``. Els possibles valors dels camps de cerca *Figura jurídica*
i *Estat* són fixos. En canvi, els del camp *Cercar solament en* estan
calculats utilitzant l'estat actual del web i tenen les següents
característiques:

* Són noms de carpetes contingudes a la carpeta arrel de l'idioma. Per exemple,
  *Gabinet del Rector*, que té el *path* ``ens/ca/gabinet-del-rector``.
* Els identificadors de les carpetes coincideixen amb l'identificador d'algun
  dels grups d'usuaris definits al lloc web. Per exemple, `gabinet-del-rector`.
* Els valors apareixen seleccionats si l'usuari que està identificat al lloc
  web pertany al grup d'usuaris relacionat amb la carpeta.
* Si hi ha un o més valors seleccionats, la cerca ignorarà el contingut que no
  estiga dintre de les carpetes seleccionades. Si no n'hi ha cap, la cerca
  inclourà resultats continguts en qualsevol carpeta del lloc web.

Instal·lació
============

To install `genweb.ens` you simply add ``genweb.ens``
to the list of eggs in your buildout, run buildout and restart Plone.
Then, install `genweb.ens` using the Add-ons control panel.
