# Python-OC-Lettings-FR — Plan de refonte "Site web 2.0"

> Ce fichier centralise le plan d'action issu du cahier des charges. Aucune modification
> de code n'a été effectuée à sa création — c'est un document de contexte/roadmap à suivre
> phase par phase. Cocher les cases au fur et à mesure de l'avancement réel du travail.

## 0. Contexte du projet (état constaté au 2026-09-09)

- Django 5.2.17 monolithique : une seule app `oc_lettings_site` contenant les modèles
  `Address`, `Letting`, `Profile`, toutes les vues, tous les templates et l'admin.
- Templates à la racine `templates/` (non namespacés par app) : `index.html`,
  `lettings_index.html`, `letting.html`, `profiles_index.html`, `profile.html`, `base.html`.
- `urls.py` : routes `''`, `lettings/`, `lettings/<id>/`, `profiles/`, `profiles/<username>/`,
  `admin/`, toutes déclarées sans namespace, `ROOT_URLCONF = 'oc_lettings_site.urls'`.
- `views.py` contient des blocs de commentaires "lorem ipsum" (placeholders) au-dessus de
  chaque vue — le cahier des charges demande de **conserver les commentaires existants**
  tout en ajoutant des docstrings. À clarifier avant d'y toucher (voir section 8).
- `admin.py` enregistre les 3 modèles sans `verbose_name_plural` → bug de pluralisation
  connu ("Addresss" dans l'admin).
- `settings.py` : `SECRET_KEY` en clair, `DEBUG = True` en dur, pas de variables
  d'environnement, pas de config logging, pas de Sentry.
- `requirements.txt` : seulement `django`, `flake8`, `pytest-django` — manque
  `sentry-sdk`, `python-dotenv` (ou équivalent), `pytest-cov`/`coverage`, et pour la prod
  un serveur WSGI (`gunicorn`) + fichiers statiques (`whitenoise`).
- `setup.cfg` : lint flake8 (`max-line-length = 99`, exclude migrations/venv) — **ne pas
  modifier**. Config pytest : `python_files = tests.py`.
- `oc_lettings_site/tests.py` : test factice (`assert 1`), pas de couverture réelle.
- Pas de pages d'erreur 404/500 personnalisées.
- Pas de CI/CD (`.github/workflows` absent), pas de `Dockerfile`.
- Pas de dossier `docs/` (Sphinx/Read the Docs).
- `README.md` : pas de section "Déploiement".
- Dépôt GitHub : `github.com/GuillaumeChiron/Python-OC-Lettings-FR`, branche unique `master`.
- Fichier `oc-lettings-site.sqlite3` versionné dans git (actuellement modifié selon
  `git status`) — à garder en tête pour le futur `.gitignore` / la stratégie de données.

**Contrainte transverse rappelée par le cahier des charges** : c'est une refonte pure,
le site (apparence + fonctionnalités, admin inclus) ne doit pas changer.

---

## Phase 1 — Refonte architecturale (apps `lettings` / `profiles`)

- [ ] Créer l'app `lettings` (`python manage.py startapp lettings`) avec les modèles
      `Address` et `Letting` (recopiés depuis `oc_lettings_site/models.py`).
- [ ] Créer l'app `profiles` avec le modèle `Profile`.
- [ ] Ajouter les deux apps à `INSTALLED_APPS` dans `settings.py`.
- [ ] Générer les migrations initiales de `lettings` et `profiles` (`makemigrations`).
- [ ] Écrire une **migration de données Django** (`RunPython`, pas de SQL brut) qui copie
      les lignes des anciennes tables (`oc_lettings_site_address`, `_letting`, `_profile`)
      vers les nouvelles tables. Attention à l'ordre (Address avant Letting, à cause de la
      FK) et à la préservation des PK existantes.
- [ ] Une fois les données migrées et vérifiées, écrire une migration Django qui supprime
      les modèles/tables historiques de `oc_lettings_site` (migration avec
      `DeleteModel`/dépendances correctes, toujours pas de SQL brut).
- [ ] **Exécuter `python manage.py migrate` immédiatement après avoir écrit ces deux
      migrations** (copie des données + suppression des anciennes tables) — ne pas
      attendre le nettoyage final. Valider tout de suite après que les données sont
      identiques (comparer un dump avant/après, compter les lignes par table). C'est ce
      `migrate` qui fait basculer réellement la base ; les étapes suivantes (déplacement
      des templates/vues/urls/admin) doivent être testées contre cette base déjà migrée,
      sinon les nouvelles vues (`Letting.objects.all()`, etc.) n'ont rien à afficher.
