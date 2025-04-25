# Lancement du projet

## Backend

1. Créer un environnement virtuel avec Python 3.11 :
    ```bash
    python -m venv venv
    ```

2. Activer l'environnement virtuel :
    - Sur Windows :
        ```bash
        .\venv\Scripts\activate
        ```
    - Sur macOS/Linux :
        ```bash
        source venv/bin/activate
        ```

3. À la racine du projet `GROOT`, exécuter la commande suivante pour installer le projet sous forme de package :
    ```bash
    pip install -e .
    ```

4. Tester l'installation de **Streamlink** :
    - Exécuter la commande suivante dans la console :
      ```bash
      streamlink
      ```
    - Si cette commande n'est pas reconnue, consultez la section "Bug courant et solutions" ci-dessous.

### Lancement du backend en mode debug

5.1 Lancer le backend en mode debug avec le script `run.py` :

    ```bash
    python run.py
    ```

5.2 Ajouter des points d'arrêt dans le code (cela concerne uniquement le backend, pas le frontend) et interagir avec les parties du frontend qui appellent les fonctions du backend.

### Lancement du backend en mode normal

5.3 Lancer le backend en mode normal avec le script `run` :

    ```bash
    python run
    ```

## Frontend

1. Se rendre dans le dossier `GROOT/twitok_website` avec la commande :
    ```bash
    cd twitok_website
    ```

2. Installer les dépendances :
    ```bash
    npm install
    ```

3. Lancer le projet en mode développement :
    ```bash
    npm run dev
    ```

4. Ouvrir le lien affiché sur le navigateur.

## Bugs courants et solutions

### Bug Streamlink

- **Symptôme** : Une pop-up "Impossible de récupérer les clips" et un code 500 `Internal Server Error` dans la console du navigateur.

- **Diagnostic** :
    1. Interrompre le backend et exécuter la commande suivante dans le terminal :
        ```bash
        streamlink
        ```
    2. Si cette commande n'est pas reconnue, cela signifie que le problème vient de **Streamlink**. Si la commande fonctionne, le problème est ailleurs.

- **Rôle de Streamlink** :
    - Streamlink est utilisé dans l'API Twitch pour télécharger les clips dans le dossier `fetch_clips`. C'est une commande terminal que l'on exécute via Python.

- **Problème** : Bien que `streamlink` soit inclus dans le fichier `requirements.txt` et installé dans les bibliothèques du venv (`.venv/Lib/site-packages/streamlink`), l'exécutable `streamlink` n'est pas présent dans le dossier `.venv/Scripts` où se trouvent les exécutables des bibliothèques installées.

### Solution

1. Répéter toutes les étapes d'installation du backend.
2. Supprimer tout fichier faisant référence à `streamlink` dans le dossier `.venv/Lib/site-packages` et exécuter la commande suivante dans le terminal :
    ```bash
    pip install streamlink
    ```
3. **Attention** : Assurez-vous d'être dans l'environnement virtuel (`venv`) pour que toutes les dépendances soient correctement accessibles.


