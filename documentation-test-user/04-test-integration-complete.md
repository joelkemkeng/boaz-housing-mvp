# 🔗 TEST 4 : Intégration Complète

## 🎯 Objectif
Test d'intégration final qui combine :
- Modèles SQLAlchemy + Base de données
- Schémas Pydantic
- Création d'utilisateurs en base de données
- Vérification bout en bout du système User

---

## 📋 Étape 1 : Vue d'ensemble de l'intégration

Ce test simule un workflow complet :
1. **Créer** un utilisateur avec UserCreate (Pydantic)
2. **Sauvegarder** en base de données (SQLAlchemy)
3. **Récupérer** depuis la base de données
4. **Convertir** en UserResponse (Pydantic)
5. **Vérifier** la cohérence des données

---

## 🔧 Étape 2 : Script d'intégration complète

Créer le fichier `documentation-test-user/scripts/test_integration_complete.py` :

```python
#!/usr/bin/env python3
"""
Test d'intégration complet : Modèles + Schémas + Base de données
"""
import sys
sys.path.append('/app')

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.database import get_db, engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import traceback

# Setup du contexte de hachage (simple pour les tests)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hacher un mot de passe"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifier un mot de passe"""
    return pwd_context.verify(plain_password, hashed_password)

def test_database_session():
    """Test 1 : Connexion à la session de base de données"""
    print("🧪 Test 1: Connexion à la session de base de données...")
    
    try:
        db = next(get_db())
        # Test simple
        result = db.execute("SELECT 1")
        result.fetchone()
        db.close()
        
        print("✅ Session de base de données fonctionnelle")
        return True
    except Exception as e:
        print(f"❌ Erreur de session: {str(e)}")
        return False

def test_create_user_in_database():
    """Test 2 : Créer un utilisateur en base de données"""
    print("\n🧪 Test 2: Créer un utilisateur en base de données...")
    
    try:
        # Données d'entrée via schéma Pydantic
        user_create = UserCreate(
            email="integration-test@boaz-study.com",
            nom="Integration",
            prenom="Test",
            password="test1234",
            role=UserRole.AGENT_BOAZ,
            active=True
        )
        
        print(f"📝 Données à créer:")
        print(f"   📧 Email: {user_create.email}")
        print(f"   👤 Nom: {user_create.nom} {user_create.prenom}")
        print(f"   👔 Rôle: {user_create.role.value}")
        
        # Créer l'objet SQLAlchemy
        db_user = User(
            email=user_create.email,
            nom=user_create.nom,
            prenom=user_create.prenom,
            password_hash=hash_password(user_create.password),
            role=user_create.role,
            active=user_create.active
        )
        
        # Sauvegarder en base de données
        db = next(get_db())
        
        # Supprimer l'utilisateur s'il existe déjà (pour les tests répétés)
        existing_user = db.query(User).filter(User.email == user_create.email).first()
        if existing_user:
            db.delete(existing_user)
            db.commit()
            print("🧹 Utilisateur existant supprimé")
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        print(f"✅ Utilisateur créé avec succès en base de données:")
        print(f"   🆔 ID: {db_user.id}")
        print(f"   📧 Email: {db_user.email}")
        print(f"   🔐 Password hash: {db_user.password_hash[:30]}...")
        print(f"   📅 Créé le: {db_user.created_at}")
        
        db.close()
        return True, db_user.id
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        traceback.print_exc()
        return False, None

def test_retrieve_user_from_database(user_id: int):
    """Test 3 : Récupérer l'utilisateur depuis la base de données"""
    print(f"\n🧪 Test 3: Récupérer l'utilisateur ID {user_id} depuis la base...")
    
    try:
        db = next(get_db())
        
        # Récupérer par ID
        db_user = db.query(User).filter(User.id == user_id).first()
        
        if not db_user:
            print("❌ Utilisateur non trouvé")
            db.close()
            return False, None
        
        print(f"✅ Utilisateur récupéré:")
        print(f"   🆔 ID: {db_user.id}")
        print(f"   📧 Email: {db_user.email}")
        print(f"   👤 Nom: {db_user.nom} {db_user.prenom}")
        print(f"   👔 Rôle: {db_user.role.value}")
        print(f"   ✅ Actif: {db_user.active}")
        
        db.close()
        return True, db_user
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False, None

def test_convert_to_response_schema(db_user):
    """Test 4 : Convertir en schéma UserResponse"""
    print(f"\n🧪 Test 4: Convertir en schéma UserResponse...")
    
    try:
        # Convertir l'objet SQLAlchemy en schéma Pydantic
        user_response = UserResponse.from_orm(db_user)
        
        print(f"✅ Conversion UserResponse réussie:")
        print(f"   🆔 ID: {user_response.id}")
        print(f"   📧 Email: {user_response.email}")
        print(f"   👤 Nom: {user_response.nom} {user_response.prenom}")
        print(f"   👔 Rôle: {user_response.role.value}")
        print(f"   ✅ Actif: {user_response.active}")
        print(f"   📅 Créé le: {user_response.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Vérification : le password ne doit PAS être dans la réponse
        if hasattr(user_response, 'password') or hasattr(user_response, 'password_hash'):
            print("❌ ERREUR: Le mot de passe est exposé dans UserResponse!")
            return False
        else:
            print("✅ Sécurité: Aucun mot de passe exposé dans UserResponse")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        traceback.print_exc()
        return False

def test_password_verification(user_id: int):
    """Test 5 : Vérifier le hachage du mot de passe"""
    print(f"\n🧪 Test 5: Vérifier le hachage du mot de passe...")
    
    try:
        db = next(get_db())
        db_user = db.query(User).filter(User.id == user_id).first()
        
        if not db_user:
            print("❌ Utilisateur non trouvé")
            db.close()
            return False
        
        # Test avec le bon mot de passe
        original_password = "test1234"
        if verify_password(original_password, db_user.password_hash):
            print("✅ Vérification mot de passe correct réussie")
        else:
            print("❌ Vérification mot de passe correct échouée")
            db.close()
            return False
        
        # Test avec un mauvais mot de passe
        wrong_password = "mauvais_password"
        if not verify_password(wrong_password, db_user.password_hash):
            print("✅ Vérification mauvais mot de passe correctement rejetée")
        else:
            print("❌ Vérification mauvais mot de passe aurait dû échouer")
            db.close()
            return False
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_user_login_workflow():
    """Test 6 : Workflow de connexion utilisateur"""
    print(f"\n🧪 Test 6: Workflow de connexion utilisateur...")
    
    try:
        # Schéma de login
        login_data = UserLogin(
            email="integration-test@boaz-study.com",
            password="test1234"
        )
        
        print(f"🔐 Tentative de connexion:")
        print(f"   📧 Email: {login_data.email}")
        print(f"   🔑 Password: {'*' * len(login_data.password)}")
        
        # Rechercher l'utilisateur
        db = next(get_db())
        db_user = db.query(User).filter(User.email == login_data.email).first()
        
        if not db_user:
            print("❌ Utilisateur non trouvé pour connexion")
            db.close()
            return False
        
        # Vérifier le mot de passe
        if not verify_password(login_data.password, db_user.password_hash):
            print("❌ Mot de passe incorrect")
            db.close()
            return False
        
        # Vérifier que l'utilisateur est actif
        if not db_user.active:
            print("❌ Utilisateur inactif")
            db.close()
            return False
        
        # Créer la réponse de connexion
        user_response = UserResponse.from_orm(db_user)
        
        print("✅ Connexion réussie!")
        print(f"   👤 Utilisateur connecté: {user_response.prenom} {user_response.nom}")
        print(f"   👔 Rôle: {user_response.role.value}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        traceback.print_exc()
        return False

def cleanup_test_user():
    """Nettoyage : Supprimer l'utilisateur de test"""
    print(f"\n🧹 Nettoyage: Suppression de l'utilisateur de test...")
    
    try:
        db = next(get_db())
        test_user = db.query(User).filter(User.email == "integration-test@boaz-study.com").first()
        
        if test_user:
            db.delete(test_user)
            db.commit()
            print("✅ Utilisateur de test supprimé")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {str(e)}")
        return False

def main():
    """Exécuter tous les tests d'intégration"""
    print("=" * 80)
    print("🔗 TESTS D'INTÉGRATION COMPLÈTE - SYSTÈME USER")
    print("=" * 80)
    
    success_count = 0
    user_id = None
    db_user = None
    
    # Test 1: Session DB
    if test_database_session():
        success_count += 1
    
    # Test 2: Création utilisateur
    success, user_id = test_create_user_in_database()
    if success:
        success_count += 1
    
    # Test 3: Récupération utilisateur
    if user_id:
        success, db_user = test_retrieve_user_from_database(user_id)
        if success:
            success_count += 1
    
    # Test 4: Conversion en schéma
    if db_user:
        if test_convert_to_response_schema(db_user):
            success_count += 1
    
    # Test 5: Vérification password
    if user_id:
        if test_password_verification(user_id):
            success_count += 1
    
    # Test 6: Workflow de login
    if test_user_login_workflow():
        success_count += 1
    
    # Nettoyage
    cleanup_test_user()
    
    print("\n" + "=" * 80)
    print(f"📊 RÉSULTAT FINAL: {success_count}/6 tests d'intégration réussis")
    
    if success_count == 6:
        print("🎉 TOUS LES TESTS D'INTÉGRATION SONT RÉUSSIS!")
        print("🚀 Le système User est complètement fonctionnel!")
        print("✅ Phase 1.1 validée - Prêt pour la Phase 1.2")
        return True
    else:
        print("❌ CERTAINS TESTS D'INTÉGRATION ONT ÉCHOUÉ")
        print("🔧 Vérifiez l'intégration entre modèles, schémas et base de données")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
```

