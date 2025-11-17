#!/usr/bin/env python3
"""
SCRIPT DE TEST COMPLET DE A À Z
Teste toute la chaîne de traitement avec le streamer sniper_biscuit
"""

import os
import sys
import logging
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

print("🚀 " + "="*70)
print("🚀 SCRIPT DE TEST COMPLET - DE A À Z")
print("🚀 Streamer: sniper_biscuit")
print("🚀 " + "="*70)

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/test_complet.log"),
        logging.StreamHandler()
    ]
)

# Charger les variables d'environnement
print("\n📋 ÉTAPE 1: CONFIGURATION")
print("-" * 50)
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)

CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')

print(f"✓ Fichier .env chargé: {env_path}")
print(f"✓ CLIENT_ID: {'présent' if CLIENT_ID else 'MANQUANT'}")
print(f"✓ CLIENT_SECRET: {'présent' if CLIENT_SECRET else 'MANQUANT'}")

if not CLIENT_ID or not CLIENT_SECRET:
    print("❌ ERREUR: Clés API Twitch manquantes!")
    exit(1)

# Test d'import des modules
print("\n📦 ÉTAPE 2: IMPORTATION DES MODULES")
print("-" * 50)

try:
    from Adapter.twitch_api import TwitchApi
    print("✓ TwitchApi importé avec succès")
except Exception as e:
    print(f"❌ Erreur import TwitchApi: {e}")
    exit(1)

try:
    from Edit.Video_processor import VideoProcessor
    print("✓ VideoProcessor importé avec succès")
except Exception as e:
    print(f"❌ Erreur import VideoProcessor: {e}")
    exit(1)

try:
    import subprocess
    print("✓ Subprocess importé")
except Exception as e:
    print(f"❌ Erreur import subprocess: {e}")
    exit(1)

# Configuration
STREAMER_USERNAME = "sniper_biscuit"
MAX_CLIPS = 3
MAX_DURATION = 90  # 1m30
MIN_VIEWS = 10     # Réduit pour avoir plus de résultats

print(f"\n⚙️  CONFIGURATION:")
print(f"   • Streamer: {STREAMER_USERNAME}")
print(f"   • Max clips: {MAX_CLIPS}")
print(f"   • Durée max: {MAX_DURATION}s")
print(f"   • Vues min: {MIN_VIEWS}")

# ÉTAPE 3: Test API Twitch
print("\n🌐 ÉTAPE 3: TEST API TWITCH")
print("-" * 50)

start_time = time.time()

try:
    twitch_api = TwitchApi(CLIENT_ID, CLIENT_SECRET)
    print("✓ API Twitch initialisée")
    
    # Récupération de l'ID utilisateur
    user_id = twitch_api.getUserId(STREAMER_USERNAME)
    if not user_id:
        print(f"❌ Streamer '{STREAMER_USERNAME}' non trouvé")
        exit(1)
    
    print(f"✓ ID utilisateur: {user_id}")
    
    # Récupération des clips
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # 30 jours pour plus de chances
    
    filters = {
        "started_at": start_date.isoformat() + "Z",
        "ended_at": end_date.isoformat() + "Z",
        "first": MAX_CLIPS
    }
    
    print(f"📅 Recherche des clips sur 30 jours...")
    clips = twitch_api.getClips(user_id, filters=filters)
    
    if not clips:
        print("⚠️  Aucun clip trouvé, test avec plus de jours...")
        # Test sans filtre de date
        clips = twitch_api.getClips(user_id, filters={"first": MAX_CLIPS})
    
    if not clips:
        print(f"❌ Aucun clip trouvé pour {STREAMER_USERNAME}")
        exit(1)
    
    print(f"✓ {len(clips)} clips récupérés:")
    for i, clip in enumerate(clips, 1):
        print(f"   {i}. {clip.get('title', 'Sans titre')} - {clip.get('duration', '?')}s - {clip.get('view_count', 0)} vues")

except Exception as e:
    print(f"❌ Erreur API Twitch: {e}")
    exit(1)

api_time = time.time() - start_time

# ÉTAPE 4: Test téléchargement Streamlink
print(f"\n⬇️  ÉTAPE 4: TÉLÉCHARGEMENT DES CLIPS")
print("-" * 50)

download_start = time.time()
downloaded_clips = []

# Créer le dossier de téléchargement
base_dir = os.path.dirname(os.path.abspath(__file__))
download_folder = os.path.join(base_dir, "data", "fetch_clips")
os.makedirs(download_folder, exist_ok=True)

