## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Variables d'environnement

Le projet utilise un fichier `.env` (non versionné, à la racine du projet) pour sa configuration sensible.

- Copier `.env.example` vers `.env` : `cp .env.example .env`
- Renseigner les valeurs suivantes dans `.env` :
  - `SECRET_KEY` : clé de signature interne à Django (sessions, tokens CSRF, etc.), obligatoire. Générer une valeur avec :
    `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
  - `DEBUG` : `True` en local pour afficher les erreurs détaillées, doit être `False` en production.
  - `ALLOWED_HOSTS` : noms de domaine autorisés à servir le site, séparés par des virgules. Valeur par défaut : `localhost,127.0.0.1`.
  - `SENTRY_DSN` : optionnelle. Si elle est absente, Sentry est simplement désactivé (le site fonctionne normalement, sans remontée d'erreurs). Pour l'obtenir :
    1. Créer un compte sur [sentry.io](https://sentry.io).
    2. Créer un projet de plateforme **Django**.
    3. Récupérer le DSN dans le projet : **Settings → Projects → *(votre projet)* → Client Keys (DSN)**.

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`

## Déploiement

Le site est en ligne à l'adresse : https://oc-lettings-7w6w.onrender.com

### Fonctionnement

Le déploiement est entièrement automatisé par un pipeline GitHub Actions (`.github/workflows/ci.yml`), composé de 3 jobs qui s'enchaînent. Un job ne démarre que si le précédent a réussi.

```
build-and-test  →  containerize  →  deploy
```

1. **build-and-test** : installe les dépendances, lance `flake8` puis `pytest`. Le job échoue si un test échoue ou si la couverture de tests est inférieure à 80 %.
2. **containerize** : construit l'image Docker et la publie sur Docker Hub (`guillaumechiron/oc-lettings`) avec deux tags : `latest` et le hash du commit.
3. **deploy** : déclenche le redéploiement du service sur Render, qui récupère la nouvelle image `latest` et redémarre le site.

| Événement | Jobs exécutés |
|---|---|
| Push sur une autre branche que `master` | `build-and-test` uniquement |
| Pull request | `build-and-test` uniquement |
| Push sur `master` (y compris un merge) | `build-and-test` → `containerize` → `deploy` |

Du code qui ne passe pas les tests ne peut donc jamais être publié ni mis en production.

### Prérequis

- Un compte [GitHub](https://github.com) avec les droits d'administration sur ce repository (pour gérer les secrets).
- Un compte [Docker Hub](https://hub.docker.com).
- Un compte [Render](https://render.com).
- Un compte [Sentry](https://sentry.io) (optionnel, pour la remontée des erreurs en production).
- Docker installé en local (uniquement pour lancer ou construire l'image sur sa machine).

### Configuration

Aucune donnée sensible n'est stockée dans le code : elles sont renseignées dans les secrets GitHub et dans les variables d'environnement Render.

#### Secrets GitHub Actions

À créer dans **Settings → Secrets and variables → Actions → New repository secret** :

| Nom | Rôle | Où l'obtenir |
|---|---|---|
| `DOCKERHUB_USERNAME` | Nom d'utilisateur Docker Hub | Votre compte Docker Hub |
| `DOCKERHUB_TOKEN` | Token d'accès pour publier l'image | Docker Hub : **Account settings → Personal access tokens**, permissions **Read & Write** |
| `RENDER_DEPLOY_HOOK_URL` | URL qui déclenche un redéploiement | Render : **votre service → Settings → Deploy Hook** |

#### Service Render (mise en place initiale, une seule fois)

1. Sur Render : **New + → Web Service → Existing Image**.
2. Image URL : `docker.io/guillaumechiron/oc-lettings:latest`.
3. Region : **Frankfurt (EU)**, Instance Type : **Free**.
4. Renseigner les variables d'environnement ci-dessous, puis cliquer sur **Deploy Web Service**.

| Variable | Valeur |
|---|---|
| `SECRET_KEY` | Une clé dédiée à la production, différente de la clé locale (voir la commande de génération dans la section *Variables d'environnement*) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | L'adresse du service, sans `https://` (ex. `oc-lettings-7w6w.onrender.com`) |
| `SENTRY_DSN` | Le DSN du projet Sentry, sans guillemets |

La variable `PORT` est fournie automatiquement par Render : il ne faut pas la définir.

### Déployer une nouvelle version

1. Créer une branche de travail : `git checkout -b ma-branche`
2. Développer, puis pousser la branche : `git push -u origin ma-branche`. Le job `build-and-test` vérifie le code.
3. Une fois le job au vert, merger la branche sur `master` (pull request sur GitHub, ou `git checkout master`, `git merge ma-branche`, `git push`).
4. Suivre l'exécution des 3 jobs dans l'onglet **Actions** de GitHub, puis le déploiement dans l'onglet **Events** du service Render.

Remarque : la base SQLite est embarquée dans l'image Docker. Les modifications faites via l'admin en production sont perdues à chaque redéploiement.

### Lancer le site en local avec Docker

Une seule commande suffit pour récupérer l'image depuis Docker Hub et lancer le site :

```
docker run --rm -p 8000:8000 -e SECRET_KEY=une-cle-de-test guillaumechiron/oc-lettings:latest
```

Puis aller sur `http://localhost:8000`. `Ctrl+C` pour arrêter le conteneur.

Pour utiliser sa propre configuration (Sentry, etc.), remplacer `-e SECRET_KEY=...` par `--env-file .env`. Attention : avec Docker, les valeurs du fichier `.env` ne doivent pas être entourées de guillemets.

Pour construire l'image à partir du code local :

```
docker build -t oc-lettings .
docker run --rm -p 8000:8000 -e SECRET_KEY=une-cle-de-test oc-lettings
```
