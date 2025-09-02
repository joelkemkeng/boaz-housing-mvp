# Service Email - Boaz Housing MVP

## Vue d'ensemble

Le service d'envoi d'emails permet d'envoyer automatiquement les documents PDF (Proforma et Attestation) aux clients par email.

## Configuration

### Variables d'environnement (.env)

```bash
# Configuration SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=votre-email@gmail.com
SMTP_PASSWORD=votre-mot-de-passe-application
FROM_EMAIL=info@boaz-study.fr
```

### Pour Gmail

1. Activer l'authentification à 2 facteurs
2. Générer un "Mot de passe d'application" 
3. Utiliser ce mot de passe dans `SMTP_PASSWORD`

### Pour tests locaux (recommandé)

Utilisez Mailtrap (service de test gratuit) :

```bash
SMTP_HOST=sandbox.smtp.mailtrap.io
SMTP_PORT=2525
SMTP_USERNAME=votre-username-mailtrap
SMTP_PASSWORD=votre-password-mailtrap
```

## Endpoints API

### 1. Envoyer Proforma par email

```http
POST /api/souscriptions/{souscription_id}/send-proforma-email
Content-Type: application/json

{
  "to_email": "client@example.com",
  "client_name": "Jean Martin"
}
```

### 2. Envoyer Attestation par email

```http
POST /api/souscriptions/{souscription_id}/send-attestation-email
Content-Type: application/json

{
  "to_email": "client@example.com", 
  "client_name": "Jean Martin"
}
```

### 3. Tester la connexion SMTP

```http
GET /api/souscriptions/test-email-connection
```

## Templates Email

### Proforma
- **Objet :** "Votre Proforma Boaz-Housing - Ref: {reference}"
- **Contenu :** HTML avec infos client et pièce jointe PDF
- **Pièce jointe :** Proforma_{reference}.pdf

### Attestation  
- **Objet :** "Votre Attestation de Logement - Ref: {reference}"
- **Contenu :** HTML avec instructions et pièce jointe PDF
- **Pièce jointe :** Attestation_{reference}.pdf

## Utilisation dans le code

```python
from app.services.email_service import email_service

# Envoyer Proforma
success = email_service.send_proforma_email(
    to_email="client@example.com",
    pdf_bytes=pdf_data,
    reference="ATT-123456",
    client_name="Jean Martin"
)

# Tester connexion
is_connected = email_service.test_connection()
```

## Gestion d'erreurs

- ✅ Retry automatique en cas d'échec temporaire
- ✅ Logging des erreurs dans les logs
- ✅ Messages d'erreur explicites dans l'API
- ✅ Timeout connexion SMTP (30 secondes)

## MVP - Simplicité

Pour le MVP, le service est volontairement simple :
- Pas de file d'attente (envoi immédiat)
- Templates HTML basiques mais professionnels  
- Configuration via variables d'environnement
- Gestion d'erreur simple et robuste

Cette approche permet un déploiement rapide tout en restant fonctionnel et professionnel.