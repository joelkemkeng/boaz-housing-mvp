#!/usr/bin/env python3
"""
Service de génération de l'Attestation de logement et prise en charge PDF (2 pages)
Selon le modèle Livin France adapté à Boaz-Housing

Story 4.2 : Service génération Attestation logement + prise en charge PDF
Epic 4 : GÉNÉRATION DOCUMENTS PDF
"""

import json
import os
import qrcode
import tempfile
from datetime import datetime
from typing import Dict, List, Any
from jinja2 import Template
import subprocess
import platform
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def find_wkhtmltopdf():
    """Cherche wkhtmltopdf sur le système"""
    possible_paths = [
        # Windows
        r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
        r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe",
        # Linux
        "/usr/bin/wkhtmltopdf",
        "/usr/local/bin/wkhtmltopdf",
        # macOS
        "/opt/homebrew/bin/wkhtmltopdf",
        "/usr/local/bin/wkhtmltopdf"
    ]
    
    # Vérifier dans le PATH
    try:
        result = subprocess.run(['wkhtmltopdf', '--version'], 
                                capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return 'wkhtmltopdf'
    except:
        pass
    
    # Vérifier les chemins spécifiques
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def get_attestation_html_template():
    """Template HTML exact du fichier backend/brouillon/template-attestation.html"""
    return """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Attestation de logement</title>
    <style>
        @page {
            size: A4;
            margin: 10mm;
        }
        
        * {
            box-sizing: border-box;
        }
        
        body {
            font-family: "Segoe UI", "Arial", sans-serif;
            margin: 0;
            padding: 0;
            line-height: 1.4;
            color: #2c3e50;
            font-size: 10pt;
            background: #f8f9fa;
            min-height: 100vh;
        }
        
        .document-container {
            max-width: 210mm;
            margin: 0 auto;
            padding: 5mm 12mm 5mm 12mm;
            background: #ffffff;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
            position: relative;
        }
        
        .document-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: #f88206;
        }
        
        /*
        .document-container::after {
            content: '';
            position: absolute;
            
            left: 0;
            right: 0;
            bottom: 0;
            height: 3px;
            background: #0140ff;
        }*/
        
        .header {
            background: #ffffff;
            color: #2c3e50;
            padding: -20px 8px 10px 8px;
            text-align: center;
            position: relative;
            border-bottom: 1px solid #e8e8e8;
            margin-bottom: 10px;
        }
        
        .header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 45%;
            transform: translateX(-50%);
            width: 100px;
            height: 2px;
            background: #0140ff;
        }
        
       
        .logo-section {
            margin-bottom: 15px;
        }
        
        .logo-placeholder {
            width: 45px;
            height: 45px;
            background: #f8f9fa;
            border: 2px solid #0140ff;
            border-radius: 50%;
            margin: 0 auto 5px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            color: #0140ff;
            font-weight: 600;
        }
        
        .company-name {
            font-size: 12pt;
            font-weight: 600;
            letter-spacing: 1px;
            margin-bottom: 2px;
            color: #2c3e50;
        }
        
        .company-tagline {
            font-size: 8pt;
            color: #7f8c8d;
            font-style: italic;
        }
        
        .title-section {
            background: #ecf0f1;
            padding: 20px 12px;
            text-align: center;
            border-bottom: 1px solid #e8e8e8;
            margin-bottom: 25px;
        }
        
        .document-title {
            font-size: 16pt;
            font-weight: 600;
            color: #2c3e50;
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 2px;
            position: relative;
            display: inline-block;
            white-space: nowrap;
        }
        
        .document-title::after {
            content: '';
            position: absolute;
            bottom: -6px;
            left: 50%;
            transform: translateX(-50%);
            width: 40px;
            height: 2px;
            background: #f88206;
        }
        
        .content-section {
            padding: 0;
        }
        
        .intro-paragraph {
            background: #f8f9fa;
            padding: 15px 20px;
            border-left: 4px solid #0140ff;
            margin-bottom: 20px;
            border-radius: 0 4px 4px 0;
            font-size: 9pt;
            color: #5a6c7d;
        }
        
        .attestation-content {
            margin-bottom: 20px;
            padding: 0 10px;
        }
        
        .attestation-content p {
            margin: 15px 0;
            text-align: justify;
            color: #34495e;
            line-height: 1.6;
        }
        
        .highlight-box {
            background: #fafbff;
            border: 1px solid #0140ff;
            border-radius: 6px;
            padding: 20px;
            margin: 20px 0;
            position: relative;
        }
        
        .address-info {
            font-weight: 600;
            color: #2c3e50;
            font-size: 11pt;
            text-align: center;
        }
        
        .rental-details {
            display: table;
            table-layout: fixed;
            width: 100%;
            margin: 15px 0;
            border-spacing: 12px 0;
        }
        
        .detail-item {
            display: table-cell;
            width: 50%;
            background: white;
            padding: 12px;
            border-radius: 4px;
            border: 1px solid #e8e8e8;
            text-align: center;
            vertical-align: top;
        }
        
        .detail-label {
            font-size: 9pt;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }
        
        .detail-value {
            font-size: 11pt;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .signature-section {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px dashed #bdc3c7;
        }
        
        .signature-container {
            display: table;
            table-layout: fixed;
            width: 100%;
            margin: 0 auto;
            padding: 0 10px;
        }
        
        .qr-section {
            display: table-cell;
            width: 50%;
            text-align: center;
            vertical-align: top;
            padding-right: 20px;
        }
        
        .qr-placeholder {
            width: 160px;
            height: 160px;
            background: #f8f9fa;
            border: 2px dashed #bdc3c7;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 5px;
            font-size: 7pt;
            color: #7f8c8d;
            text-align: center;
            line-height: 1.0;
        }
        
        .signature-details {
            display: table-cell;
            width: 50%;
            text-align: right;
            vertical-align: top;
            padding-left: 20px;
        }
        
        .stamp {
            width: 200px;
            height: auto;
            transform: rotate(-10deg);
            transform-origin: center center;
            -webkit-transform: rotate(-10deg);
            -moz-transform: rotate(-10deg);
            -ms-transform: rotate(-10deg);
            -o-transform: rotate(-10deg);
            margin: 15px 0;
            filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.1));
            display: inline-block;
        }
        
        .company-info {
            font-size: 8pt;
            color: #5a6c7d;
            line-height: 1.3;
        }
        
        .footer {
            background: #ffffff;
            color: #2c3e50;
            padding: 20px 10px;
            text-align: center;
            margin-top: 25px;
            border-top: 1px solid #e8e8e8;
        }
        
        .reference-info {
            display: flex;
            justify-content: center;
            font-size: 8pt;
        }
        
        .contact-person, .document-ref {
            background: #f8f9fa;
            padding: 12px;
            border-radius: 4px;
            border: 1px solid #e8e8e8;
        }
        
        .contact-person h4, .document-ref h4 {
            margin: 0 0 8px 0;
            color: #f88206;
            font-size: 8pt;
        }
        
        .validity-notice {
            margin-top: 15px;
            padding: 12px;
            background: #fff5f0;
            border: 1px solid #f88206;
            border-radius: 4px;
            font-size: 7pt;
            color: #d35400;
            text-align: center;
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
                font-size: 9pt;
                line-height: 1.3;
            }
            .document-container {
                box-shadow: none;
                border-radius: 0;
                max-width: none;
                margin: 0;
            }
            .validity-notice {
                background: #f8f8f8;
                border: 1px solid #ddd;
            }
            .header, .title-section, .content-section, .footer {
                page-break-inside: avoid;
            }
            .attestation-content p {
                orphans: 2;
                widows: 2;
            }
        }
    </style>
</head>
<body>
    <div class="document-container">
        <header class="header">
            <div class="logo-section">
                <img src="/app/app/static/assets/logo-boaz-housing.png" alt="Boaz Housing Logo" style="width: 220px; height: auto; margin-bottom: 10px;">
                <!-- <div class="company-name">{{ nom_organisation }}</div> -->
                <div class="company-tagline">Votre partenaire logement en France</div>
            </div>
        </header>

        <section class="title-section">
            <h1 class="document-title">Attestation de logement</h1>
        </section>

        <main class="content-section">
            <div class="intro-paragraph">
                <strong>{{ site_organisation }}</strong> est un site web exploité par <strong>{{ nom_complet_organisation }}</strong>, une entreprise de l'économie sociale et solidaire qui a pour objet social l'insertion sociale, scolaire et professionnelle des étrangers en France.
            </div>

            <div class="attestation-content">
                <p><strong>{{ nom_complet_ceo }}</strong>, né le {{ date_naissance_ceo }} à {{ ville_naissance_ceo }} en {{ pays_naissance_ceo }}, Président Directeur Générale de la société {{ nom_complet_organisation }} exploitant le site web {{ site_organisation }}, dont le siège social est situé au {{ adresse_organisation }}, inscrite au R.C.S. de {{ ville_organisation }} sous le numéro {{ numero_rcs_organisation }}, code NAF : {{ code_naf_organisation }}, <strong>atteste sur l'honneur que :</strong></p>

                <p><strong>{{ nom_complet_client }}</strong> née le {{ date_naissance_client }} à {{ ville_naissance_client }}, {{ pays_naissance_client }}, logera dans l'un des logements proposés par la plateforme {{ site_organisation }} situé à l'adresse ci-dessous :</p>

                <div class="highlight-box">
                    <div class="address-info">
                        {{ adresse_logement }}
                    </div>
                    <div class="rental-details">
                        <div class="detail-item">
                            <div class="detail-label">Loyer mensuel</div>
                            <div class="detail-value">{{ montant_loyer_logement }} €</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Date d'entrée</div>
                            <div class="detail-value">{{ date_entree_logement }}</div>
                        </div>
                    </div>
                    <div class="detail-item" style="width: 100%; margin-top: 5px; display: block;">
                        <div class="detail-label">Durée de location estimée</div>
                        <div class="detail-value">{{ duree_location_souscription }}</div>
                    </div>
                </div>

                <p>Nous restons à votre disposition pour tout complément d'information. Ce document ne peut être revendu.</p>
            </div>

            <div class="signature-section">
                <div class="signature-container">
                    <div class="qr-section">
                        <div class="qr-placeholder">
                            <img src="data:image/png;base64,{{ qr_code_base64 }}" alt="QR Code" style="width: 160px; height: 160px;">
                        </div>
                        <div style="font-size: 8pt; color: #7f8c8d;">Code de vérification</div>
                        <div style="font-size: 7pt; color: #7f8c8d; margin-top: 5px; text-align: center;">Flasher ce code QR pour vérifier la validité de ce document</div>
                    </div>

                    <div class="signature-details">
                        <p style="margin-bottom: 5px; font-weight: 600;">Fait à {{ ville_organisation }} en {{ pays_organisation }}</p>
                        <p style="margin-bottom: 20px; color: #7f8c8d;">Le {{ date_emission_document }}</p>
                        
                        <img src="/app/app/static/assets/cachet-bs-rouge-rectangle.jpeg" alt="Cachet Boaz Study" class="stamp">

                        <div class="company-info">
                            <strong>{{ nom_complet_organisation }}</strong><br>
                            R.C.S. {{ numero_rcs_organisation }}  <br>
                            {{ email_contact_organisation }}<br>
                            {{ adresse_organisation }}
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <footer class="footer">
            <div class="reference-info">
                <div class="document-ref">
                    <h4>Référence du document</h4>
                    <p><strong>{{ reference_document }}</strong></p>
                </div>
            </div>

            <div class="validity-notice">
                <strong>IMPORTANT :</strong> Cette attestation est valide pendant {{ duree_validite_document }} jours après la date d'émission
            </div>
        </footer>
    </div>
</body>
</html>"""

def generate_qr_code(reference: str, base_url: str = "https://boaz-study.com") -> str:
    """Génère un QR code avec URL de vérification et retourne en base64"""
    verification_url = f"{base_url}/verify?ref={reference}"
    
    # Générer QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=4,
        border=2,
    )
    qr.add_data(verification_url)
    qr.make(fit=True)
    
    # Créer image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Convertir en base64
    import io
    import base64
    buffer = io.BytesIO()
    qr_img.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return qr_base64

