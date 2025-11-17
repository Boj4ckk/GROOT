#!/usr/bin/env python3
"""
Test de traitement vidéo pour vérifier si la détection faciale fonctionne
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from Edit.Video_processor import VideoProcessor

def test_video_processing():
    """Test du traitement d'un clip téléchargé"""
    
    # Utiliser le premier clip téléchargé
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_clip = os.path.join(base_dir, "data", "fetch_clips", "clip_1_CautiousVictoriousWaterFUNgineer-yUz0HNobXXhECJUa.mp4")
    output_clip = "test_processed_clip.mp4"
    
    print("="*60)
    print("TEST DU TRAITEMENT VIDÉO")
    print("="*60)
    
    if not os.path.exists(input_clip):
        print(f"✗ Fichier d'entrée non trouvé: {input_clip}")
        return False
    
    print(f"Fichier d'entrée: {input_clip}")
    print(f"Taille: {os.path.getsize(input_clip) / 1024 / 1024:.1f} MB")
    
    try:
        print("\nInitialisation du processeur vidéo...")
        processor = VideoProcessor(
            input_clip,
            webcam_extraction=True,
            clip_format="portrait"
        )
        
        print("Début du traitement vidéo...")
        result = processor.process_video(target_width=1080, target_height=1920)
        
        if result:
            print(f"✓ Traitement réussi !")
            # Le fichier de sortie est généré automatiquement dans processed_clips
            return True
        else:
            print("✗ Échec du traitement")
            return False
            
    except Exception as e:
        print(f"✗ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_video_processing()
    
    print("\n" + "="*60)
    if success:
        print("✓ TEST RÉUSSI - Le traitement vidéo fonctionne")
    else:
        print("✗ TEST ÉCHOUÉ - Problème dans le traitement vidéo")
    print("="*60)