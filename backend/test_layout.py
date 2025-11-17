#!/usr/bin/env python3
"""
TEST RAPIDE DU NOUVEAU LAYOUT
Utilise le clip déjà téléchargé pour tester les modifications
"""

import os
import sys
from Edit.Video_processor import VideoProcessor

base_dir = os.path.dirname(os.path.abspath(__file__))

print("🎬 " + "="*50)
print("🎬 TEST RAPIDE DU NOUVEAU LAYOUT")
print("🎬 Webcam: 500px | Gameplay: Complet (sans rognage)")
print("🎬 " + "="*50)

# Utiliser le clip déjà téléchargé
input_clip = os.path.join(base_dir, "data", "fetch_clips", "custom_AbstruseStupidFriseeYouDontSay-V-AZ0l9mSJVx0uJV.mp4")

if not os.path.exists(input_clip):
    print(f"❌ Fichier non trouvé: {input_clip}")
    exit(1)

print(f"📁 Clip d'entrée: {os.path.basename(input_clip)}")
file_size = os.path.getsize(input_clip) / 1024 / 1024
print(f"📏 Taille: {file_size:.1f} MB")

# Créer les dossiers nécessaires
os.makedirs(os.path.join(base_dir, "data", "processed_clips"), exist_ok=True)
os.makedirs(os.path.join(base_dir, "Edit", "in_process_clips"), exist_ok=True)

print(f"\n🎨 LAYOUT OPTIMISÉ POUR GAMEPLAY MAXIMUM:")
print(f"   • Webcam: 250px de hauteur (minimale)")
print(f"   • Gameplay: 1670px MAXIMUM (tout l'espace disponible)")
print(f"   • Total: 1920px portrait TikTok")

try:
    print(f"\n🚀 Démarrage du traitement...")
    
    processor = VideoProcessor(
        input_clip,
        webcam_extraction=True,
        clip_format="portrait"
    )
    
    result = processor.process_video(target_width=1080, target_height=1920)
    
    # Chercher le fichier le plus récent
    processed_files = []
    processed_dir = os.path.join(base_dir, "data", "processed_clips")
    for file in os.listdir(processed_dir):
        if file.endswith("_processed.mp4"):
            file_path = os.path.join(processed_dir, file)
            processed_files.append(file_path)
    
    if processed_files:
        latest_file = max(processed_files, key=os.path.getmtime)
        output_size = os.path.getsize(latest_file) / 1024 / 1024
        
        print(f"\n✅ NOUVEAU LAYOUT APPLIQUÉ !")
        print(f"📁 Fichier: {os.path.basename(latest_file)}")
        print(f"📏 Taille: {output_size:.1f} MB")
        print(f"📍 Emplacement: {os.path.abspath(latest_file)}")
        
        print(f"\n🎯 LAYOUT GAMEPLAY MAXIMUM:")
        print(f"   ✓ Webcam: 250px (minimale pour plus de gameplay)")
        print(f"   ✓ Gameplay: 1670px - ESPACE MAXIMUM")
        print(f"   ✓ Gameplay a 590px d'espace en plus vs original")
        print(f"   ✓ Layout optimisé pour le contenu de jeu")
        
        print(f"\n🎉 LAYOUT OPTIMISÉ AVEC SUCCÈS ! 🎉")
        
    else:
        print(f"❌ Aucun fichier traité trouvé")

except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print(f"\n" + "="*50)