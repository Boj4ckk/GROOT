# GROOT - Generate, Render, Optimize, Output, Transmit

### L'objectif de GROOT est d'aider les petits et moyens créateurs de contenu en live sur des plateformes comme Twitch à générer automatiquement du contenu au format court (TikTok) à partir des moments forts de leurs lives. Ainsi, ils n'auront pas à consacrer un temps conséquent à la sélection et au montage de ces moments, ni à engager une tierce personne pour le faire à leur place.


### Fonctionnalités du projet, ordonnées par flux de travail :

#### Dans le cadre de ce projet, nous utilisons Python pour effectuer tout le traitement logique de l'application. Python permet de gérer l'ensemble des opérations nécessaires à la récupération, au traitement et à la publication du contenu.

##### Avant de détailler les fonctionnalités, voici quelques termes clés utilisés dans ce projet :

#### Vocabulaire :

##### Streamer : créateur de contenu sur une plateforme de live (Twitch).
##### Clip : courte vidéo (maximum 1 minute 30) issue d'un moment en live.
##### Webcam : Vidéo montrant le visage du streamer pendant son live, souvent utilisée pour personnaliser l'expérience et interagir avec les spectateurs.
##### Gameplay : Contenu vidéo montrant l'écran du jeu ou l'activité du streamer pendant le live.
##### Web Scraping : Technique d'extraction de données depuis un site web en automatisant la navigation et les interactions avec le site à l'aide d'un programme.


##### 1 . Service de récupération de clips Twitch : Ce service permet de récupérer des clips en fonction de divers critères personnalisables tels que le nom du streamer, le jeu vidéo, la durée du clip, le nombre de vues et la date de sortie du clip. Cette étape est réalisée à l'aide de l'API de Twitch, qui permet, grâce à des requêtes spécifiques, de récupérer les clips correspondants aux critères définis.[NE PAS UTILISER LE CHAMP GAME CAR BACKEND PAS ENCORE OPTIMAL]

##### 2. Montage vidéo pour le format court (TikTok) : Cette fonctionnalité se divise en deux parties principales. La première consiste à extraire la webcam du streamer et le contenu vidéo, autrement appelé gameplay. La deuxième partie consiste à utiliser ces deux éléments extraits pour créer la vidéo finale au format souhaité, 9:16, adapté à TikTok.

##### Il est également possible de réaliser le montage sans extraction de la webcam, car bien que celle-ci soit très prisée par les créateurs de contenu en live, elle n'est pas obligatoire. De plus, une option permet de monter la vidéo au format paysage, bien que ce format soit moins recommandé par TikTok. Toutefois, la liberté de création est un objectif primordial chez GROOT, et nous souhaitons offrir cette flexibilité aux utilisateurs.

##### 3. Mise en ligne de la vidéo montée sur TikTok à l'aide de web scraping
##### L'éligibilité à l'API TikTok étant trop longue, cette fonctionnalité repose sur l'utilisation du web scraping. Plusieurs actions automatisées sont réalisées via un navigateur afin de télécharger automatiquement la vidéo sur TikTok. Ce processus permet de contourner les limitations de l'API et de garantir une mise en ligne rapide et efficace des vidéos créées.


### Répartition des tâches pour la réalisation du projet (Yazid, Hugo)
#### Les tâches réalisées seront marquées par l'initiale de la personne responsable :

#### Y : Fonctionnalité de récupération de clips.
#### Y : Fonctionnalité de montage vidéo.
#### H : Création de l'API TikTok (à l'aide de web scraping).
#### H : Création de la page Login.
#### Y : Création de la page Home.
#### Y : Création de la page Register.
#### Y : Création de la page Filtrate.
#### H : Création de la page Studio.
#### H : Création de la page TiktokPost.
#### Y/H : Création de la base de données (bdd.py, application Flask).
#### Y/H : Création du fichier router.js.
#### Y/H : Design de l'application sur Figma.


### Organisation
#### Nous avons utilisé GitHub pour suivre et gérer l'avancement du projet. Dès le début, un compte rendu des tâches à réaliser pour l'application a été établi, mais ce dernier a naturellement évolué au fil du temps en fonction des besoins du projet. Pour chaque fonctionnalité de l'application, nous avons dédié une branche spécifique sur GitHub sur laquelle nous avons travaillé, avant de la fusionner une fois la fonctionnalité développée. Nous avons également appliqué la même méthode pour la gestion des bugs, en créant des branches spécifiques pour chaque bug, puis en les fusionnant une fois les problèmes corrigés.

