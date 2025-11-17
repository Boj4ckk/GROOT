#!/usr/bin/env python3
"""
Analyse des dimensions du clip original pour connaître la taille de gameplay vertical
"""

import cv2
import os

def analyze_clip_dimensions():
    """Analyse les dimensions du clip original"""
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    clip_path = os.path.join(base_dir, "data", "fetch_clips", "custom_AbstruseStupidFriseeYouDontSay-V-AZ0l9mSJVx0uJV.mp4")
    
    if not os.path.exists(clip_path):
        print(f"❌ Clip non trouvé: {clip_path}")
        return
    
    print("📐 " + "="*50)
    print("📐 ANALYSE DES DIMENSIONS DU CLIP ORIGINAL")
    print("📐 " + "="*50)
    
    # Lire les dimensions avec OpenCV
    cap = cv2.VideoCapture(clip_path)
    
    if not cap.isOpened():
        print("❌ Impossible d'ouvrir le clip")
        return
    
    # Récupérer les dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps > 0 else 0
    
    cap.release()
    
    # Calculer le ratio
    ratio = width / height
    
    print(f"📏 DIMENSIONS ORIGINALES:")
    print(f"   • Largeur: {width}px")
    print(f"   • Hauteur: {height}px") 
    print(f"   • Ratio: {ratio:.2f} ({width}:{height})")
    print(f"   • Format: {'Paysage' if ratio > 1 else 'Portrait'}")
    print(f"   • FPS: {fps:.1f}")
    print(f"   • Durée: {duration:.1f}s")
    
    # Calculer ce qui se passe dans le traitement
    print(f"\n🔄 TRANSFORMATION VERS FORMAT TIKTOK:")
    print(f"   • Cible: 1080x1920 (ratio 0.56)")
    print(f"   • Original: {width}x{height} (ratio {ratio:.2f})")
    
    if ratio > 0.56:
        print(f"   • Clip TROP LARGE → rognage sur les côtés")
        new_width = int(height * 0.56)
        rogned_width = width - new_width
        print(f"   • Nouvelle largeur: {new_width}px")
        print(f"   • Pixels rognés (côtés): {rogned_width}px")
        print(f"   • HAUTEUR CONSERVÉE: {height}px")
        
        # Dans le système actuel
        gameplay_space = 1570  # Espace alloué au gameplay
        if height > gameplay_space:
            scale_factor = gameplay_space / height
            final_width = int(new_width * scale_factor)
            final_height = gameplay_space
            print(f"\n📐 REDIMENSIONNEMENT FINAL:")
            print(f"   • Hauteur gameplay disponible: {gameplay_space}px")
            print(f"   • Facteur de réduction: {scale_factor:.3f}")
            print(f"   • Dimensions finales gameplay: {final_width}x{final_height}px")
        else:
            print(f"\n✅ Pas de redimensionnement nécessaire")
            print(f"   • Le gameplay rentre dans l'espace {gameplay_space}px")
    else:
        print(f"   • Clip TROP HAUT → redimensionnement pour conserver tout")
        gameplay_space = 1570
        scale_factor = gameplay_space / height
        final_width = int(width * scale_factor)
        final_height = gameplay_space
        print(f"   • Facteur de réduction: {scale_factor:.3f}")
        print(f"   • Dimensions finales: {final_width}x{final_height}px")
        print(f"   • TOUT LE CONTENU VERTICAL CONSERVÉ")

if __name__ == "__main__":
    analyze_clip_dimensions()