---

## ▶️ Étape 3 : Exécuter le test d'intégration

```bash
# S'assurer que passlib est installé (pour le hachage des mots de passe)
docker-compose exec backend pip install passlib[bcrypt]

# Copier et exécuter le script d'intégration
docker cp documentation-test-user/scripts/test_integration_complete.py boaz-backend:/app/test_integration_complete.py
docker-compose exec backend python /app/test_integration_complete.py
```

---

## ✅ Résultats attendus

```
================================================================================
🔗 TESTS D'INTÉGRATION COMPLÈTE - SYSTÈME USER
================================================================================
🧪 Test 1: Connexion à la session de base de données...
✅ Session de base de données fonctionnelle

🧪 Test 2: Créer un utilisateur en base de données...
📝 Données à créer:
   📧 Email: integration-test@boaz-study.com
   👤 Nom: Integration Test
   👔 Rôle: agent-boaz
✅ Utilisateur créé avec succès en base de données:
   🆔 ID: 15
   📧 Email: integration-test@boaz-study.com
   🔐 Password hash: $2b$12$abcd1234efgh5678ijkl...
   📅 Créé le: 2025-09-02 15:45:30.123456

🧪 Test 3: Récupérer l'utilisateur ID 15 depuis la base...
✅ Utilisateur récupéré:
   🆔 ID: 15
   📧 Email: integration-test@boaz-study.com
   👤 Nom: Integration Test
   👔 Rôle: agent-boaz
   ✅ Actif: True

🧪 Test 4: Convertir en schéma UserResponse...
✅ Conversion UserResponse réussie:
   🆔 ID: 15
   📧 Email: integration-test@boaz-study.com
   👤 Nom: Integration Test
   👔 Rôle: agent-boaz
   ✅ Actif: True
   📅 Créé le: 2025-09-02 15:45:30
✅ Sécurité: Aucun mot de passe exposé dans UserResponse

🧪 Test 5: Vérifier le hachage du mot de passe...
✅ Vérification mot de passe correct réussie
✅ Vérification mauvais mot de passe correctement rejetée

🧪 Test 6: Workflow de connexion utilisateur...
🔐 Tentative de connexion:
   📧 Email: integration-test@boaz-study.com
   🔑 Password: ********
✅ Connexion réussie!
   👤 Utilisateur connecté: Test Integration
   👔 Rôle: agent-boaz

🧹 Nettoyage: Suppression de l'utilisateur de test...
✅ Utilisateur de test supprimé

================================================================================
📊 RÉSULTAT FINAL: 6/6 tests d'intégration réussis
🎉 TOUS LES TESTS D'INTÉGRATION SONT RÉUSSIS!
🚀 Le système User est complètement fonctionnel!
✅ Phase 1.1 validée - Prêt pour la Phase 1.2
```

