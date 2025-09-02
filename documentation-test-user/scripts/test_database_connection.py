#!/usr/bin/env python3
"""
Test de la structure de la base de données après migration
"""
import sys
sys.path.append('/app')

from sqlalchemy import create_engine, text, inspect
from app.database import get_db, engine
import os

def test_database_connection():
    """Test 1 : Connexion à la base de données"""
    print("🧪 Test 1: Connexion à la base de données...")
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
        print("✅ Connexion à la base de données réussie")
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion: {str(e)}")
        return False

def test_users_table_exists():
    """Test 2 : Vérifier que la table users existe"""
    print("\n🧪 Test 2: Existence de la table users...")
    
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if 'users' in tables:
            print("✅ Table 'users' trouvée")
            return True
        else:
            print("❌ Table 'users' non trouvée")
            print(f"Tables disponibles: {tables}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_users_table_structure():
    """Test 3 : Vérifier la structure de la table users"""
    print("\n🧪 Test 3: Structure de la table users...")
    
    try:
        inspector = inspect(engine)
        columns = inspector.get_columns('users')
        
        expected_columns = {
            'id': 'INTEGER',
            'email': 'VARCHAR',
            'nom': 'VARCHAR', 
            'prenom': 'VARCHAR',
            'password_hash': 'VARCHAR',
            'role': 'USER-DEFINED',  # Enum
            'active': 'BOOLEAN',
            'created_at': 'TIMESTAMP',
            'updated_at': 'TIMESTAMP'
        }
        
        print("📋 Colonnes trouvées:")
        found_columns = {}
        for col in columns:
            col_type = str(col['type']).upper()
            found_columns[col['name']] = col_type
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            default = f" DEFAULT {col['default']}" if col['default'] else ""
            print(f"   ✓ {col['name']}: {col_type} {nullable}{default}")
        
        # Vérifier les colonnes essentielles
        missing_columns = []
        for col_name in expected_columns:
            if col_name not in found_columns:
                missing_columns.append(col_name)
        
        if missing_columns:
            print(f"❌ Colonnes manquantes: {missing_columns}")
            return False
        else:
            print("✅ Toutes les colonnes essentielles sont présentes")
            return True
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_userrole_enum():
    """Test 4 : Vérifier l'enum userrole"""
    print("\n🧪 Test 4: Enum userrole...")
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT enumlabel 
                FROM pg_enum e 
                JOIN pg_type t ON e.enumtypid = t.oid 
                WHERE t.typname = 'userrole'
                ORDER BY enumlabel
            """))
            
            enum_values = [row[0] for row in result]
            expected_values = ['admin-generale', 'agent-boaz', 'bailleur', 'client']
            
            print(f"📋 Valeurs enum trouvées: {enum_values}")
            
            if set(enum_values) == set(expected_values):
                print("✅ Enum userrole correcte")
                return True
            else:
                print(f"❌ Enum incorrecte")
                print(f"   Attendu: {expected_values}")
                print(f"   Trouvé: {enum_values}")
                return False
                
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def test_indexes():
    """Test 5 : Vérifier les index"""
    print("\n🧪 Test 5: Index sur la table users...")
    
    try:
        inspector = inspect(engine)
        indexes = inspector.get_indexes('users')
        
        print("📋 Index trouvés:")
        for idx in indexes:
            columns = ", ".join(idx['column_names'])
            unique = " (UNIQUE)" if idx['unique'] else ""
            print(f"   ✓ {idx['name']}: {columns}{unique}")
        
        # Vérifier qu'il y a au moins l'index sur email
        email_index_found = any(
            'email' in idx['column_names'] for idx in indexes
        )
        
        if email_index_found:
            print("✅ Index sur email trouvé")
            return True
        else:
            print("❌ Index sur email manquant")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Exécuter tous les tests de base de données"""
    print("=" * 70)
    print("🗃️  TESTS MIGRATION BASE DE DONNÉES")
    print("=" * 70)
    
    success_count = 0
    
    if test_database_connection():
        success_count += 1
    
    if test_users_table_exists():
        success_count += 1
        
    if test_users_table_structure():
        success_count += 1
        
    if test_userrole_enum():
        success_count += 1
        
    if test_indexes():
        success_count += 1
    
    print("\n" + "=" * 70)
    print(f"📊 RÉSULTAT: {success_count}/5 tests réussis")
    
    if success_count == 5:
        print("🎉 TOUS LES TESTS SONT RÉUSSIS!")
        print("➡️  Vous pouvez passer au test suivant: 03-test-schemas-pydantic.md")
        return True
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifiez la migration Alembic ou relancez-la")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)