#!/usr/bin/env python3
"""
Test simple de téléchargement Streamlink pour diagnostiquer le problème
"""

import subprocess
import os
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def test_streamlink_download():
    """Test simple de téléchargement avec timeout"""
    
    clip_url = "https://www.twitch.tv/xqc/clip/CautiousVictoriousWaterFUNgineer-yUz0HNobXXhECJUa"
    output_path = "test_clip.mp4"
    
    # Utiliser le chemin complet vers streamlink dans l'environnement virtuel
    venv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.venv', 'Scripts', 'streamlink.exe')
    
    command = [
        venv_path,
        clip_url,
        "best",
        "-o", output_path,
        "--retry-open", "3",
        "--retry-streams", "3"
    ]
    
    print(f"Test de téléchargement de : {clip_url}")
    print(f"Commande : {' '.join(command)}")
    print("Début du téléchargement...")
    
    try:
        # Timeout de 60 secondes
        result = subprocess.run(command, timeout=60, capture_output=True, text=True, check=True)
        print(f"✓ Téléchargement réussi !")
        print(f"STDOUT: {result.stdout}")
        
        # Vérifier si le fichier existe
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✓ Fichier créé : {output_path} ({file_size} bytes)")
            return True
        else:
            print("✗ Fichier non créé")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ TIMEOUT : Le téléchargement a pris plus de 60 secondes")
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"✗ ERREUR Streamlink : {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False
        
    except Exception as e:
        print(f"✗ ERREUR inattendue : {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("TEST DE TÉLÉCHARGEMENT STREAMLINK")
    print("="*60)
    
    success = test_streamlink_download()
    
    print("\n" + "="*60)
    if success:
        print("✓ TEST RÉUSSI - Streamlink fonctionne correctement")
    else:
        print("✗ TEST ÉCHOUÉ - Problème avec Streamlink")
    print("="*60)