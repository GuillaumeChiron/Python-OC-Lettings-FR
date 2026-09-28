Déploiement et gestion de l'application
=======================================

Le site est en ligne à l'adresse `https://oc-lettings-7w6w.onrender.com
<https://oc-lettings-7w6w.onrender.com>`_.

Fonctionnement
--------------

Le déploiement est entièrement automatisé par un pipeline GitHub Actions,
défini dans le fichier ``.github/workflows/ci.yml``. Il est composé de trois
jobs qui s'enchaînent : un job ne démarre que si le précédent a réussi.

.. code-block:: text

   build-and-test  →  containerize  →  deploy

1. **build-and-test** : installe les dépendances, lance ``flake8`` puis
   ``pytest``. Le job échoue si un test échoue ou si la couverture de tests est
   inférieure à 80 %.
2. **containerize** : construit l'image Docker et la publie sur Docker Hub
   (``guillaumechiron/oc-lettings``) avec deux tags : ``latest`` et le hash du
   commit.
3. **deploy** : déclenche le redéploiement du service sur Render, qui récupère
   la nouvelle image ``latest`` et redémarre le site.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Événement
     - Jobs exécutés
   * - Push sur une autre branche que ``master``
     - ``build-and-test`` uniquement
   * - Pull request
     - ``build-and-test`` uniquement
   * - Push sur ``master`` (y compris un merge)
     - ``build-and-test`` → ``containerize`` → ``deploy``

Du code qui ne passe pas les tests ne peut donc jamais être publié ni mis en
production.

Image Docker
------------

Le ``Dockerfile`` à la racine du projet construit l'image de production :

- image de base ``python:3.13-slim`` ;
- installation des dépendances de ``requirements.txt`` ;
- collecte des fichiers statiques (``collectstatic``), servis ensuite par
  WhiteNoise ;
- lancement du site avec Gunicorn, sur le port défini par la variable
  ``PORT`` (8000 par défaut).

.. important::

   Aucune donnée sensible n'est incluse dans l'image : la ``SECRET_KEY`` est
   fournie au lancement du conteneur, et le fichier ``.env`` est exclu par le
   ``.dockerignore``.

Prérequis
---------

- Un compte `GitHub <https://github.com>`_ avec les droits d'administration
  sur le dépôt (pour gérer les secrets).
- Un compte `Docker Hub <https://hub.docker.com>`_.
- Un compte `Render <https://render.com>`_.
- Un compte `Sentry <https://sentry.io>`_ (optionnel, pour la remontée des
  erreurs en production).
- Docker installé en local (uniquement pour lancer ou construire l'image sur
  sa machine).

Configuration
-------------

Aucune donnée sensible n'est stockée dans le code : elles sont renseignées
dans les secrets GitHub et dans les variables d'environnement de Render.

Secrets GitHub Actions
~~~~~~~~~~~~~~~~~~~~~~

À créer dans **Settings → Secrets and variables → Actions → New repository
secret** :

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Nom
     - Rôle
     - Où l'obtenir
   * - ``DOCKERHUB_USERNAME``
     - Nom d'utilisateur Docker Hub
     - Votre compte Docker Hub
   * - ``DOCKERHUB_TOKEN``
     - Token d'accès pour publier l'image
     - Docker Hub : **Account settings → Personal access tokens**,
       permissions **Read & Write**
   * - ``RENDER_DEPLOY_HOOK_URL``
     - URL qui déclenche un redéploiement
     - Render : **votre service → Settings → Deploy Hook**

Service Render
~~~~~~~~~~~~~~

Mise en place initiale, à faire une seule fois :

1. Sur Render : **New + → Web Service → Existing Image**.
2. Image URL : ``docker.io/guillaumechiron/oc-lettings:latest``.
3. Region : **Frankfurt (EU)**, Instance Type : **Free**.
4. Renseigner les variables d'environnement ci-dessous, puis cliquer sur
   **Deploy Web Service**.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Variable
     - Valeur
   * - ``SECRET_KEY``
     - Une clé dédiée à la production, différente de la clé locale (voir
       :doc:`installation`)
   * - ``DEBUG``
     - ``False``
   * - ``ALLOWED_HOSTS``
     - L'adresse du service, sans ``https://`` (ex.
       ``oc-lettings-7w6w.onrender.com``)
   * - ``SENTRY_DSN``
     - Le DSN du projet Sentry, sans guillemets

La variable ``PORT`` est fournie automatiquement par Render : il ne faut pas
la définir.

Déployer une nouvelle version
-----------------------------

1. Créer une branche de travail :

   .. code-block:: bash

      git checkout -b ma-branche

2. Développer, puis pousser la branche. Le job ``build-and-test`` vérifie le
   code :

   .. code-block:: bash

      git push -u origin ma-branche

3. Une fois le job au vert, fusionner la branche sur ``master`` (pull request
   sur GitHub, ou en ligne de commande) :

   .. code-block:: bash

      git checkout master
      git merge ma-branche
      git push

4. Suivre l'exécution des trois jobs dans l'onglet **Actions** de GitHub, puis
   le déploiement dans l'onglet **Events** du service Render.

Gestion de l'application
------------------------

Données en production
~~~~~~~~~~~~~~~~~~~~~

.. warning::

   La base SQLite est embarquée dans l'image Docker. Les modifications faites
   via l'administration en production sont perdues à chaque redéploiement.

Surveillance
~~~~~~~~~~~~

Les erreurs de production sont remontées dans Sentry (onglet **Issues**), et
les journaux du serveur sont consultables dans l'onglet **Logs** du service
Render.

Revenir à une version précédente
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Chaque image est aussi publiée avec le hash de son commit. Pour revenir à une
version précédente, modifier l'**Image URL** du service Render pour utiliser
le tag du commit souhaité, par exemple
``docker.io/guillaumechiron/oc-lettings:<hash-du-commit>``.

Lancer l'image en local
~~~~~~~~~~~~~~~~~~~~~~~

Une seule commande suffit pour récupérer l'image depuis Docker Hub et lancer
le site :

.. code-block:: bash

   docker run --rm -p 8000:8000 -e SECRET_KEY=une-cle-de-test guillaumechiron/oc-lettings:latest

Pour construire l'image à partir du code local :

.. code-block:: bash

   docker build -t oc-lettings .
   docker run --rm -p 8000:8000 -e SECRET_KEY=une-cle-de-test oc-lettings
