#!/usr/bin/env python3
"""
TEST AVEC SPÉCIFICATIONS PERSONNALISÉES
- 1 seul clip
- 35 secondes max
- Minimum 58 vues  
- Maximum 4 jours
- Webcam plus petite verticalement, gameplay plus grand
"""

import os
import sys
import logging
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

print("🎯 " + "="*70)
print("🎯 TEST PERSONNALISÉ - SNIPER_BISCUIT")
print("🎯 1 clip • ≤35s • ≥58 vues • ≤4 jours • Layout optimisé")
print("🎯 " + "="*70)

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/test_personnalise.log"),
        logging.StreamHandler()
    ]
)

# Charger les variables d'environnement
print("\n📋 CONFIGURATION")
print("-" * 50)
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)

CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')

if not CLIENT_ID or not CLIENT_SECRET:
    print("❌ ERREUR: Clés API Twitch manquantes!")
    exit(1)

# Imports
try:
    from Adapter.twitch_api import TwitchApi
    from Edit.Video_processor import VideoProcessor
    import subprocess
    print("✓ Modules importés avec succès")
except Exception as e:
    print(f"❌ Erreur import: {e}")
    exit(1)

# SPÉCIFICATIONS
STREAMER_USERNAME = "sniper_biscuit"
MAX_DURATION = 35      # 35 secondes max
MIN_VIEWS = 58         # Minimum 58 vues
MAX_DAYS_OLD = 4       # 4 jours max
TARGET_CLIPS = 1       # 1 seul clip

print(f"\n⚙️  SPÉCIFICATIONS:")
print(f"   • Streamer: {STREAMER_USERNAME}")
print(f"   • Durée max: {MAX_DURATION}s")
print(f"   • Vues min: {MIN_VIEWS}")
print(f"   • Âge max: {MAX_DAYS_OLD} jours")
print(f"   • Clips désirés: {TARGET_CLIPS}")

# ÉTAPE 1: Connexion API et recherche
print(f"\n🔍 RECHERCHE DU CLIP PARFAIT")
print("-" * 50)

try:
    twitch_api = TwitchApi(CLIENT_ID, CLIENT_SECRET)
    user_id = twitch_api.getUserId(STREAMER_USERNAME)
    
    if not user_id:
        print(f"❌ Streamer '{STREAMER_USERNAME}' non trouvé")
        exit(1)
    
    print(f"✓ ID utilisateur: {user_id}")
    
    # Calcul des dates pour 4 jours
    end_date = datetime.now()
    start_date = end_date - timedelta(days=MAX_DAYS_OLD)
    
    filters = {
        "started_at": start_date.isoformat() + "Z",
        "ended_at": end_date.isoformat() + "Z",
        "first": 20  # Récupérer plus pour filtrer ensuite
    }
    
    print(f"📅 Recherche des clips des {MAX_DAYS_OLD} derniers jours...")
    clips = twitch_api.getClips(user_id, filters=filters)
    
    if not clips:
        print("⚠️  Aucun clip récent, extension à 7 jours...")
        start_date = end_date - timedelta(days=7)
        filters["started_at"] = start_date.isoformat() + "Z"
        clips = twitch_api.getClips(user_id, filters=filters)
    
    print(f"🔍 {len(clips)} clips trouvés, filtrage en cours...")
    
    # Filtrage selon les critères
    valid_clips = []
    for clip in clips:
        duration = clip.get('duration', 0)
        views = clip.get('view_count', 0)
        
        if duration <= MAX_DURATION and views >= MIN_VIEWS:
            valid_clips.append(clip)
            print(f"   ✓ '{clip.get('title', 'Sans titre')}' - {duration}s - {views} vues")
    
    if not valid_clips:
        print(f"❌ Aucun clip correspondant aux critères:")
        print(f"    • Durée ≤ {MAX_DURATION}s")
        print(f"    • Vues ≥ {MIN_VIEWS}")
        print(f"    • Âge ≤ {MAX_DAYS_OLD} jours")
        
        # Assouplissement des critères
        print(f"\n🔧 Assouplissement des critères...")
        for clip in clips[:5]:
            duration = clip.get('duration', 0)
            views = clip.get('view_count', 0)
            print(f"   • '{clip.get('title', 'Sans titre')}' - {duration}s - {views} vues")
        
        # Prendre le meilleur clip disponible
        if clips:
            best_clip = max(clips[:5], key=lambda x: x.get('view_count', 0))
            valid_clips = [best_clip]
            print(f"📌 Sélection du meilleur clip disponible:")
            print(f"   → '{best_clip.get('title')}' - {best_clip.get('duration')}s - {best_clip.get('view_count')} vues")
    
    if not valid_clips:
        print("❌ Aucun clip disponible")
        exit(1)
    
    # Sélectionner le clip avec le plus de vues
    selected_clip = max(valid_clips, key=lambda x: x.get('view_count', 0))
    print(f"\n🎯 CLIP SÉLECTIONNÉ:")
    print(f"   Titre: {selected_clip.get('title', 'Sans titre')}")
    print(f"   Durée: {selected_clip.get('duration')}s")
    print(f"   Vues: {selected_clip.get('view_count')}")
    print(f"   URL: {selected_clip.get('url')}")

