Base de données et modèles
==========================

Le projet utilise une base de données **SQLite**, stockée dans le fichier
``oc-lettings-site.sqlite3`` à la racine du projet. Les tables sont gérées
par l'ORM de Django : chaque modèle correspond à une table nommée
``<application>_<modèle>``.

Schéma général
--------------

.. code-block:: text

   lettings_address            lettings_letting
   ┌──────────────────┐        ┌──────────────────┐
   │ id (PK)          │◄───────│ address_id (1-1) │
   │ number           │        │ id (PK)          │
   │ street           │        │ title            │
   │ city             │        └──────────────────┘
   │ state            │
   │ zip_code         │
   │ country_iso_code │
   └──────────────────┘

   auth_user                   profiles_profile
   ┌──────────────────┐        ┌──────────────────┐
   │ id (PK)          │◄───────│ user_id (1-1)    │
   │ username         │        │ id (PK)          │
   │ first_name       │        │ favorite_city    │
   │ last_name        │        └──────────────────┘
   │ email            │
   │ ...              │
   └──────────────────┘

Les deux relations sont de type **un-à-un** (``OneToOneField``) : une location
possède une seule adresse, et un profil est rattaché à un seul utilisateur.

Application ``lettings``
------------------------

Modèle ``Address``
~~~~~~~~~~~~~~~~~~

Adresse postale d'une location. Table : ``lettings_address``.

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Champ
     - Type
     - Contraintes
   * - ``number``
     - ``PositiveIntegerField``
     - Entier positif, 9999 maximum
   * - ``street``
     - ``CharField``
     - 64 caractères maximum
   * - ``city``
     - ``CharField``
     - 64 caractères maximum
   * - ``state``
     - ``CharField``
     - Exactement 2 caractères (ex. ``CA``)
   * - ``zip_code``
     - ``PositiveIntegerField``
     - Entier positif, 99999 maximum
   * - ``country_iso_code``
     - ``CharField``
     - Exactement 3 caractères (code ISO, ex. ``USA``)

Représentation textuelle : ``<number> <street>``. Le nom au pluriel est
défini à « addresses » (``verbose_name_plural``) pour un affichage correct
dans l'administration.

Modèle ``Letting``
~~~~~~~~~~~~~~~~~~

Location proposée sur le site. Table : ``lettings_letting``.

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Champ
     - Type
     - Contraintes
   * - ``title``
     - ``CharField``
     - 256 caractères maximum
   * - ``address``
     - ``OneToOneField`` vers ``Address``
     - Suppression en cascade : supprimer l'adresse supprime la location

Représentation textuelle : le titre de la location.

Application ``profiles``
------------------------

Modèle ``Profile``
~~~~~~~~~~~~~~~~~~

Profil d'un utilisateur du site. Table : ``profiles_profile``.

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Champ
     - Type
     - Contraintes
   * - ``user``
     - ``OneToOneField`` vers ``User``
     - Utilisateur Django (``django.contrib.auth``). Suppression en
       cascade : supprimer l'utilisateur supprime le profil
   * - ``favorite_city``
     - ``CharField``
     - 64 caractères maximum, facultatif

Représentation textuelle : le nom d'utilisateur.

Les informations d'identité (nom d'utilisateur, prénom, nom, e-mail) sont
stockées dans le modèle ``User`` fourni par Django, table ``auth_user``.

Migrations
----------

Lors de la refonte, les modèles ont été déplacés de l'application
``oc_lettings_site`` vers les applications ``lettings`` et ``profiles``. Les
données ont été transférées par des migrations Django (``RunPython``), sans
SQL brut, en conservant les identifiants existants. Les anciennes tables ont
ensuite été supprimées par une migration dédiée.

Consulter la base de données
----------------------------

Depuis la racine du projet, avec SQLite3 en ligne de commande :

.. code-block:: text

   sqlite3 oc-lettings-site.sqlite3
   .tables
   pragma table_info(profiles_profile);
   select user_id, favorite_city from profiles_profile where favorite_city like 'B%';
   .quit
