Interfaces
==========

Architecture du projet
----------------------

Le projet est découpé en trois applications Django :

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Application
     - Contenu
   * - ``oc_lettings_site``
     - Configuration globale (``settings.py``, ``urls.py`` racine, ``wsgi.py``)
       et page d'accueil
   * - ``lettings``
     - Modèles ``Address`` et ``Letting``, vues, templates et administration
       des locations
   * - ``profiles``
     - Modèle ``Profile``, vues, templates et administration des profils

Les templates communs (``base.html``, ``index.html``, ``404.html``,
``500.html``) se trouvent dans le dossier ``templates/`` à la racine. Les
templates propres à chaque application se trouvent dans
``<application>/templates/<application>/``.

Routes et vues
--------------

Les routes de ``lettings`` et ``profiles`` sont déclarées dans le
``urls.py`` de chaque application, avec un espace de noms (``app_name``), et
incluses dans le ``urls.py`` racine avec ``include()``.

.. list-table::
   :header-rows: 1
   :widths: 25 20 25 30

   * - URL
     - Nom de la route
     - Vue
     - Template
   * - ``/``
     - ``index``
     - ``oc_lettings_site.views.index``
     - ``index.html``
   * - ``/lettings/``
     - ``lettings:index``
     - ``lettings.views.index``
     - ``lettings/index.html``
   * - ``/lettings/<letting_id>/``
     - ``lettings:letting``
     - ``lettings.views.letting``
     - ``lettings/letting.html``
   * - ``/profiles/``
     - ``profiles:index``
     - ``profiles.views.index``
     - ``profiles/index.html``
   * - ``/profiles/<username>/``
     - ``profiles:profile``
     - ``profiles.views.profile``
     - ``profiles/profile.html``
   * - ``/admin/``
     - ``admin:index``
     - Administration Django
     - Templates de l'admin

Exemple d'utilisation d'une route dans un template :

.. code-block:: html+django

   <a href="{% url 'lettings:letting' letting_id=letting.id %}">{{ letting.title }}</a>

Détail des vues
~~~~~~~~~~~~~~~

``lettings.views.index``
   Récupère toutes les locations et les transmet au template dans la variable
   ``lettings_list``.

``lettings.views.letting``
   Récupère la location dont l'identifiant est ``letting_id`` et transmet au
   template son titre (``title``) et son adresse (``address``). Renvoie une
   erreur 404 si la location n'existe pas.

``profiles.views.index``
   Récupère tous les profils et les transmet au template dans la variable
   ``profiles_list``.

``profiles.views.profile``
   Récupère le profil de l'utilisateur ``username`` et le transmet au template
   dans la variable ``profile``. Renvoie une erreur 404 si le profil n'existe
   pas.

Pages d'erreur
--------------

Des pages personnalisées, cohérentes avec le design du site, remplacent les
pages d'erreur par défaut de Django :

- ``templates/404.html`` : page ou objet introuvable ;
- ``templates/500.html`` : erreur interne du serveur.

.. note::

   Ces pages ne s'affichent qu'avec ``DEBUG=False``. En mode ``DEBUG=True``,
   Django affiche à la place sa page de débogage détaillée.

Interface d'administration
--------------------------

L'administration Django est accessible sur ``/admin/`` avec un compte
administrateur. Elle permet de gérer :

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Section
     - Modèle
     - Enregistré dans
   * - Lettings
     - ``Address``, ``Letting``
     - ``lettings/admin.py``
   * - Profiles
     - ``Profile``
     - ``profiles/admin.py``
   * - Authentication and Authorization
     - ``User``, ``Group``
     - Fourni par Django

Pour créer un nouveau compte administrateur :

.. code-block:: bash

   python manage.py createsuperuser

Journalisation et Sentry
------------------------

Les vues utilisent le module ``logging`` de Python :

- niveau ``INFO`` lors de la consultation d'une liste (locations ou profils) ;
- niveau ``WARNING`` lorsqu'une location ou un profil demandé est introuvable.

Les journaux sont affichés dans la console. Lorsque la variable
``SENTRY_DSN`` est définie, Sentry reçoit en plus :

- les erreurs non gérées (exceptions) ;
- un événement pour chaque journal de niveau ``WARNING`` ou supérieur ;
- les journaux de niveau ``INFO``, joints aux événements comme contexte
  (*breadcrumbs*).

Aucune donnée personnelle des utilisateurs n'est envoyée à Sentry
(``send_default_pii=False``).