### Difficultés rencontrées
#### Les premières difficultés que nous avons rencontrées étaient d'ordre technique. En effet, il a fallu trouver les bonnes bibliothèques de développement pour mener à bien le projet. Nous avons exploré plusieurs outils différents, notamment pour la détection faciale afin d'extraire la webcam du streamer. Il y a également eu des contretemps concernant l'éligibilité à l'utilisation de certains outils, comme l'API de TikTok, ce qui nous a contraints à nous adapter et à développer notre propre API TikTok. De plus, nous avons rencontré de nombreux problèmes d'architecture de dossiers qu'il a fallu résoudre pour assurer le fonctionnement optimal de l'application, notamment en ce qui concerne le dossier des clips.

### Etapes pour lancer notre application 

#### Prérequis d'installation : 
##### Installer Node.js
##### Installer python version 3.11.9

##### télécharger notre fichier zip 
##### Allez dans le dossier ou vous allez faire vos test, pour notre part on se place dans `Sdn` dans notre explorateur de fichiers. Puis : 
   ##### -> Créer un dossier du nom de votre choix, on a choisi pour la démonstration `test_twitok`. 
   ##### -> Entrez dans `test_twitok` et placez-y votre fichier zip. 
   ##### -> Faites un clic droit sur votre fichier zip et sélectionnez "Extraire ici". Il est important de bien "extraire ici" et non pas "Extraire Tout". 
   ##### <i> Résumé : Répertoire courant `..../sdn/test_twitok` et il doit y avoir le fichier zip, ainsi que le dossier qui contient notre projet (celui-ci doit s'appeler "GROOT-main"). </i> 
   ##### -> Créez un dossier appelé 'clips' dans le dossier courant. (dossier courant = `..../sdn/test_twitok`)
   ##### -> Renommez le dossier 'GROOT-main' en 'GROOT' (Désolé pour ces deux dernières étapes peu communes)
   ##### -> ouvrez un terminal et naviguez vers `twitok_website`. Dans notre cas voici notre terminal : `PS C:\Users\Sdn\test_twitok> cd GROOT` puis `PS C:\Users\Sdn\test_twitok\GROOT> cd twitok_website`.
   ##### -> Vous voici maintenant dans le répertoire `twitok_website` qui contient toute la partie VueJs. tapez la commande `npm install`. 
   ##### -> tapez la commande `npm run dev`
   ##### Le serveur doit être operationnel.
    //
   ##### -> Ouvrez en paralèle un autre terminal. 
   ##### -> Vous avez normalement en pré-requis installé la version 3.11.9 de Python. Lancez la commande suivante dans votre terminal : `PS C:\Users\Sdn\test_twitok>py -3.11 -m venv Twitok_venv` 
   ##### -> Ensuite tapez la commande suivante dans ce même terminal : `PS C:\Users\Sdn\test_twitok>.\Twitok_venv\Scripts\activate`
   ##### -> Vous devriez etre comme ceci : `(Twitok_venv) PS C:\Users\Sdn\test_twitok>` 
   ##### -> Vous pouvez taper cette commande pour etre sur que votre environnement virtuel est bien configuré avec la bonne version de python : `(Twitok_venv) PS C:\Users\Sdn\test_twitok>python --version` (la version doit donc etre la 3.11.9)
   ##### -> Entrez maintenant la commande suivante : `(Twitok_venv) PS C:\Users\Sdn\test_twitok\GROOT>pip install -r requirements.txt`
   ##### -> Enfin, entrez la commande suivante : `(Twitok_venv) PS C:\Users\Sdn\test_twitok> watchmedo auto-restart --patterns="*.py" --recursive -- python -m GROOT.bdd.bdd`
   ##### Le serveur Flask doit être opérationnel. 
    
   ##### Il ne vous reste plus qu'à aller sur votre navigateur et taper http://localhost:5173 






### BONUS : Lien du figma pour visualiser le design futur de l'application.
##### https://www.figma.com/design/b9Hm6yQ9WsMw77VkCh9F25/Untitled?node-id=0-1&p=f&t=6dAuwtAn41czKliy-0






