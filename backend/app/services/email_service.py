import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        # Configuration SMTP depuis variables d'environnement
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', os.getenv('EMAIL_FROM', 'info@boaz-study.fr'))
        self.use_tls = os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'
    
    def send_proforma_email(self, to_email: str, pdf_bytes: bytes, reference: str, client_name: str = "") -> bool:
        """Envoie le Proforma par email avec pièce jointe PDF"""
        try:
            subject = f"Votre Proforma Boaz-Housing - Ref: {reference}"
            
            # Template HTML simple pour Proforma
            body = f"""
            <html>
            <body>
                <h2>Bonjour {client_name},</h2>
                <p>Veuillez trouver ci-joint votre Proforma pour votre demande d'attestation de logement.</p>
                
                <p><strong>Référence :</strong> {reference}</p>
                
                <p>Ce document contient les détails de votre souscription. Veuillez le conserver précieusement.</p>
                
                <p>Cordialement,<br>
                L'équipe Boaz-Housing</p>
                
                <hr>
                <p><small>
                Boaz-Housing<br>
                14 Rue Jean Piestre, Corbeil-Essonnes, 91100, France<br>
                Email: info@boaz-study.fr<br>
                Tél: +33 01 84 18 02 67<br>
                Site: www.boaz-study.com
                </small></p>
            </body>
            </html>
            """
            
            filename = f"Proforma_{reference}.pdf"
            
            return self._send_email(to_email, subject, body, pdf_bytes, filename)
            
        except Exception as e:
            logger.error(f"Erreur envoi Proforma: {str(e)}")
            return False
    
    def send_attestation_email(self, to_email: str, pdf_bytes: bytes, reference: str, client_name: str = "") -> bool:
        """Envoie l'Attestation par email avec pièce jointe PDF"""
        try:
            subject = f"Votre Attestation de Logement - Ref: {reference}"
            
            # Template HTML simple pour Attestation
            body = f"""
            <html>
            <body>
                <h2>Bonjour {client_name},</h2>
                <p>Félicitations ! Votre attestation de logement et de prise en charge est prête.</p>
                
                <p><strong>Référence :</strong> {reference}</p>
                
                <p>Veuillez trouver ci-joint votre attestation officielle. Ce document est valable 45 jours à compter de sa date d'émission.</p>
                
                <p><strong>Important :</strong> Conservez ce document précieusement, il vous sera demandé pour vos démarches administratives.</p>
                
                <p>Cordialement,<br>
                L'équipe Boaz-Housing</p>
                
                <hr>
                <p><small>
                Boaz-Housing<br>
                14 Rue Jean Piestre, Corbeil-Essonnes, 91100, France<br>
                Email: info@boaz-study.fr<br>
                Tél: +33 01 84 18 02 67<br>
                Site: www.boaz-study.com
                </small></p>
            </body>
            </html>
            """
            
            filename = f"Attestation_{reference}.pdf"
            
            return self._send_email(to_email, subject, body, pdf_bytes, filename)
            
        except Exception as e:
            logger.error(f"Erreur envoi Attestation: {str(e)}")
            return False
    
    def _send_email(self, to_email: str, subject: str, body: str, pdf_bytes: Optional[bytes] = None, filename: Optional[str] = None) -> bool:
        """Méthode privée pour envoyer un email avec pièce jointe optionnelle"""
        try:
            # Créer le message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Ajouter le corps HTML
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            # Ajouter la pièce jointe PDF si fournie
            if pdf_bytes and filename:
                pdf_part = MIMEApplication(pdf_bytes, _subtype='pdf')
                pdf_part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                msg.attach(pdf_part)
            
            # Envoyer l'email
            if self.smtp_port == 465:
                # Port 465 = SSL complet
                with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
                    if self.smtp_username and self.smtp_password:
                        server.login(self.smtp_username, self.smtp_password)
                    server.send_message(msg)
            else:
                # Port 587 = STARTTLS
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    if self.use_tls:
                        server.starttls()
                    if self.smtp_username and self.smtp_password:
                        server.login(self.smtp_username, self.smtp_password)
                    server.send_message(msg)
            
            logger.info(f"Email envoyé avec succès à {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur envoi email à {to_email}: {str(e)}")
            return False
    
    def test_connection(self) -> bool:
        """Teste la connexion SMTP"""
        try:
            if self.smtp_port == 465:
                # Port 465 = SSL complet
                with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
                    if self.smtp_username and self.smtp_password:
                        server.login(self.smtp_username, self.smtp_password)
            else:
                # Port 587 = STARTTLS
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    if self.use_tls:
                        server.starttls()
                    if self.smtp_username and self.smtp_password:
                        server.login(self.smtp_username, self.smtp_password)
            return True
        except Exception as e:
            logger.error(f"Erreur test connexion SMTP: {str(e)}")
            return False

# Instance globale
email_service = EmailService()