import json
from datetime import datetime
import os
import uuid
import subprocess
import platform
import logging
import tempfile
from typing import Dict, List, Any
from jinja2 import Template

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def format_currency(amount: float) -> str:
    """Formate les montants avec des espaces comme séparateurs de milliers"""
    return f"{amount:,.0f}".replace(",", " ")

def get_html_template():
    """Template HTML moderne professionnel correspondant exactement au design de référence"""
    return """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facture - Boaz Study Cameroun</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #ffffff;
            color: #333333;
            font-size: 11px;
            line-height: 1.5;
            padding: 15mm;
        }

        /* Container principal avec hauteur complète */
        .invoice-container {
            width: 210mm;
            max-width: 210mm;
            min-height: 267mm; /* Hauteur A4 moins marges */
            margin: 0 auto;
            padding: 25px;
            background-color: #ffffff;
            border: 2px solid #0140FF;
            border-radius: 10px;
            position: relative;
            box-shadow: 0 2px 10px rgba(1, 64, 255, 0.1);
        }

        /* Header professionnel */
        .header-section {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            background-color: #f8f9fb;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-top: 4px solid #0140FF;
            border-left: 2px solid #F88206;
        }

        .logo-company-info {
            display: flex;
            align-items: flex-start;
            flex: 1;
        }

        .logo-section {
            margin-right: 25px;
        }

        .logo {
            width: 130px;
            height: auto;
            border-radius: 5px;
        }

        .company-info h2 {
            font-size: 15px;
            font-weight: 700;
            color: #0140FF;
            margin-bottom: 10px;
            letter-spacing: 0.3px;
        }

        .company-info p {
            font-size: 10px;
            color: #555;
            margin-bottom: 4px;
            line-height: 1.4;
        }

        .invoice-title-section {
            text-align: right;
            flex-shrink: 0;
            background-color: rgba(1, 64, 255, 0.85);
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
        }

        .invoice-title {
            font-size: 26px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 8px;
            letter-spacing: 1px;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        }

        .invoice-meta {
            font-size: 11px;
            color: rgba(255, 255, 255, 0.95);
            text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.2);
        }

        /* Section détails améliorée */
        .details-grid {
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
            gap: 40px;
            background-color: #fafbfc;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e8eaed;
        }

        .details-column {
            flex: 1;
        }

        .details-column.customer-column {
            text-align: right; /* Aligner "Facturé à" à droite */
        }

        .details-column h3 {
            font-size: 13px;
            font-weight: 700;
            color: #0140FF;
            border-bottom: 2px solid #F88206;
            padding-bottom: 6px;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .details-column p {
            font-size: 10px;
            margin-bottom: 5px;
            line-height: 1.4;
            color: #333;
        }

        .details-column p strong {
            color: #0140FF;
            font-weight: 600;
        }

        .bank-separator {
            height: 1px;
            background-color: #e0e0e0;
            margin: 12px 0;
        }

        /* Tableau moderne et lisible */
        .services-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 25px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .services-table thead th {
            background-color: rgba(1, 64, 255, 0.9);
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 15px 12px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.2);
        }

        .services-table tbody td {
            padding: 12px;
            border-bottom: 1px solid #e8eaed;
            font-size: 11px;
            vertical-align: middle;
        }

        .services-table tbody tr:nth-child(even) {
            background-color: #f8f9fb;
        }

        .services-table tbody tr:hover {
            background-color: rgba(1, 64, 255, 0.05);
        }

        .text-center { text-align: center; }
        .text-right { text-align: right; font-weight: 600; }

        /* Section totaux user-friendly */
        .totals-section {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-top: 30px;
            gap: 30px;
        }

        .recommendation-box {
            flex: 1;
            max-width: 60%;
        }

        .recommendation {
            border: 2px dashed #F88206;
            background-color: rgba(248, 130, 6, 0.08);
            padding: 15px;
            text-align: center;
            font-weight: 600;
            color: #F88206;
            font-size: 12px;
            border-radius: 8px;
            margin-bottom: 20px;
        }

        .totals-table-section {
            min-width: 280px;
        }

        .totals-table {
            width: 100%;
            border-collapse: collapse;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .totals-table tr td {
            padding: 12px 15px;
            font-size: 12px;
            border-bottom: 1px solid #e8eaed;
            background-color: #fafbfc;
        }

        .totals-table tr.total-ttc td {
            background-color: #F88206;
            color: white;
            font-weight: 700;
            font-size: 14px;
            border: none;
            padding: 15px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Section signature améliorée */
        .signature-section {
            text-align: right;
            margin-top: 25px;
            margin-right: 30px;
        }

        .signature-box {
            display: inline-block;
            text-align: center;
            position: relative;
            background-color: rgba(248, 130, 6, 0.02);
            padding: 15px;
            border-radius: 8px;
        }

        .signature-date {
            font-size: 10px;
            margin-bottom: 12px;
            color: #666;
            font-weight: 500;
        }

        .stamp {
            width: 140px;
            height: auto;
            transform: rotate(-8deg); /* Exactement -8° comme demandé */
            margin: 8px 0;
            filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.1));
        }

        /* Footer informatif */
        .footer {
            position: absolute;
            bottom: 20px;
            left: 25px;
            right: 25px;
            background-color: #f8f9fb;
            border-top: 3px solid #0140FF;
            border-left: 2px solid #F88206;
            padding: 15px;
            font-size: 9px;
            color: #666;
            text-align: justify;
            line-height: 1.4;
            border-radius: 6px;
        }

        /* Responsive et impression */
        @media print {
            body { 
                padding: 10mm;
                font-size: 10px;
            }
            .invoice-container {
                border: 1px solid #ddd;
                page-break-inside: avoid;
                min-height: auto;
                box-shadow: none;
            }
            .footer {
                position: relative;
                margin-top: 30px;
            }
        }
    </style>
</head>
<body>
    <div class="invoice-container">
        
        <!-- Header moderne avec logo Boaz Housing -->
        <div class="header-section">
            <div class="logo-company-info">
                <div class="logo-section">
                    <img src="/app/app/static/assets/logo-boaz-housing.png" alt="Boaz Housing Logo" class="logo">
                </div>
                <div class="company-info">
                    <h2>Boaz Study Cameroun SAS</h2>
                    <p>Yaoundé Total Ecole de Police - Tel: (+237) 658 870 473</p>
                    <p>389 Rue Toyota Bonapriso, B.P: 1230 Douala - Tel: (+237) 694 186 936</p>
                    <p>Email: info@boaz-study.com | Web: www.boaz-study.com</p>
                </div>
            </div>
            <div class="invoice-title-section">
                <h1 class="invoice-title">FACTURE</h1>
                <div class="invoice-meta">
                    <p>Date : {{ date }}</p>
                    {% if invoice_number %}
                    <p>N° : {{ invoice_number }}</p>
                    {% endif %}
                </div>
            </div>
        </div>

        <!-- Section coordonnées bancaires et client -->
        <div class="details-grid">
            <div class="details-column">
                <h3>Coordonnées Bancaires</h3>
                <p><strong>Payable à :</strong> BOAZ STUDY CAMEROUN</p>
                {% for bank in banks %}
                <p><strong>Banque :</strong> {{ bank.bank_name }}</p>
                {% if bank.iban %}
                <p><strong>IBAN :</strong> {{ bank.iban }}</p>
                {% endif %}
                {% if bank.swift_code %}
                <p><strong>CODE SWIFT :</strong> {{ bank.swift_code }}</p>
                {% endif %}
                {% if bank.account_number %}
                <p><strong>N° Compte :</strong> {{ bank.account_number }}</p>
                {% endif %}
                {% if not loop.last %}
                <div class="bank-separator"></div>
                {% endif %}
                {% endfor %}
            </div>
            
            <div class="details-column customer-column">
                <h3>Facturé à</h3>
                <p><strong>{{ customer.name }}</strong></p>
                <p><strong>Adresse :</strong> {{ customer.address }}</p>
                <p><strong>Mail :</strong> {{ customer.email }}</p>
                {% if customer.phone %}
                <p><strong>Téléphone :</strong> {{ customer.phone }}</p>
                {% endif %}
            </div>
        </div>

        <!-- Tableau des services -->
        <table class="services-table">
            <thead>
                <tr>
                    <th style="text-align: left; width: 40%;">DESCRIPTION</th>
                    <th style="width: 10%;">QTÉ</th>
                    <th style="width: 25%;">PRIX UNITAIRE</th>
                    <th style="width: 25%;">MONTANT</th>
                </tr>
            </thead>
            <tbody>
                {% for item in items %}
                <tr>
                    <td>{{ item.description }}</td>
                    <td class="text-center">{{ item.quantity }}</td>
                    <td class="text-right">{{ format_currency(item.unit_price) }}</td>
                    <td class="text-right">{{ format_currency(item.amount) }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <!-- Section totaux et signature -->
        <div class="totals-section">
            <div class="recommendation-box">
                {% if notes %}
                <div class="recommendation">{{ notes }}</div>
                {% endif %}
            </div>
            
            <div class="totals-table-section">
                <table class="totals-table">
                    <tr>
                        <td>Total HT</td>
                        <td class="text-right">{{ format_currency(total_ht) }} FCFA</td>
                    </tr>
                    <tr class="total-ttc">
                        <td><strong>Total TTC</strong></td>
                        <td class="text-right"><strong>{{ format_currency(total_ttc) }} FCFA</strong></td>
                    </tr>
                </table>
                
                <div class="signature-section">
                    <div class="signature-box">
                        <div class="signature-date">Boaz-Housing {{ date }}</div>
                        <img src="/app/app/static/assets/cachet-bs-rouge-rectangle.jpeg" alt="Cachet Boaz Study" class="stamp">
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            {% if terms %}
            <strong>Terms and conditions:</strong> {{ terms }}
            {% else %}
            <strong>Terms and conditions:</strong> Cette facture sera payable au plus tard 30 jours après réception. Les montants en retard sont sujets à des frais de retard de 10% par mois.
            {% endif %}
        </div>
    </div>
</body>
</html>"""

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

