Démarrage rapide
================

Cette page permet de lancer le site en quelques minutes, soit depuis le code
source, soit directement avec Docker.

Option 1 : depuis le code source
--------------------------------

Après avoir suivi la page :doc:`installation`, depuis la racine du projet et
avec l'environnement virtuel activé :

.. code-block:: bash

   python manage.py runserver

Le site est alors accessible à l'adresse http://localhost:8000.

La base de données SQLite ``oc-lettings-site.sqlite3`` est fournie avec le
projet : elle contient déjà des locations et des profils de démonstration.
Aucune migration n'est à lancer.

Option 2 : avec Docker
----------------------

Seul Docker est nécessaire. Une seule commande récupère l'image depuis
Docker Hub et lance le site :

.. code-block:: bash

   docker run --rm -p 8000:8000 -e SECRET_KEY=une-cle-de-test guillaumechiron/oc-lettings:latest

Le site est alors accessible à l'adresse http://localhost:8000. ``Ctrl+C``
arrête le conteneur.

Pour utiliser sa propre configuration (Sentry, etc.), remplacer
``-e SECRET_KEY=...`` par ``--env-file .env``.

.. warning::

   Avec Docker, les valeurs du fichier ``.env`` ne doivent pas être entourées
   de guillemets.

Découvrir le site
-----------------

Une fois le site lancé :

- ``/`` : page d'accueil, avec les liens vers les locations et les profils ;
- ``/lettings/`` : liste des locations ;
- ``/lettings/1/`` : détail de la location n°1 ;
- ``/profiles/`` : liste des profils ;
- ``/profiles/<nom d'utilisateur>/`` : détail d'un profil ;
- ``/admin/`` : interface d'administration.

Accéder à l'administration
--------------------------

L'interface d'administration est disponible sur http://localhost:8000/admin.
Les identifiants du compte administrateur de la base de démonstration sont
indiqués dans le fichier ``README.md`` du dépôt.

Commandes utiles
----------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Commande
     - Rôle
   * - ``python manage.py runserver``
     - Lancer le serveur de développement
   * - ``flake8``
     - Vérifier le style du code
   * - ``pytest``
     - Lancer les tests
   * - ``pytest --cov=. --cov-report=term-missing``
     - Lancer les tests avec le rapport de couverture
   * - ``python manage.py createsuperuser``
     - Créer un nouveau compte administrateur