- [ ] Déplacer les templates :
      - `templates/lettings_index.html` → `lettings/templates/lettings/index.html`
        (renommer la vue `lettings_index` → `index`)
      - `templates/letting.html` → `lettings/templates/lettings/letting.html`
      - `templates/profiles_index.html` → `profiles/templates/profiles/index.html`
        (renommer la vue `profiles_index` → `index`)
      - `templates/profile.html` → `profiles/templates/profiles/profile.html`
      - Garder `base.html` et `index.html` (page d'accueil globale) dans
        `oc_lettings_site/templates/` ou `templates/` racine (couche "site").
- [ ] Déplacer les vues correspondantes dans `lettings/views.py` et `profiles/views.py`,
      avec les nouveaux noms (`index` au lieu de `lettings_index`/`profiles_index`).
- [ ] Créer `lettings/urls.py` et `profiles/urls.py` avec `app_name = 'lettings'` /
      `'profiles'` (namespaces), et les inclure depuis `oc_lettings_site/urls.py` via
      `include()`, en gardant `ROOT_URLCONF` inchangé.
- [ ] Mettre à jour tous les `{% url %}` dans les templates avec le préfixe de namespace
      (`lettings:index`, `lettings:letting`, `profiles:index`, `profiles:profile`, etc.)
      et tous les `reverse()`/`redirect()` équivalents dans le code.
- [ ] Déplacer l'admin : `lettings/admin.py` (Address, Letting), `profiles/admin.py`
      (Profile). Supprimer les enregistrements dans `oc_lettings_site/admin.py`.
- [ ] Nettoyer `oc_lettings_site` : supprimer `models.py` (vidé), `admin.py` (vidé) si
      plus rien à y déclarer, anciennes migrations obsolètes une fois la suppression de
      table actée, et tout fichier devenu inutile.
- [ ] Vérifier que `oc_lettings_site` garde uniquement ce qui reste global : `settings.py`,
      `urls.py` racine, `wsgi.py`/`asgi.py`, vue `index` (accueil), template `index.html`.
- [ ] Re-vérification finale : relancer `makemigrations` (aucune migration en attente ne
      doit apparaître) et confirmer une dernière fois qu'aucune donnée n'a été perdue
      depuis le `migrate` effectué plus haut (le `migrate` lui-même n'est PAS refait ici,
      il a déjà eu lieu juste après les migrations de copie/suppression).
- [ ] Vérifier manuellement (site + admin) que rien n'a changé visuellement ni
      fonctionnellement.
- [ ] Vérifier que `flake8` et `pytest` fonctionnent toujours depuis la racine du projet.

## Phase 2 — Qualité de code et robustesse

- [ ] Corriger toutes les erreurs `flake8` (sans modifier `setup.cfg`, en conservant les
      commentaires existants — voir section 8 pour la question des commentaires lorem
      ipsum dans les vues).
- [ ] Corriger la pluralisation "Addresss" → "Addresses" : ajouter
      `class Meta: verbose_name_plural = "addresses"` sur le modèle `Address` (dans
      l'app `lettings`), puis vérifier qu'aucune autre pluralisation n'est cassée sur le
      site (recherche globale des libellés générés par Django).
- [ ] Créer des pages d'erreur personnalisées : `templates/404.html`, `templates/500.html`
      (cohérentes avec `base.html`/le design du site), `DEBUG = False` requis pour les
      voir en conditions réelles ; ajouter des vues/handlers si besoin
      (`handler404`, `handler500` dans `oc_lettings_site/urls.py`).
- [ ] Ajouter des docstrings sur chaque module, classe et fonction (modèles, vues,
      apps.py, admin.py, urls.py) dans `lettings`, `profiles`, et `oc_lettings_site`.
- [ ] Écrire les tests par app (dans `lettings/tests.py` et `profiles/tests.py`, ou
      des sous-modules `tests/` dédiés si plus lisible) :
      - Tests de modèles (`__str__`, validators, `Meta`).
      - Tests de vues (rendu, contexte, codes HTTP, 404 sur objet inexistant).
      - Tests d'URLs (résolution des routes namespacées).
      - Tests d'intégration de bout en bout (parcours utilisateur simple).
- [ ] Ajouter `pytest-cov` (ou `coverage`) aux dépendances de dev, configurer la
      commande de mesure de couverture, et vérifier que la couverture globale dépasse
      80 % (`pytest --cov=. --cov-report=term-missing`).

## Phase 3 — Sentry et logging

- [ ] Installer `sentry-sdk` (ajout à `requirements.txt`, séparer éventuellement
      `requirements-dev.txt` si on veut isoler flake8/pytest/coverage du runtime prod).
- [ ] Configurer Sentry dans `settings.py` via `sentry_sdk.init(...)`, DSN lu depuis une
      variable d'environnement (`SENTRY_DSN`), jamais en dur dans le code.
- [ ] Mettre en place `python-dotenv` (ou équivalent) + fichier `.env.example` (sans
      valeurs réelles) pour documenter les variables attendues ; s'assurer que `.env`
      réel est dans `.gitignore`.
- [ ] Déplacer `SECRET_KEY`, `DEBUG`, et toute autre donnée sensible vers des variables
      d'environnement avec des valeurs par défaut sûres pour le développement local.
- [ ] Configurer le module `logging` standard Django (dict `LOGGING` dans `settings.py`)
      avec au moins un handler console + un handler qui relaie vers Sentry.
- [ ] Insérer des logs aux endroits stratégiques : vues (accès, objet non trouvé),
      blocs `try/except`, points de validation de données (formulaires/modèles).
- [ ] Documenter dans le README (section dédiée) comment un successeur active Sentry
      localement/en prod (variables d'env à définir, où les récupérer).

## Phase 4 — Pipeline CI/CD et déploiement

- [ ] Choisir l'hébergeur de production (Render / AWS Elastic Beanstalk ou App Runner /
      Azure App Service, etc.) — **décision à valider avec l'utilisateur avant
      implémentation**, impacte le job de déploiement.
- [ ] Écrire `Dockerfile` (image de prod : dépendances, collectstatic, gunicorn) et
      idéalement un `docker-compose.yml` pour lancer facilement en local.
      - ⚠️ `SECRET_KEY` : ne **jamais** écrire `ENV SECRET_KEY=...` dans le Dockerfile
        (la clé serait gravée dans l'image publiée sur Docker Hub). La passer au lancement :
        `docker run --env-file .env ...` ou `-e SECRET_KEY=...`. Ne pas copier `.env`
        dans l'image (`.dockerignore`).
      - ⚠️ `settings.py` lève `ImproperlyConfigured` si `SECRET_KEY` est absente (fail fast) :
        `collectstatic` au build a donc besoin d'une clé temporaire limitée à la commande :
        `RUN SECRET_KEY=build-only python manage.py collectstatic --noinput`.
- [ ] Mettre en place GitHub Actions (`.github/workflows/ci.yml` ou similaire) avec 3 jobs :
      1. **build-and-test** : setup Python, install `requirements.txt` (+ dev deps),
         `flake8`, `pytest` avec couverture, échec si couverture < 80 %. Se déclenche sur
         toute branche/PR.
         ⚠️ La CI n'a pas de `.env` : sans `SECRET_KEY`, 16 tests échouent
         (`ImproperlyConfigured`, constaté le 2026-09-24). Définir une clé factice dans le
         YAML du job (`env: SECRET_KEY: cle-factice-pour-les-tests`) — non sensible, elle ne
         sert qu'aux tests. La vraie clé de prod va uniquement dans les secrets de l'hébergeur.
      2. **containerize** : dépend du succès du job 1, uniquement sur push vers `master` ;
         build de l'image Docker, tag avec le hash de commit (+ `latest`), push vers
         Docker Hub (credentials via secrets GitHub Actions).
      3. **deploy** : dépend du succès du job 2, uniquement sur push vers `master` ; déploie
         l'image sur l'hébergeur choisi.
- [ ] Vérifier que les branches autres que `master` ne déclenchent que le job 1 (pas de
      containerisation, pas de déploiement).
- [ ] Documenter la commande unique permettant de pull l'image depuis Docker Hub et de
      lancer le site en local avec uniquement Docker (ex. `docker run ...` ou
      `docker compose up`).
- [ ] Configurer les secrets nécessaires côté GitHub (Docker Hub, credentials hébergeur,
      `SENTRY_DSN`, `SECRET_KEY` de prod, etc.) — lister précisément les noms attendus
      dans la documentation, sans jamais les committer.
- [ ] Après déploiement, valider explicitement le chargement des fichiers statiques en
      prod (CSS/JS/fonts/images) et l'apparence de l'admin (attention particulière car
      le CTO utilise l'admin fréquemment).
- [ ] Ajouter au `README.md` une section "Déploiement" : récapitulatif du fonctionnement,
      prérequis/configuration nécessaires, étapes precises pour déployer.

## Phase 5 — Documentation technique (Sphinx / Read the Docs)

- [ ] `pip install sphinx` (+ éventuellement `sphinx-rtd-theme`), ajouter aux dépendances
      de dev.
- [ ] Créer le dossier `docs/`, lancer `sphinx-quickstart` dedans.
- [ ] Rédiger le contenu (dans `docs/source/index.rst` + fichiers inclus) :
      - Description du projet.
      - Instructions d'installation.
      - Guide de démarrage rapide.
      - Technologies et langages utilisés.
      - Structure de la base de données et modèles de données (schéma `lettings`/
        `profiles`).
      - Description des interfaces (routes/vues, admin).
      - Guide d'utilisation avec cas d'utilisation concrets.
      - Procédures de déploiement et de gestion de l'application (renvoi/synthèse de la
        section README "Déploiement").
- [ ] Générer et vérifier localement (`make html`, ouvrir `build/html/index.html`).
- [ ] Créer/connecter le projet sur Read the Docs (import du repo GitHub), configurer le
      build automatique sur push.
- [ ] Ajouter un badge/lien Read the Docs dans le `README.md` une fois l'URL disponible.

---

## Ordre de réalisation recommandé

1. Phase 1 (archi) — base de tout le reste, à valider avant de continuer.
2. Phase 2 (qualité/tests) — nécessaire pour que la CI (Phase 4) ait quelque chose à
   vérifier avec un seuil de couverture fiable.
3. Phase 3 (Sentry/logging) — peut être menée en parallèle de la Phase 2.
4. Phase 4 (CI/CD/déploiement) — dépend de 1, 2 et 3 (tests + couverture + config env
   pour les secrets).
5. Phase 5 (doc Sphinx) — peut démarrer dès que l'architecture (Phase 1) est stabilisée,
   à finaliser après le déploiement pour documenter l'état réel.

---

## Points à clarifier avec l'utilisateur avant d'implémenter

- **Commentaires "lorem ipsum" dans `oc_lettings_site/views.py`** : le cahier des charges
  dit de conserver les commentaires existants tout en documentant via docstrings. Faut-il
  garder ces lorem ipsum tels quels au-dessus des nouvelles fonctions (dans
  `lettings/views.py` / `profiles/views.py`), les remplacer, ou les considérer comme du
  bruit à nettoyer malgré la consigne générale ?
- **Hébergeur de production** (Render / AWS / Azure / autre) — impacte directement le job
  de déploiement du pipeline CI/CD.
- **Gestion du fichier `oc-lettings-site.sqlite3` versionné dans git** : le garder versionné
  (actuellement modifié selon `git status`) ou basculer vers une base non versionnée +
  fixtures/seed script pour la démo ?
- **Compte Docker Hub et compte Sentry** : à créer/fournir par l'utilisateur (les
  identifiants ne doivent jamais être en dur dans le code, seulement en secrets CI /
  variables d'environnement).
- **Read the Docs** : compte à créer et connecter au repo GitHub
  (`GuillaumeChiron/Python-OC-Lettings-FR`).

## Rappels transverses (contraintes du cahier des charges)

- Ne jamais utiliser de SQL brut dans les fichiers de migration Django.
- Ne pas modifier `setup.cfg` (config flake8).
- Conserver les commentaires existants dans le code (cf. point à clarifier ci-dessus).
- Le site (apparence + fonctionnalités) et l'admin ne doivent pas changer visuellement.
- `pytest` et `flake8` doivent rester utilisables en local à chaque étape.
- Aucune donnée sensible (SECRET_KEY, DSN Sentry, credentials Docker Hub/hébergeur) ne
  doit être stockée dans le code source — uniquement des variables d'environnement /
  secrets CI.
- Couverture de tests globale à maintenir strictement > 80 %.
