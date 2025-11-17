#!/usr/bin/env python3
"""
Script de test pour récupérer et monter des clips Twitch en format TikTok
"""

import os
import sys
import logging
import time
from datetime import datetime, timedelta
from Adapter.twitch_api import TwitchApi
from Edit.Video_processor import VideoProcessor
import subprocess
import json
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env à la racine
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/test_script.log"),
        logging.StreamHandler()
    ]
)

# Configuration Twitch API - Chargée depuis le fichier .env
CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')

# Configuration du streamer et des paramètres
STREAMER_USERNAME = "sniper_biscuit"  # Nom du streamer pour test complet
MAX_CLIPS = 1  # Nombre maximum de clips à récupérer (1 seul clip pour test)
MIN_DURATION = 10  # Durée minimum en secondes
MAX_DURATION = 31  # Durée maximum en secondes (max 31s)
MIN_VIEWS = 60   # Minimum 60 vues
DAYS_BACK = 3    # Derniers 3 jours

# Paramètres de montage
TARGET_WIDTH = 1080
TARGET_HEIGHT = 1920
WEBCAM_EXTRACTION = True  # True si on veut extraire la webcam
CLIP_FORMAT = "portrait"  # "portrait" pour TikTok, "landscape" pour garder original

def measure_execution_time(func, *args, **kwargs):
    """
    Mesure le temps d'exécution d'une fonction
    
    Args:
        func: La fonction à exécuter
        *args: Arguments de la fonction
        **kwargs: Arguments nommés de la fonction
    
    Returns:
        tuple: (résultat, temps_execution)
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time

def download_clip_with_streamlink(clip_url, output_path):
    """
    Télécharge un clip Twitch avec streamlink
    
    Args:
        clip_url (str): URL du clip Twitch
        output_path (str): Chemin de sauvegarde
    
    Returns:
        bool: True si le téléchargement a réussi
    """
    try:
        # Créer le dossier si nécessaire
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Utiliser le chemin complet vers streamlink dans l'environnement virtuel
        venv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.venv', 'Scripts', 'streamlink.exe')
        
        command = [
            venv_path,
            clip_url,
            "best",
            "-o", output_path,
            "--retry-open", "5",
            "--retry-streams", "5"
        ]
        
        logging.info(f"Téléchargement du clip: {clip_url}")
        result = subprocess.run(command, timeout=600, check=True, capture_output=True, text=True)  # Timeout de 10 minutes
        logging.info(f"Clip téléchargé avec succès: {output_path}")
        return True
        
    except subprocess.TimeoutExpired:
        logging.error(f"Timeout lors du téléchargement: {clip_url}")
        return False
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Erreur lors du téléchargement: {e}")
        logging.error(f"Stderr: {e.stderr}")
        return False
    except Exception as e:
        logging.error(f"Erreur inattendue lors du téléchargement: {e}")
        return False

def get_clips_from_streamer(twitch_api, username, days_back=7):
    """
    Récupère les clips d'un streamer sur une période donnée
    
    Args:
        twitch_api: Instance de TwitchApi
        username (str): Nom d'utilisateur Twitch
        days_back (int): Nombre de jours à remonter
    
    Returns:
        list: Liste des clips récupérés
    """
    logging.info(f"Récupération des clips pour {username}")
    
    # Obtenir l'ID utilisateur
    user_id = twitch_api.getUserId(username)
    if not user_id:
        logging.error(f"Impossible de trouver l'utilisateur: {username}")
        return []
    
    logging.info(f"ID utilisateur trouvé: {user_id}")
    
    # Calculer les dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    # Filtres pour les clips
    filters = {
        "started_at": start_date.isoformat() + "Z",
        "ended_at": end_date.isoformat() + "Z",
        "first": MAX_CLIPS
    }
    
    # Récupérer les clips
    clips_data, execution_time = measure_execution_time(
        twitch_api.getClips, user_id, filters=filters
    )
    
    logging.info(f"Clips récupérés en {execution_time:.2f} secondes")
    logging.info(f"Nombre de clips trouvés: {len(clips_data)}")
    
    # Filtrer par durée et vues
    filtered_clips = []
    for clip in clips_data:
        if (MIN_DURATION <= clip['duration'] <= MAX_DURATION and 
            clip['view_count'] >= MIN_VIEWS):
            filtered_clips.append(clip)
    
    logging.info(f"Clips après filtrage: {len(filtered_clips)}")
    
    # Trier par nombre de vues (décroissant)
    filtered_clips.sort(key=lambda x: x['view_count'], reverse=True)
    
    return filtered_clips

def process_clips(clips):
    """
    Traite et monte les clips en format TikTok
    
    Args:
        clips (list): Liste des clips à traiter
    
    Returns:
        list: Liste des chemins des vidéos traitées
    """
    processed_videos = []
    
    for i, clip in enumerate(clips, 1):
        logging.info(f"Traitement du clip {i}/{len(clips)}: {clip['title']}")
        
        # Chemin de téléchargement
        clip_filename = f"clip_{i}_{clip['id']}.mp4"
        base_dir = os.path.dirname(os.path.abspath(__file__))
        download_path = os.path.join(base_dir, "data", "fetch_clips", clip_filename)
        
        try:
            # Vérifier si le clip est déjà téléchargé
            if os.path.exists(download_path) and os.path.getsize(download_path) > 0:
                logging.info(f"Clip déjà téléchargé, réutilisation: {download_path}")
            else:
                # Télécharger le clip
                success = download_clip_with_streamlink(clip['url'], download_path)
                if not success:
                    logging.warning(f"Échec du téléchargement pour le clip {i}, passage au suivant")
                    continue
            
            # Vérifier que le fichier existe et n'est pas vide
            if not os.path.exists(download_path) or os.path.getsize(download_path) == 0:
                logging.warning(f"Fichier non trouvé ou vide: {download_path}")
                continue
            
            # Traiter la vidéo
            logging.info(f"Début du montage pour le clip {i}")
            video_processor = VideoProcessor(
                clipUrl=download_path,
                webcam_extraction=WEBCAM_EXTRACTION,
                clip_format=CLIP_FORMAT
            )
            
            # Mesurer le temps de traitement
            _, processing_time = measure_execution_time(
                video_processor.process_video, TARGET_WIDTH, TARGET_HEIGHT
            )
            
            logging.info(f"Clip {i} traité en {processing_time:.2f} secondes")
            
            # Ajouter à la liste des vidéos traitées
            base_dir = os.path.dirname(os.path.abspath(__file__))
            processed_video_path = os.path.join(
                base_dir, "data", "processed_clips", f"{video_processor.clipId}_processed.mp4"
            )
            
            if os.path.exists(processed_video_path):
                processed_videos.append({
                    'clip_info': clip,
                    'processed_path': processed_video_path,
                    'processing_time': processing_time
                })
                logging.info(f"Vidéo traitée sauvegardée: {processed_video_path}")
            else:
                logging.error(f"Vidéo traitée non trouvée: {processed_video_path}")
            
        except Exception as e:
            logging.error(f"Erreur lors du traitement du clip {i}: {e}")
            continue
        
        finally:
            # Nettoyer le fichier téléchargé
            if os.path.exists(download_path):
                try:
                    os.remove(download_path)
                    logging.info(f"Fichier temporaire supprimé: {download_path}")
                except Exception as e:
                    logging.warning(f"Impossible de supprimer {download_path}: {e}")
    
    return processed_videos

def main():
    """
    Fonction principale du script
    """
    logging.info("="*50)
    logging.info("DÉBUT DU SCRIPT DE RÉCUPÉRATION ET MONTAGE DE CLIPS")
    logging.info("="*50)
    
    # Vérifier les clés API
    if not CLIENT_ID or not CLIENT_SECRET:
        logging.error("Clés API Twitch manquantes dans le fichier .env")
        logging.error("Assurez-vous que TWITCH_CLIENT_ID et TWITCH_CLIENT_SECRET sont définis dans .env")
        return
    
    try:
        # Créer les dossiers nécessaires
        base_dir = os.path.dirname(os.path.abspath(__file__))
        os.makedirs(os.path.join(base_dir, "data", "fetch_clips"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "data", "processed_clips"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "Edit", "in_process_clips"), exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        
        # Initialiser l'API Twitch
        logging.info("Initialisation de l'API Twitch...")
        twitch_api = TwitchApi(CLIENT_ID, CLIENT_SECRET)
        
        # Récupérer les clips
        logging.info(f"Recherche des clips pour {STREAMER_USERNAME}...")
        clips = get_clips_from_streamer(twitch_api, STREAMER_USERNAME, days_back=DAYS_BACK)
        
        if not clips:
            logging.warning("Aucun clip trouvé pour ce streamer")
            return
        
        # Afficher les informations des clips trouvés
        logging.info("Clips trouvés:")
        for i, clip in enumerate(clips, 1):
            logging.info(f"  {i}. '{clip['title']}' - {clip['duration']}s - {clip['view_count']} vues")
        
        # Traiter les clips
        logging.info("Début du traitement des clips...")
        start_time = time.time()
        processed_videos = process_clips(clips)
        total_time = time.time() - start_time
        
        # Résumé final
        logging.info("="*50)
        logging.info("RÉSUMÉ DU TRAITEMENT")
        logging.info("="*50)
        logging.info(f"Clips récupérés: {len(clips)}")
        logging.info(f"Clips traités avec succès: {len(processed_videos)}")
        logging.info(f"Temps total: {total_time:.2f} secondes")
        
        if processed_videos:
            logging.info("Vidéos traitées:")
            for i, video in enumerate(processed_videos, 1):
                logging.info(f"  {i}. {video['processed_path']} "
                           f"(temps: {video['processing_time']:.2f}s)")
        
        logging.info("SCRIPT TERMINÉ AVEC SUCCÈS")
        
    except KeyboardInterrupt:
        logging.info("Script interrompu par l'utilisateur")
    except Exception as e:
        logging.error(f"Erreur inattendue: {e}")
        raise

if __name__ == "__main__":
    main()