#!/usr/bin/env python3
"""
Script de debug pour tester étape par étape la récupération des clips Twitch
"""

import os
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

print("="*50)
print("DÉBUT DU DEBUG - RÉCUPÉRATION DES CLIPS")
print("="*50)

# Charger les variables d'environnement
print("1. Chargement du fichier .env...")
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
print(f"Chemin du .env : {env_path}")
load_dotenv(env_path)

CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')

print(f"CLIENT_ID chargé : {'✓' if CLIENT_ID else '✗'}")
print(f"CLIENT_SECRET chargé : {'✓' if CLIENT_SECRET else '✗'}")

if not CLIENT_ID or not CLIENT_SECRET:
    print("ERREUR : Clés API manquantes !")
    exit(1)

print("\n2. Importation de TwitchApi...")
try:
    from Adapter.twitch_api import TwitchApi
    print("✓ Import TwitchApi réussi")
except Exception as e:
    print(f"✗ Erreur import TwitchApi : {e}")
    exit(1)

print("\n3. Initialisation de l'API Twitch...")
try:
    twitch_api = TwitchApi(CLIENT_ID, CLIENT_SECRET)
    print("✓ API Twitch initialisée avec succès")
except Exception as e:
    print(f"✗ Erreur initialisation API : {e}")
    exit(1)

# Test de récupération de l'ID utilisateur
print("\n4. Test de récupération de l'ID utilisateur...")
STREAMER_USERNAME = "xqc"  # Changé pour un streamer plus actif
print(f"Recherche de l'utilisateur : {STREAMER_USERNAME}")

try:
    user_id = twitch_api.getUserId(STREAMER_USERNAME)
    if user_id:
        print(f"✓ ID utilisateur trouvé : {user_id}")
    else:
        print(f"✗ Utilisateur '{STREAMER_USERNAME}' non trouvé")
        print("Essayons avec un autre nom...")
        # Test avec des streamers populaires
        test_streamers = ["xQc", "summit1g", "shroud"]
        for streamer in test_streamers:
            print(f"Test avec {streamer}...")
            test_id = twitch_api.getUserId(streamer)
            if test_id:
                print(f"✓ {streamer} trouvé avec l'ID : {test_id}")
                STREAMER_USERNAME = streamer
                user_id = test_id
                break
        
        if not user_id:
            print("✗ Aucun streamer de test trouvé")
            exit(1)
except Exception as e:
    print(f"✗ Erreur récupération ID utilisateur : {e}")
    exit(1)

# Test de récupération des clips
print(f"\n5. Test de récupération des clips pour {STREAMER_USERNAME}...")

try:
    # Calculer les dates (7 derniers jours)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    filters = {
        "started_at": start_date.isoformat() + "Z",
        "ended_at": end_date.isoformat() + "Z",
        "first": 3  # Seulement 3 clips pour le test
    }
    
    print(f"Filtres appliqués :")
    print(f"  - Date début : {filters['started_at']}")
    print(f"  - Date fin : {filters['ended_at']}")
    print(f"  - Nombre max : {filters['first']}")
    
    clips = twitch_api.getClips(user_id, filters=filters)
    
    print(f"✓ Requête API réussie")
    print(f"Nombre de clips récupérés : {len(clips)}")
    
    if clips:
        print("\nDétails des clips :")
        for i, clip in enumerate(clips, 1):
            print(f"  Clip {i} :")
            print(f"    - Titre : {clip.get('title', 'N/A')}")
            print(f"    - Durée : {clip.get('duration', 'N/A')} secondes")
            print(f"    - Vues : {clip.get('view_count', 'N/A')}")
            print(f"    - URL : {clip.get('url', 'N/A')}")
            print(f"    - ID : {clip.get('id', 'N/A')}")
            print()
    else:
        print("Aucun clip trouvé pour cette période")
        
        # Test sans filtres de date
        print("\nTest sans filtres de date...")
        clips_no_filter = twitch_api.getClips(user_id, filters={"first": 5})
        print(f"Clips trouvés sans filtre de date : {len(clips_no_filter)}")
        
        if clips_no_filter:
            print("Détails des clips sans filtre :")
            for i, clip in enumerate(clips_no_filter, 1):
                print(f"  Clip {i} :")
                print(f"    - Titre : {clip.get('title', 'N/A')}")
                print(f"    - Durée : {clip.get('duration', 'N/A')} secondes")
                print(f"    - Vues : {clip.get('view_count', 'N/A')}")
                print()

except Exception as e:
    print(f"✗ Erreur récupération des clips : {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "="*50)
print("TEST DE RÉCUPÉRATION TERMINÉ AVEC SUCCÈS !")
print("="*50)