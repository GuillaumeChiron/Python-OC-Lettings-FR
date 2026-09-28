Guide d'utilisation
===================

Cette page présente des cas d'utilisation concrets du site, pour un
visiteur, un administrateur et un développeur.

Visiteur : consulter une location
---------------------------------

1. Ouvrir la page d'accueil du site.
2. Cliquer sur **Lettings** pour afficher la liste des locations.
3. Cliquer sur le titre d'une location, par exemple *Joshua Tree Green Haus
   /w Hot Tub*.
4. La page de détail affiche le titre et l'adresse complète de la location.

Si l'identifiant saisi dans l'URL ne correspond à aucune location (par
exemple ``/lettings/999/``), la page d'erreur 404 du site s'affiche.

Visiteur : consulter un profil
------------------------------

1. Depuis la page d'accueil, cliquer sur **Profiles**.
2. Cliquer sur un nom d'utilisateur.
3. La page de détail affiche le prénom, le nom, l'adresse e-mail et la ville
   favorite de l'utilisateur.

Administrateur : ajouter une location
-------------------------------------

Une location est toujours liée à une adresse : il faut donc créer l'adresse
en premier.

1. Se connecter à l'administration sur ``/admin/``.
2. Dans la section **Lettings**, cliquer sur **Addresses**, puis sur
   **Add address**.
3. Renseigner l'adresse, puis cliquer sur **Save** :

   - ``State`` : code sur 2 lettres (ex. ``CA``) ;
   - ``Country iso code`` : code ISO sur 3 lettres (ex. ``USA``).

4. Revenir dans **Lettings**, cliquer sur **Lettings**, puis sur
   **Add letting**.
5. Saisir le titre et sélectionner l'adresse créée à l'étape 3, puis cliquer
   sur **Save**.

La nouvelle location apparaît immédiatement dans la liste du site.

.. note::

   Une adresse ne peut être liée qu'à une seule location. Supprimer une
   adresse supprime aussi la location associée.

Administrateur : ajouter un profil
----------------------------------

Un profil est toujours lié à un utilisateur Django.

1. Dans la section **Authentication and Authorization**, cliquer sur
   **Users**, puis sur **Add user**. Renseigner le nom d'utilisateur et le mot
   de passe, puis enregistrer.
2. Sur la page suivante, compléter le prénom, le nom et l'adresse e-mail, puis
   enregistrer.
3. Dans la section **Profiles**, cliquer sur **Profiles**, puis sur
   **Add profile**.
4. Sélectionner l'utilisateur créé à l'étape 1, saisir sa ville favorite, puis
   cliquer sur **Save**.

Développeur : ajouter une fonctionnalité
----------------------------------------

1. Créer une branche de travail :

   .. code-block:: bash

      git checkout -b ma-fonctionnalite

2. Développer la fonctionnalité et ses tests dans le fichier ``tests.py`` de
   l'application concernée.
3. Vérifier le code en local :

   .. code-block:: bash

      flake8
      pytest --cov=. --cov-report=term-missing

4. Pousser la branche : le pipeline GitHub Actions lance automatiquement le
   linting et les tests.
5. Une fois le pipeline au vert, fusionner la branche sur ``master`` : le site
   est alors automatiquement mis en production (voir :doc:`deployment`).

Développeur : analyser une erreur en production
-----------------------------------------------

1. Se connecter à `Sentry <https://sentry.io>`_ et ouvrir le projet du site.
2. Dans l'onglet **Issues**, ouvrir l'erreur à analyser.
3. Consulter la trace de l'erreur (*stack trace*), l'URL concernée et les
   journaux qui l'ont précédée (*breadcrumbs*).
4. Reproduire l'erreur en local, la corriger et ajouter un test qui la couvre.
5. Déployer la correction en suivant le cas précédent.
