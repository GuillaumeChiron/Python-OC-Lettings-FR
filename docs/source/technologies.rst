Technologies utilisées
======================

Langages
--------

- **Python 3.13** : langage du back-end.
- **HTML / CSS / JavaScript** : templates et fichiers statiques du front-end.
- **reStructuredText** : rédaction de cette documentation.
- **YAML** : configuration du pipeline CI/CD et de Read the Docs.

Back-end
--------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Outil
     - Rôle
   * - Django 5.2
     - Framework web : modèles, vues, templates, administration
   * - SQLite
     - Base de données, stockée dans le fichier ``oc-lettings-site.sqlite3``
   * - python-dotenv
     - Chargement des variables d'environnement depuis le fichier ``.env``
   * - Gunicorn
     - Serveur WSGI utilisé en production
   * - WhiteNoise
     - Service des fichiers statiques (CSS, JS, images) en production

Front-end
---------

- **Bootstrap 5** : mise en page et composants.
- **Font Awesome** et **Feather Icons** : icônes.
- **AOS** (*Animate On Scroll*) : animations au défilement.

Ces bibliothèques sont chargées depuis des CDN dans le template ``base.html``.

Qualité et tests
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Outil
     - Rôle
   * - flake8
     - Vérification du style du code (configuration dans ``setup.cfg``)
   * - pytest et pytest-django
     - Exécution des tests unitaires et d'intégration
   * - pytest-cov
     - Mesure de la couverture de code (minimum 80 %)

Surveillance
------------

- **Sentry** (``sentry-sdk``) : remontée des erreurs et des événements de
  journalisation en production.
- **logging** (module standard de Python) : journalisation dans la console.

Déploiement
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Outil
     - Rôle
   * - Git et GitHub
     - Gestion des versions et hébergement du code
   * - GitHub Actions
     - Pipeline CI/CD : tests, construction de l'image, déploiement
   * - Docker
     - Conteneurisation de l'application
   * - Docker Hub
     - Registre des images Docker (``guillaumechiron/oc-lettings``)
   * - Render
     - Hébergement du site en production

Documentation
-------------

- **Sphinx** avec le thème **sphinx-rtd-theme** : génération de cette
  documentation.
- **Read the Docs** : hébergement et mise à jour automatique de la
  documentation.
