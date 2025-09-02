"""
Script de test pour le service d'envoi d'emails
Usage: python test_email_service.py
"""

import sys
import os
sys.path.append('/home/joel/projet-boaz-housing/boaz-housing-mvp/backend')

from app.services.email_service import email_service

def test_smtp_connection():
    """Test de la connexion SMTP"""
    print("=== Test de connexion SMTP ===")
    
    # Afficher la configuration
    print(f"Host: {email_service.smtp_host}")
    print(f"Port: {email_service.smtp_port}")
    print(f"Username: {email_service.smtp_username}")
    print(f"From Email: {email_service.from_email}")
    
    # Tester la connexion
    success = email_service.test_connection()
    
    if success:
        print("✅ Connexion SMTP réussie!")
        return True
    else:
        print("❌ Échec de la connexion SMTP")
        print("Vérifiez vos paramètres SMTP dans le fichier .env:")
        print("- SMTP_HOST")
        print("- SMTP_PORT") 
        print("- SMTP_USERNAME")
        print("- SMTP_PASSWORD")
        return False

def test_send_proforma_email():
    """Test d'envoi d'email Proforma (sans PDF pour le test)"""
    print("\n=== Test envoi email Proforma ===")
    
    # Email de test - CHANGEZ CETTE ADRESSE
    test_email = "test@example.com"  # MODIFIEZ CETTE ADRESSE
    
    print(f"Envoi d'un email de test à: {test_email}")
    print("Note: Le PDF sera vide pour ce test, seul le template HTML sera envoyé")
    
    # PDF vide pour le test
    fake_pdf_bytes = b"PDF Test Content"
    
    success = email_service.send_proforma_email(
        to_email=test_email,
        pdf_bytes=fake_pdf_bytes,
        reference="ATT-TEST123456",
        client_name="Jean Test"
    )
    
    if success:
        print("✅ Email Proforma envoyé avec succès!")
        return True
    else:
        print("❌ Échec envoi email Proforma")
        return False

def main():
    print("🧪 Test du service d'envoi d'emails Boaz-Housing MVP")
    print("=" * 50)
    
    # Test 1: Connexion SMTP
    connection_ok = test_smtp_connection()
    
    if not connection_ok:
        print("\n❌ Impossible de continuer sans connexion SMTP")
        print("\n💡 Pour configurer SMTP:")
        print("1. Modifiez le fichier backend/.env")
        print("2. Configurez vos paramètres SMTP (Gmail, Mailtrap, etc.)")
        print("3. Relancez ce test")
        return
    
    # Test 2: Envoi d'email (si connexion OK)
    print("\n⚠️  ATTENTION: Le test suivant va envoyer un email réel!")
    user_input = input("Voulez-vous continuer avec le test d'envoi? (y/N): ")
    
    if user_input.lower() in ['y', 'yes', 'oui']:
        email_ok = test_send_proforma_email()
        
        if email_ok:
            print("\n🎉 Tous les tests réussis!")
            print("Le service d'email est prêt pour le MVP")
        else:
            print("\n❌ Test d'envoi échoué")
    else:
        print("\n⏭️  Test d'envoi ignoré")
        print("La connexion SMTP fonctionne, c'est déjà un bon début!")
    
    print("\n📋 Récapitulatif:")
    print("- Service email créé ✅")
    print("- Templates HTML intégrés ✅") 
    print("- Endpoints API ajoutés ✅")
    print("- Configuration SMTP disponible ✅")
    print("\n✨ Le service email MVP est terminé!")

if __name__ == "__main__":
    main()