---

## 🔍 Que vérifier dans ce test

1. **✅ Session DB** : Connexion à la base de données fonctionnelle
2. **✅ CRUD complet** : Création, lecture d'utilisateur en base
3. **✅ Intégration Modèles↔Schémas** : Conversion bidirectionnelle
4. **✅ Sécurité** : Hachage des mots de passe, pas d'exposition
5. **✅ Workflow Login** : Processus de connexion complet
6. **✅ Nettoyage** : Pas de données de test qui traînent

---

## 🚨 En cas d'erreur

### ImportError passlib
```bash
# Installer passlib dans le container
docker-compose exec backend pip install passlib[bcrypt]

# Ou l'ajouter aux requirements.txt
echo "passlib[bcrypt]==1.7.4" >> backend/requirements.txt
docker-compose build backend
```

### Erreur "from_orm" 
- Vérifier que `from_attributes = True` est dans la Config des schémas Pydantic
- Vérifier la version de Pydantic (doit être >= 2.0)

### Utilisateur de test reste en base
```bash
# Nettoyage manuel
docker-compose exec backend python -c "
from app.database import get_db
from app.models.user import User
db = next(get_db())
test_user = db.query(User).filter(User.email == 'integration-test@boaz-study.com').first()
if test_user:
    db.delete(test_user)
    db.commit()
db.close()
print('Nettoyé')
"
```

---

## 🎉 Conclusion

Si ce test passe complètement, cela signifie que :

✅ **Phase 1.1 TERMINÉE** avec succès
- Modèles SQLAlchemy fonctionnels
- Migration base de données appliquée  
- Schémas Pydantic opérationnels
- Intégration complète validée

🚀 **Prêt pour Phase 1.2** : Login/Auth Simple (Backend)

---

## ➡️ Prochaine étape

**Phase 1.1 complètement validée !**

Vous pouvez maintenant demander l'autorisation pour commencer la **Phase 1.2** : Login/Auth Simple (Backend)