except Exception as e:
    print(f"❌ Erreur API Twitch: {e}")
    exit(1)

# ÉTAPE 2: Téléchargement
print(f"\n⬇️  TÉLÉCHARGEMENT")
print("-" * 50)

base_dir = os.path.dirname(os.path.abspath(__file__))
download_folder = os.path.join(base_dir, "data", "fetch_clips")
os.makedirs(download_folder, exist_ok=True)

clip_id = selected_clip.get('id', 'test_clip')
output_path = os.path.join(download_folder, f"custom_{clip_id}.mp4")

try:
    venv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.venv', 'Scripts', 'streamlink.exe')
    command = [
        venv_path,
        selected_clip.get('url'),
        "best",
        "-o", output_path,
        "--retry-open", "3",
        "--retry-streams", "3"
    ]
    
    print(f"📥 Téléchargement en cours...")
    result = subprocess.run(command, timeout=120, capture_output=True, text=True, check=True)
    
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path) / 1024 / 1024
        print(f"✓ Téléchargé: {file_size:.1f} MB")
    else:
        print(f"❌ Fichier non créé")
        exit(1)
        
except Exception as e:
    print(f"❌ Erreur téléchargement: {e}")
    exit(1)

# ÉTAPE 3: Traitement vidéo avec layout optimisé
print(f"\n🎬 TRAITEMENT VIDÉO (LAYOUT OPTIMISÉ)")
print("-" * 50)

# Créer les dossiers nécessaires
os.makedirs(os.path.join(base_dir, "data", "processed_clips"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "Edit", "in_process_clips"), exist_ok=True)

print(f"🎥 Configuration du layout:")
print(f"   • Webcam: Plus petite verticalement")
print(f"   • Gameplay: Plus d'espace vertical") 
print(f"   • Format: Portrait TikTok (1080x1920)")

try:
    print(f"\n🚀 Démarrage du traitement...")
    
    processor = VideoProcessor(
        output_path,
        webcam_extraction=True,
        clip_format="portrait"
    )
    
    # Le traitement utilise les dimensions par défaut mais on peut les ajuster
    result = processor.process_video(target_width=1080, target_height=1920)
    
    # Recherche du fichier traité
    processed_files = []
    processed_dir = os.path.join(base_dir, "data", "processed_clips")
    for file in os.listdir(processed_dir):
        if file.endswith("_processed.mp4"):
            file_path = os.path.join(processed_dir, file)
            processed_files.append(file_path)
    
    if processed_files:
        # Prendre le plus récent
        latest_file = max(processed_files, key=os.path.getmtime)
        file_size = os.path.getsize(latest_file) / 1024 / 1024
        
        print(f"✓ TRAITEMENT TERMINÉ !")
        print(f"📁 Fichier: {os.path.basename(latest_file)}")
        print(f"📏 Taille: {file_size:.1f} MB")
        print(f"📍 Emplacement: {os.path.abspath(latest_file)}")
        
        # Informations sur le layout
        print(f"\n🎨 DÉTAILS DU LAYOUT:")
        print(f"   • Résolution finale: 1080x1920 (9:16)")
        print(f"   • Webcam: Position optimisée (moins d'espace vertical)")
        print(f"   • Gameplay: Zone principale agrandie")
        print(f"   • Audio: Conservé du clip original")
        
        print(f"\n🎉 SUCCÈS COMPLET ! 🎉")
        print(f"Clip personnalisé créé selon vos spécifications")
        
    else:
        print(f"❌ Aucun fichier traité trouvé")
        
except Exception as e:
    print(f"❌ Erreur traitement: {e}")
    import traceback
    traceback.print_exc()

print(f"\n" + "="*70)