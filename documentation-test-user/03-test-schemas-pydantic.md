# 📝 TEST 3 : Schémas Pydantic User

## 🎯 Objectif
Vérifier que les schémas Pydantic fonctionnent correctement :
- UserCreate (avec validation password)
- UserLogin (email/password)
- UserResponse (sans password)
- UserUpdate (champs optionnels)
- Validation des erreurs (email invalide, password trop court, etc.)

---

## 📋 Étape 1 : Préparation

### Vérifier que le backend est démarré
```bash
docker-compose exec backend python -c "print('Backend accessible')"
```

---

## 🔧 Étape 2 : Créer le script de test des schémas

Créer le fichier `documentation-test-user/scripts/test_schemas_manual.py` :

```python
#!/usr/bin/env python3
"""
Test manuel des schémas Pydantic User
"""
import sys
sys.path.append('/app')

from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.models.user import UserRole
from datetime import datetime
import traceback

def test_user_create_valid():
    """Test 1 : UserCreate avec données valides"""
    print("🧪 Test 1: UserCreate avec données valides...")
    
    try:
        user_data = {
            "email": "agent@boaz-study.com",
            "nom": "AGENT",
            "prenom": "Boaz",
            "password": "agent1234",
            "role": UserRole.AGENT_BOAZ,
            "active": True
        }
        
        user_create = UserCreate(**user_data)
        
        print(f"✅ UserCreate validé avec succès:")
        print(f"   📧 Email: {user_create.email}")
        print(f"   👤 Nom: {user_create.nom} {user_create.prenom}")
        print(f"   🔐 Password: {'*' * len(user_create.password)}")
        print(f"   👔 Rôle: {user_create.role.value}")
        print(f"   ✅ Actif: {user_create.active}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        traceback.print_exc()
        return False

def test_user_login_valid():
    """Test 2 : UserLogin avec données valides"""
    print("\n🧪 Test 2: UserLogin avec données valides...")
    
    try:
        login_data = {
            "email": "bailleur@boaz-study.com",
            "password": "bailleur1234"
        }
        
        user_login = UserLogin(**login_data)
        
        print(f"✅ UserLogin validé avec succès:")
        print(f"   📧 Email: {user_login.email}")
        print(f"   🔐 Password: {'*' * len(user_login.password)}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_user_response():
    """Test 3 : UserResponse (simulation)"""
    print("\n🧪 Test 3: UserResponse (simulation)...")
    
    try:
        # Simuler des données comme si elles venaient de la DB
        response_data = {
            "id": 1,
            "email": "ceo@boaz-study.com",
            "nom": "CEO",
            "prenom": "Admin",
            "role": UserRole.ADMIN_GENERALE,
            "active": True,
            "created_at": datetime.now(),
            "updated_at": None
        }
        
        user_response = UserResponse(**response_data)
        
        print(f"✅ UserResponse validé avec succès:")
        print(f"   🆔 ID: {user_response.id}")
        print(f"   📧 Email: {user_response.email}")
        print(f"   👤 Nom: {user_response.nom} {user_response.prenom}")
        print(f"   👔 Rôle: {user_response.role.value}")
        print(f"   📅 Créé le: {user_response.created_at.strftime('%Y-%m-%d %H:%M')}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        traceback.print_exc()
        return False

def test_user_update():
    """Test 4 : UserUpdate avec champs optionnels"""
    print("\n🧪 Test 4: UserUpdate avec champs optionnels...")
    
    try:
        # Test avec seulement quelques champs
        update_data = {
            "nom": "NOUVEAU NOM",
            "active": False
        }
        
        user_update = UserUpdate(**update_data)
        
        print(f"✅ UserUpdate validé avec succès:")
        print(f"   👤 Nom: {user_update.nom}")
        print(f"   ✅ Actif: {user_update.active}")
        print(f"   📧 Email: {user_update.email}")  # Doit être None
        print(f"   👔 Rôle: {user_update.role}")   # Doit être None
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_validation_errors():
    """Test 5 : Validation des erreurs"""
    print("\n🧪 Test 5: Validation des erreurs...")
    
    tests_passed = 0
    
    # Test 5.1: Email invalide
    try:
        UserCreate(
            email="email_invalide",
            nom="Test",
            prenom="User",
            password="test1234",
            role=UserRole.CLIENT
        )
        print("❌ La validation email aurait dû échouer")
    except ValueError as e:
        print(f"✅ Validation email invalide correcte: {str(e)[:50]}...")
        tests_passed += 1
    
    # Test 5.2: Password trop court
    try:
        UserCreate(
            email="test@valid.com",
            nom="Test",
            prenom="User",
            password="123",  # Trop court
            role=UserRole.CLIENT
        )
        print("❌ La validation password court aurait dû échouer")
    except ValueError as e:
        print(f"✅ Validation password court correcte: {str(e)[:50]}...")
        tests_passed += 1
    
    # Test 5.3: Nom vide
    try:
        UserCreate(
            email="test@valid.com",
            nom="",  # Vide
            prenom="User",
            password="test1234",
            role=UserRole.CLIENT
        )
        print("❌ La validation nom vide aurait dû échouer")
    except ValueError as e:
        print(f"✅ Validation nom vide correcte: {str(e)[:50]}...")
        tests_passed += 1
    
    # Test 5.4: Login sans password
    try:
        UserLogin(
            email="test@valid.com",
            password=""  # Vide
        )
        print("❌ La validation login sans password aurait dû échouer")
    except ValueError as e:
        print(f"✅ Validation login sans password correcte: {str(e)[:50]}...")
        tests_passed += 1
    
    return tests_passed == 4

def test_all_roles_in_schemas():
    """Test 6 : Tous les rôles dans les schémas"""
    print("\n🧪 Test 6: Tous les rôles dans les schémas...")
    
    try:
        roles_to_test = [
            UserRole.CLIENT,
            UserRole.AGENT_BOAZ,
            UserRole.ADMIN_GENERALE,
            UserRole.BAILLEUR
        ]
        
        success_count = 0
        
        for role in roles_to_test:
            try:
                user = UserCreate(
                    email=f"test-{role.value}@boaz-study.com",
                    nom="Test",
                    prenom="User",
                    password="test1234",
                    role=role
                )
                print(f"   ✅ Rôle {role.value} validé")
                success_count += 1
            except Exception as e:
                print(f"   ❌ Rôle {role.value} échoué: {str(e)}")
        
        if success_count == len(roles_to_test):
            print("✅ Tous les rôles fonctionnent dans les schémas")
            return True
        else:
            print(f"❌ {len(roles_to_test) - success_count} rôles ont échoué")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Exécuter tous les tests des schémas Pydantic"""
    print("=" * 70)
    print("📝 TESTS SCHÉMAS PYDANTIC USER")
    print("=" * 70)
    
    success_count = 0
    
    if test_user_create_valid():
        success_count += 1
    
    if test_user_login_valid():
        success_count += 1
        
    if test_user_response():
        success_count += 1
        
    if test_user_update():
        success_count += 1
        
    if test_validation_errors():
        success_count += 1
        
    if test_all_roles_in_schemas():
        success_count += 1
    
    print("\n" + "=" * 70)
    print(f"📊 RÉSULTAT: {success_count}/6 tests réussis")
    
    if success_count == 6:
        print("🎉 TOUS LES TESTS SONT RÉUSSIS!")
        print("➡️  Vous pouvez passer au test suivant: 04-test-integration-complete.md")
        return True
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifiez les schémas dans backend/app/schemas/user.py")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
```