def generate_pdf_from_html(proforma_data: dict, output_path: str):
    """Génère un PDF à partir du template HTML exact - UNIQUEMENT AVEC WKHTMLTOPDF"""
    
    temp_html_path = None
    
    try:
        # Créer le template Jinja2
        template = Template(get_html_template())
        
        # Fonction helper pour le formatage des devises
        def currency_filter(value):
            return format_currency(value)
        
        # Rendu du template avec les données exactement comme le code de référence
        html_content = template.render(
            customer=proforma_data.get('customer', {}),
            items=proforma_data.get('items', []),
            banks=proforma_data.get('banks', []),
            date=proforma_data.get('date', ''),
            invoice_number=proforma_data.get('invoice_number', ''),
            total_ht=proforma_data.get('total_ht', 0),
            total_ttc=proforma_data.get('total_ttc', 0),
            notes=proforma_data.get('notes', ''),
            terms=proforma_data.get('terms', ''),
            format_currency=currency_filter
        )
        
        # Sauvegarder le HTML temporaire de manière sécurisée
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as temp_file:
            temp_file.write(html_content)
            temp_html_path = temp_file.name
        
        # UNIQUEMENT wkhtmltopdf - comme le code de référence
        wkhtmltopdf_path = find_wkhtmltopdf()
        
        if not wkhtmltopdf_path:
            raise Exception("wkhtmltopdf n'est pas installé - REQUIS pour la génération PDF")
        
        # Utiliser wkhtmltopdf exactement comme le code de référence
        is_linux = platform.system().lower() == 'linux'
        
        if is_linux:
            # Paramètres optimisés pour Ubuntu/Linux (du code de référence)
            cmd = [
                wkhtmltopdf_path,
                #'--page-size', 'A4',
                # '--margin-top', '5mm',
                # '--margin-right', '5mm', 
                # '--margin-bottom', '5mm',
                # '--margin-left', '5mm',
                '--encoding', 'UTF-8',
                '--enable-local-file-access',
                # '--disable-smart-shrinking',
                # '--zoom', '1.0',
                '--dpi', '300',
                '--image-dpi', '300',
                '--javascript-delay', '1000',
                '--no-stop-slow-scripts',
                #'--disable-javascript',
                '--print-media-type',
                '--no-outline',
                '--quiet',
                
                temp_html_path,
                output_path
            ]
        else:
            # Paramètres pour Windows (du code de référence)
            cmd = [
                wkhtmltopdf_path,
                # '--page-size', 'A4',
                # '--margin-top', '5mm',
                # '--margin-right', '5mm', 
                # '--margin-bottom', '5mm',
                # '--margin-left', '5mm',
                # '--encoding', 'UTF-8',
                # '--enable-local-file-access',
                # '--disable-smart-shrinking',
                # '--zoom', '0.95',
                # '--dpi', '300',
                # '--image-dpi', '300',
                # '--image-quality', '100',
                # '--print-media-type',
                '--no-outline',
                #temp_html_path,
                output_path
            ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            logger.info(f"PDF généré avec wkhtmltopdf: {output_path}")
        else:
            logger.error(f"Erreur wkhtmltopdf: {result.stderr}")
            raise Exception(f"Erreur wkhtmltopdf: {result.stderr}")
        
    except Exception as e:
        logger.error(f"Erreur génération PDF: {str(e)}")
        raise e
        
    finally:
        # Nettoyer le fichier temporaire
        if temp_html_path and os.path.exists(temp_html_path):
            os.remove(temp_html_path)

class ProformaGenerator:
    """Générateur de proforma PDF utilisant UNIQUEMENT wkhtmltopdf comme le code de référence"""
    
    def __init__(self):
        pass
    
    def generate_proforma(
        self, 
        client_data: Dict[str, Any], 
        services_data: List[Dict[str, Any]], 
        logement_data: Dict[str, Any],
        organisation_data: Dict[str, Any],
        numero_proforma: str = None
    ) -> str:
        """
        Génère une proforma PDF professionnelle - EXACTEMENT comme le code de référence
        
        Args:
            client_data: Données du client  
            services_data: Liste des services sélectionnés
            logement_data: Données du logement
            organisation_data: Données de l'organisation
            numero_proforma: Numéro de la proforma (généré automatiquement si None)
        
        Returns:
            str: Chemin vers le fichier PDF généré
        """
        try:
            # Génération du numéro de proforma si non fourni
            if not numero_proforma:
                numero_proforma = f"PRF-{datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}"
            
            # Création du fichier permanent dans /tmp avec nom significatif
            pdf_filename = f"proforma_{numero_proforma}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            output_path = os.path.join(tempfile.gettempdir(), pdf_filename)
            
            # Préparation des données pour le template
            proforma_data = self._prepare_template_data(
                client_data, services_data, logement_data, organisation_data, numero_proforma
            )
            
            # Génération du PDF avec wkhtmltopdf UNIQUEMENT
            generate_pdf_from_html(proforma_data, output_path)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la proforma: {str(e)}")
            raise e
    
    def _prepare_template_data(
        self, 
        client_data: Dict, 
        services_data: List[Dict], 
        logement_data: Dict, 
        organisation_data: Dict,
        numero_proforma: str
    ) -> Dict:
        """Prépare les données pour le template HTML"""
        
        # Calcul des totaux
        total_services = sum(service.get('tarif', 0) for service in services_data)
        total_ht = total_services
        total_ttc = total_ht
        
        # Préparation des items pour le tableau
        items = []
        for service in services_data:
            items.append({
                'description': service.get('nom', ''),
                'quantity': 1,
                'unit_price': service.get('tarif', 0),
                'amount': service.get('tarif', 0)
            })
        
        # Banques par défaut comme dans le code de référence
        default_banks = [
            {
                "bank_name": "SOCIETE GENERALE CAMEROUN",
                "iban": "CM21 1000 3001 0006 0110 7319 526"
            },
            {
                "bank_name": "BANQUE ATLANTIQUE", 
                "swift_code": "ATCRCMCM",
                "account_number": "00012750501"
            }
        ]

        # Préparation du customer exactement comme dans le code de référence
        customer_data = {
            'name': f"{client_data.get('prenom_client', '')} {client_data.get('nom_client', '')}".strip(),
            'address': f"{logement_data.get('adresse', '')}, {logement_data.get('ville', '')}" if logement_data else '',
            'email': client_data.get('email_client', '')
        }

        # Données du template exactement comme le code de référence
        template_data = {
            'customer': customer_data,
            'items': items,
            'banks': default_banks,
            'date': datetime.now().strftime('%d/%m/%Y'),
            'invoice_number': numero_proforma,
            'total_ht': total_ht,
            'total_ttc': total_ttc,
            'notes': "RECOMMANDEZ-NOUS ET RECEVEZ 25000 FCFA",
            'terms': ''
        }
        
        return template_data