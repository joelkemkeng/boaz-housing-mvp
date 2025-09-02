#!/usr/bin/env python3
"""
Test manuel du modèle User SQLAlchemy
"""
import sys
sys.path.append('/app')

from app.models.user import User, UserRole

def test_user_creation():
    """Test 1 : Création d'un utilisateur"""
    print("🧪 Test 1: Création d'un utilisateur User...")
    
    try:
        user = User()
        user.email = "test@boaz-study.com"
        user.nom = "Dupont"
        user.prenom = "Jean"
        user.password_hash = "hashed_password_secure_123"
        user.role = UserRole.AGENT_BOAZ
        user.active = True
        
        print(f"✅ Utilisateur créé avec succès:")
        print(f"   📧 Email: {user.email}")
        print(f"   👤 Nom complet: {user.prenom} {user.nom}")
        print(f"   🔐 Password hash: {user.password_hash[:20]}...")
        print(f"   👔 Rôle: {user.role.value}")
        print(f"   ✅ Actif: {user.active}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_all_roles():
    """Test 2 : Tous les rôles disponibles"""
    print("\n🧪 Test 2: Vérification de tous les rôles...")
    
    try:
        roles_expected = ['client', 'agent-boaz', 'admin-generale', 'bailleur']
        roles_found = [role.value for role in UserRole]
        
        print("📋 Rôles disponibles:")
        for i, role in enumerate(UserRole, 1):
            print(f"   {i}. {role.value}")
        
        if set(roles_expected) == set(roles_found):
            print("✅ Tous les rôles requis sont présents")
            return True
        else:
            print(f"❌ Rôles manquants ou incorrects")
            print(f"   Attendu: {roles_expected}")
            print(f"   Trouvé: {roles_found}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_validation():
    """Test 3 : Validation des données"""
    print("\n🧪 Test 3: Validation des champs...")
    
    tests_passed = 0
    
    # Test validation email
    try:
        user = User()
        user.email = "email_invalide"  # Email invalide
        print("❌ La validation email aurait dû échouer")
    except ValueError as e:
        print(f"✅ Validation email correcte: {str(e)}")
        tests_passed += 1
    
    # Test validation nom vide
    try:
        user = User()
        user.nom = ""  # Nom vide
        print("❌ La validation nom vide aurait dû échouer")
    except ValueError as e:
        print(f"✅ Validation nom vide correcte: {str(e)}")
        tests_passed += 1
    
    # Test validation prénom trop court
    try:
        user = User()
        user.prenom = "J"  # Prénom trop court
        print("❌ La validation prénom court aurait dû échouer")
    except ValueError as e:
        print(f"✅ Validation prénom court correcte: {str(e)}")
        tests_passed += 1
    
    return tests_passed == 3

def main():
    """Exécuter tous les tests"""
    print("=" * 60)
    print("🧪 TESTS MODÈLE USER SQLAlchemy")
    print("=" * 60)
    
    success_count = 0
    
    if test_user_creation():
        success_count += 1
    
    if test_all_roles():
        success_count += 1
        
    if test_validation():
        success_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 RÉSULTAT: {success_count}/3 tests réussis")
    
    if success_count == 3:
        print("🎉 TOUS LES TESTS SONT RÉUSSIS!")
        print("➡️  Vous pouvez passer au test suivant: 02-test-migration-database.md")
        return True
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifiez le modèle User dans backend/app/models/user.py")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)