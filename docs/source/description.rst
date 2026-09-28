Description du projet
=====================

Présentation
------------

Orange County Lettings est une start-up de location de biens immobiliers. Le
site permet de consulter des annonces et des profils d'utilisateurs.

Le site est développé avec le framework Django et il est en ligne à
l'adresse suivante : `https://oc-lettings-7w6w.onrender.com
<https://oc-lettings-7w6w.onrender.com>`_.

Fonctionnalités
---------------

Pour les visiteurs :

- consulter la liste des locations ;
- afficher le détail d'une location (titre et adresse complète) ;
- consulter la liste des profils utilisateurs ;
- afficher le détail d'un profil (nom d'utilisateur, prénom, nom, e-mail et
  ville favorite).

Pour les administrateurs, l'interface d'administration de Django permet de
créer, modifier et supprimer les adresses, les locations, les profils et les
utilisateurs.

Objectifs de la refonte
-----------------------

Le site d'origine a fait l'objet d'une refonte technique, sans modification
de son apparence ni de ses fonctionnalités :

- **Architecture modulaire** : le projet monolithique a été découpé en deux
  applications Django, ``lettings`` et ``profiles``. Les données existantes
  ont été conservées grâce à des migrations Django.
- **Qualité du code** : correction des erreurs de linting (``flake8``), de la
  pluralisation dans l'administration (« Addresses ») et ajout de docstrings.
- **Pages d'erreur personnalisées** pour les erreurs 404 et 500.
- **Tests** : tests unitaires et d'intégration avec ``pytest``, pour une
  couverture de code supérieure à 80 %.
- **Surveillance** : journalisation des événements et remontée des erreurs
  vers Sentry.
- **Sécurité** : les données sensibles (clé secrète, DSN Sentry) sont lues
  depuis des variables d'environnement et ne sont plus écrites dans le code.
- **CI/CD** : un pipeline GitHub Actions teste le code, construit une image
  Docker publiée sur Docker Hub et déploie le site sur Render.