---

## ▶️ Étape 3 : Exécuter le test

```bash
# Copier et exécuter le script de test des schémas
docker cp documentation-test-user/scripts/test_schemas_manual.py boaz-backend:/app/test_schemas_manual.py
docker-compose exec backend python /app/test_schemas_manual.py
```

---

## ✅ Résultats attendus

```
======================================================================
📝 TESTS SCHÉMAS PYDANTIC USER
======================================================================
🧪 Test 1: UserCreate avec données valides...
✅ UserCreate validé avec succès:
   📧 Email: agent@boaz-study.com
   👤 Nom: Agent Boaz
   🔐 Password: ********
   👔 Rôle: agent-boaz
   ✅ Actif: True

🧪 Test 2: UserLogin avec données valides...
✅ UserLogin validé avec succès:
   📧 Email: bailleur@boaz-study.com
   🔐 Password: *************

🧪 Test 3: UserResponse (simulation)...
✅ UserResponse validé avec succès:
   🆔 ID: 1
   📧 Email: ceo@boaz-study.com
   👤 Nom: Ceo Admin
   👔 Rôle: admin-generale
   📅 Créé le: 2025-09-02 15:30

🧪 Test 4: UserUpdate avec champs optionnels...
✅ UserUpdate validé avec succès:
   👤 Nom: Nouveau Nom
   ✅ Actif: False
   📧 Email: None
   👔 Rôle: None

🧪 Test 5: Validation des erreurs...
✅ Validation email invalide correcte: 1 validation error for UserCreate...
✅ Validation password court correcte: 1 validation error for UserCreate...
✅ Validation nom vide correcte: 1 validation error for UserCreate...
✅ Validation login sans password correcte: 1 validation error for UserLogin...

🧪 Test 6: Tous les rôles dans les schémas...
   ✅ Rôle client validé
   ✅ Rôle agent-boaz validé
   ✅ Rôle admin-generale validé
   ✅ Rôle bailleur validé
✅ Tous les rôles fonctionnent dans les schémas

======================================================================
📊 RÉSULTAT: 6/6 tests réussis
🎉 TOUS LES TESTS SONT RÉUSSIS!
➡️  Vous pouvez passer au test suivant: 04-test-integration-complete.md
```

---

## 🔍 Que vérifier

1. **✅ UserCreate** : Création avec tous les champs obligatoires
2. **✅ UserLogin** : Login simple avec email/password
3. **✅ UserResponse** : Réponse API (sans password exposé)
4. **✅ UserUpdate** : Mise à jour avec champs optionnels
5. **✅ Validations** : Toutes les erreurs de validation détectées
6. **✅ Rôles** : Tous les 4 rôles fonctionnent dans les schémas

---

## 🚨 En cas d'erreur

### ImportError schémas
```bash
# Vérifier que les schémas existent
docker-compose exec backend ls -la /app/app/schemas/

# Vérifier le contenu du fichier
docker-compose exec backend cat /app/app/schemas/user.py
```

### Erreur de validation inattendue
- Vérifier les décorateurs `@validator` dans les schémas
- Vérifier que les regex d'email sont correctes
- Vérifier que les longueurs minimales sont cohérentes

### Erreur UserRole
- Vérifier l'import dans le schéma : `from app.models.user import UserRole`
- Vérifier que le modèle User est correctement importé

---

## ➡️ Étape suivante

Si tous les tests sont réussis, passez à :
**[04-test-integration-complete.md](./04-test-integration-complete.md)**