class AttestationGenerator:
    """Générateur d'Attestation de logement et prise en charge PDF (2 pages)
    Selon modèle Livin France adapté Boaz-Housing"""
    
    def __init__(self):
        pass
    
    def generate_attestation(
        self,
        client_data: Dict[str, Any],
        logement_data: Dict[str, Any],
        souscription_data: Dict[str, Any],
        organisation_data: Dict[str, Any],
        reference: str
    ) -> str:
        """
        Génère l'Attestation de logement et prise en charge PDF (2 pages)
        
        Args:
            client_data: Données du client
            logement_data: Données du logement
            souscription_data: Données de la souscription
            organisation_data: Données de l'organisation
            reference: Référence unique de la souscription
            
        Returns:
            str: Chemin vers le fichier PDF généré
        """
        try:
            # Génération QR code
            qr_code_base64 = generate_qr_code(reference)
            
            # Préparation des données pour le template
            template_data = self._prepare_template_data(
                client_data, logement_data, souscription_data, 
                organisation_data, reference, qr_code_base64
            )
            
            # Génération HTML
            template = Template(get_attestation_html_template())
            html_content = template.render(**template_data)
            
            # Génération PDF avec wkhtmltopdf
            pdf_filename = f"Attestation_{reference}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            output_path = os.path.join(tempfile.gettempdir(), pdf_filename)
            
            self._generate_pdf_from_html(html_content, output_path)
            
            logger.info(f"Attestation PDF générée: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Erreur génération Attestation PDF: {str(e)}")
            raise e
    
    def _prepare_template_data(
        self, 
        client_data: Dict, 
        logement_data: Dict,
        souscription_data: Dict,
        organisation_data: Dict,
        reference: str,
        qr_code_base64: str
    ) -> Dict:
        """Prépare les données pour le template HTML exact"""
        
        # Extraction initiales de l'organisation (ex: "Boaz Housing" -> "BH")
        nom_org = organisation_data.get('nom_complet', organisation_data.get('nom', 'Boaz Housing'))
        initiales = ''.join([word[0].upper() for word in nom_org.split() if word])[:2]
        
        return {
            # Organisation
            'nom_organisation_initiales': initiales,
            'nom_organisation': nom_org,
            'site_organisation': organisation_data.get('site_web', 'boaz-study.com'),
            'nom_complet_organisation': nom_org,
            'adresse_organisation': organisation_data.get('adresse', ''),
            'numero_rcs_organisation': organisation_data.get('numero_rcs', ''),
            'code_naf_organisation': organisation_data.get('code_naf', ''),
            'ville_organisation': organisation_data.get('ville_rcs', 'Lille'),
            'pays_organisation': 'France',
            'email_contact_organisation': organisation_data.get('email', ''),
            
            # CEO/Directeur
            'nom_complet_ceo': organisation_data.get('ceo', {}).get('nom_complet', ''),
            'date_naissance_ceo': organisation_data.get('ceo', {}).get('date_naissance', ''),
            'ville_naissance_ceo': organisation_data.get('ceo', {}).get('ville_naissance', ''),
            'pays_naissance_ceo': organisation_data.get('ceo', {}).get('pays_naissance', ''),
            
            # Client
            'nom_complet_client': f"{client_data.get('prenom', '')} {client_data.get('nom', '')}".strip(),
            'date_naissance_client': client_data.get('date_naissance', ''),
            'ville_naissance_client': client_data.get('ville_naissance_client', ''),
            'pays_naissance_client': client_data.get('pays_naissance_client', ''),
            
            # Logement
            'adresse_logement': f"{logement_data.get('adresse', '')}, {logement_data.get('ville', '')}, {logement_data.get('pays', 'France')}",
            'montant_loyer_logement': int(logement_data.get('prix_mois', 0)),
            'date_entree_logement': souscription_data.get('date_entree_prevue', ''),
            'duree_location_souscription': f"{souscription_data.get('duree_location_mois', 12)} mois",
            
            # Document
            'reference_document': reference,
            'date_emission_document': datetime.now().strftime('%d/%m/%Y'),
            'duree_validite_document': '45',
            'qr_code_base64': qr_code_base64
        }
    
    def _generate_pdf_from_html(self, html_content: str, output_path: str):
        """Génère PDF à partir du HTML avec wkhtmltopdf"""
        temp_html_path = None
        
        try:
            # Sauvegarder HTML temporaire
            with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as temp_file:
                temp_file.write(html_content)
                temp_html_path = temp_file.name
            
            # Utiliser wkhtmltopdf
            wkhtmltopdf_path = find_wkhtmltopdf()
            
            if not wkhtmltopdf_path:
                raise Exception("wkhtmltopdf n'est pas installé - REQUIS pour la génération PDF")
            
            # Paramètres optimisés pour l'attestation 2 pages
            cmd = [
                wkhtmltopdf_path,
                '--page-size', 'A4',
                '--margin-top', '1',
                '--margin-right', '1', 
                '--margin-bottom', '1',
                '--margin-left', '1',
                '--encoding', 'UTF-8',
                '--enable-local-file-access',
                '--print-media-type',
                #'--no-outline',
                temp_html_path,
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                logger.info(f"Attestation PDF générée avec wkhtmltopdf: {output_path}")
            else:
                logger.error(f"Erreur wkhtmltopdf: {result.stderr}")
                raise Exception(f"Erreur wkhtmltopdf: {result.stderr}")
                
        finally:
            # Nettoyer le fichier temporaire
            if temp_html_path and os.path.exists(temp_html_path):
                os.remove(temp_html_path)