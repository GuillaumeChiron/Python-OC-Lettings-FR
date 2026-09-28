Installation
============

Cette page décrit l'installation du projet sur un poste de développement.

Prérequis
---------

- Git
- Python 3.10 ou supérieur (le projet est testé avec Python 3.13)
- SQLite3 en ligne de commande (optionnel, pour consulter la base de données)

Cloner le dépôt
---------------

.. code-block:: bash

   git clone https://github.com/GuillaumeChiron/Python-OC-Lettings-FR.git
   cd Python-OC-Lettings-FR

Créer l'environnement virtuel
-----------------------------

.. code-block:: bash

   python -m venv venv

Activer l'environnement virtuel :

- macOS / Linux :

  .. code-block:: bash

     source venv/bin/activate

- Windows (PowerShell) :

  .. code-block:: powershell

     .\venv\Scripts\Activate.ps1

Pour désactiver l'environnement : ``deactivate``.

Installer les dépendances
-------------------------

.. code-block:: bash

   pip install -r requirements.txt

Configurer les variables d'environnement
----------------------------------------

La configuration sensible est lue depuis un fichier ``.env`` placé à la racine
du projet. Ce fichier n'est pas versionné : il faut le créer à partir du modèle
``.env.example``.

.. code-block:: bash

   cp .env.example .env

Renseigner ensuite les variables suivantes :

``SECRET_KEY`` (obligatoire)
   Clé de signature interne à Django (sessions, jetons CSRF...). Le site
   refuse de démarrer si elle est absente. Pour en générer une :

   .. code-block:: bash

      python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

``DEBUG``
   ``True`` en développement pour afficher les erreurs détaillées. Valeur par
   défaut : ``False``, qui est la valeur attendue en production.

``ALLOWED_HOSTS``
   Noms de domaine autorisés à servir le site, séparés par des virgules.
   Valeur par défaut : ``localhost,127.0.0.1``.

``SENTRY_DSN`` (optionnel)
   Adresse du projet Sentry qui reçoit les erreurs. Si la variable est vide,
   Sentry est désactivé et le site fonctionne normalement. Pour l'obtenir :

   1. créer un compte sur `sentry.io <https://sentry.io>`_ ;
   2. créer un projet de plateforme **Django** ;
   3. copier le DSN depuis **Settings → Projects → (votre projet) → Client
      Keys (DSN)**.

Exemple de fichier ``.env`` pour le développement :

.. code-block:: text

   SECRET_KEY=une-cle-generee-avec-la-commande-ci-dessus
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   SENTRY_DSN=

.. note::

   Avec ``DEBUG=False`` en local, les fichiers statiques (CSS, images) ne
   s'affichent pas tant que la commande ``python manage.py collectstatic`` n'a
   pas été exécutée.

Vérifier l'installation
-----------------------

Lancer le linting et les tests depuis la racine du projet :

.. code-block:: bash

   flake8
   pytest --cov=. --cov-report=term-missing

Les deux commandes doivent se terminer sans erreur, avec une couverture
supérieure à 80 %.