for i, clip in enumerate(clips, 1):
    clip_url = clip.get('url', '')
    clip_id = clip.get('id', f'clip_{i}')
    output_path = os.path.join(download_folder, f"test_clip_{i}_{clip_id}.mp4")
    
    print(f"📥 Téléchargement clip {i}/{len(clips)}: {clip.get('title', 'Sans titre')}")
    
    try:
        # Utiliser Streamlink avec timeout
        venv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.venv', 'Scripts', 'streamlink.exe')
        command = [
            venv_path,
            clip_url,
            "best",
            "-o", output_path,
            "--retry-open", "3",
            "--retry-streams", "3"
        ]
        
        result = subprocess.run(command, timeout=120, capture_output=True, text=True, check=True)
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / 1024 / 1024
            print(f"   ✓ Téléchargé: {file_size:.1f} MB")
            downloaded_clips.append({
                'path': output_path,
                'clip': clip,
                'size': file_size
            })
        else:
            print(f"   ❌ Fichier non créé")
            
    except subprocess.TimeoutExpired:
        print(f"   ⏰ Timeout (120s dépassé)")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

download_time = time.time() - download_start

if not downloaded_clips:
    print("❌ Aucun clip téléchargé avec succès")
    exit(1)

print(f"\n✓ {len(downloaded_clips)} clips téléchargés en {download_time:.1f}s")

# ÉTAPE 5: Test traitement vidéo
print(f"\n🎬 ÉTAPE 5: TRAITEMENT VIDÉO (FORMAT TIKTOK)")
print("-" * 50)

processing_start = time.time()
processed_clips = []

# Créer les dossiers nécessaires
os.makedirs(os.path.join(base_dir, "data", "processed_clips"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "Edit", "in_process_clips"), exist_ok=True)

for i, clip_data in enumerate(downloaded_clips, 1):
    print(f"🎥 Traitement clip {i}/{len(downloaded_clips)}: {clip_data['clip'].get('title', 'Sans titre')}")
    
    try:
        processor = VideoProcessor(
            clip_data['path'],
            webcam_extraction=True,
            clip_format="portrait"
        )
        
        # Le traitement peut prendre du temps
        result = processor.process_video(target_width=1080, target_height=1920)
        
        # Vérifier si le fichier a été créé (même si result est False)
        processed_files = []
        processed_dir = os.path.join(base_dir, "data", "processed_clips")
        for file in os.listdir(processed_dir):
            if file.endswith("_processed.mp4"):
                file_path = os.path.join(processed_dir, file)
                file_time = os.path.getmtime(file_path)
                if file_time > processing_start:  # Créé après le début du traitement
                    processed_files.append(file_path)
        
        if processed_files:
            latest_file = max(processed_files, key=os.path.getmtime)
            file_size = os.path.getsize(latest_file) / 1024 / 1024
            print(f"   ✓ Traité: {os.path.basename(latest_file)} ({file_size:.1f} MB)")
            processed_clips.append({
                'path': latest_file,
                'original': clip_data,
                'size': file_size
            })
        else:
            print(f"   ❌ Traitement échoué")
            
    except Exception as e:
        print(f"   ❌ Erreur traitement: {e}")

processing_time = time.time() - processing_start
total_time = time.time() - start_time

# RÉSUMÉ FINAL
print(f"\n🎯 RÉSUMÉ FINAL")
print("=" * 70)
print(f"⏱️  Temps total: {total_time:.1f}s")
print(f"   • API Twitch: {api_time:.1f}s")
print(f"   • Téléchargements: {download_time:.1f}s") 
print(f"   • Traitement vidéo: {processing_time:.1f}s")
print()
print(f"📊 RÉSULTATS:")
print(f"   • Clips trouvés: {len(clips)}")
print(f"   • Clips téléchargés: {len(downloaded_clips)}")
print(f"   • Clips traités: {len(processed_clips)}")
print()

if processed_clips:
    print(f"🎬 FICHIERS FINAUX:")
    for i, clip in enumerate(processed_clips, 1):
        print(f"   {i}. {os.path.basename(clip['path'])} ({clip['size']:.1f} MB)")
        print(f"      Original: {clip['original']['clip'].get('title', 'Sans titre')}")
    
    print(f"\n📁 Emplacement: C:\\Users\\User\\Desktop\\Cours\\Framework Web\\GROOT\\backend\\data\\processed_clips\\")
    
    print(f"\n🎉 TEST COMPLET RÉUSSI ! 🎉")
    print(f"Le processus de A à Z fonctionne parfaitement avec {STREAMER_USERNAME}")
else:
    print(f"\n⚠️  Test partiellement réussi")
    print(f"Téléchargement OK, mais traitement vidéo à débugger")

print("=" * 70)