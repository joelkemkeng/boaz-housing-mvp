from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import os
import uuid
from datetime import datetime
import logging
from jinja2 import Template
import subprocess
import platform

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Générateur de Facture Proforma", version="1.0.0")

# Servir les fichiers statiques (PDFs générés)
os.makedirs("static/pdfs", exist_ok=True)
os.makedirs("static/assets", exist_ok=True)
os.makedirs("templates", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Modèles Pydantic
class InvoiceItem(BaseModel):
    description: str
    quantity: int = 1
    unit_price: float
    amount: float

class CustomerInfo(BaseModel):
    name: str
    address: str
    email: EmailStr

class BankInfo(BaseModel):
    bank_name: str
    iban: Optional[str] = None
    swift_code: Optional[str] = None
    account_number: Optional[str] = None

class InvoiceData(BaseModel):
    customer: CustomerInfo
    items: List[InvoiceItem]
    date: Optional[str] = None
    invoice_number: Optional[str] = None
    banks: List[BankInfo] = []
    total_ht: Optional[float] = None
    total_ttc: Optional[float] = None
    notes: Optional[str] = "RECOMMANDEZ-NOUS ET RECEVEZ 25000 FCFA"
    terms: Optional[str] = None

def calculate_totals(items: List[InvoiceItem]):
    """Calcule les totaux HT et TTC"""
    total_ht = sum(item.amount for item in items)
    total_ttc = total_ht
    return total_ht, total_ttc

def format_currency(amount: float) -> str:
    """Formate les montants avec des espaces comme séparateurs de milliers"""
    return f"{amount:,.0f}".replace(",", " ")

def get_html_template():
    """Retourne le template HTML optimisé pour une page A4"""
    return """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facture Proforma - Format A4</title>
    <style>

        * {
            box-sizing: border-box;
        }

        body {
            font-family: Arial, 'DejaVu Sans', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
            color: #2c3e50;
            font-size: 11px;
            line-height: 1.4;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
            padding: 10mm 0;
            position: relative;
        }

        .invoice-container {
            width: 210mm;
            max-width: 210mm;
            margin: 0;
            padding: 15mm 15mm 80px 15mm;
            background-color: #ffffff;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0, 63, 255, 0.1);
            position: relative;
            min-height: calc(297mm - 20mm);
        }

        .invoice-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-top: 3px solid #003FFF;
            padding: 20px 0;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #ecf0f1 0%, #ffffff 100%);
            border-radius: 4px;
            min-height: 120px;
        }
        
        .company-details {
            flex: 1;
            padding-left: 15mm;
        }
        
        .company-details p {
            margin: 3px 0;
            font-size: 11px;
            line-height: 1.3;
            color: #34495e;
        }

        .company-details p:first-child {
            font-weight: bold;
            font-size: 13px;
            color: #2c3e50;
            margin-bottom: 8px;
        }

        .logo {
            max-width: 160px;
            height: auto;
            margin-bottom: 10px;
            margin-top: 5px;
        }
        
        .invoice-title-section {
            text-align: right;
            flex-shrink: 0;
            padding-right: 15mm;
        }

        .invoice-title {
            font-size: 26px;
            font-weight: bold;
            color: #003FFF;
            margin: 10px 0 10px 0;
            line-height: 1.1;
            text-shadow: 1px 1px 2px rgba(0, 63, 255, 0.1);
        }
        
        .invoice-title-section p {
            margin: 4px 0;
            font-size: 12px;
            color: #34495e;
            font-weight: 500;
        }
        
        .details-section {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
            gap: 15px;
        }

        .billing-info, .customer-info {
            flex-basis: 48%;
        }

        .billing-info p, .customer-info p {
            margin: 4px 0;
            font-size: 11px;
            line-height: 1.3;
            color: #34495e;
        }

        .billing-info strong.block-title, .customer-info strong.block-title {
            font-size: 13px;
            display: block;
            margin-bottom: 10px;
            border-bottom: 2px solid #003FFF;
            padding-bottom: 5px;
            color: #2c3e50;
            font-weight: 600;
        }
        
        .orange-separator {
            border: 0;
            height: 4px;
            background: linear-gradient(90deg, #F88206 0%, #FF9500 50%, #F88206 100%);
            margin: 15px 0 20px 0;
            border-radius: 2px;
        }

        .invoice-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
            flex-shrink: 0;
        }

        .invoice-table th, .invoice-table td {
            padding: 15px 18px;
            text-align: left;
            border-bottom: 1px solid #ecf0f1;
            font-size: 18px;
            line-height: 1.4;
            font-weight: 600;
        }

        .invoice-table thead th {
            background: linear-gradient(135deg, #003FFF 0%, #0033CC 100%);
            font-weight: 600;
            color: #ffffff;
            font-size: 12px;
            padding: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .text-right { text-align: right; }
        .text-center { text-align: center; }

        .totals-and-footer {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-top: 10px;
            flex: 1;
        }

        .notes-section {
            flex-basis: 55%;
            padding-right: 10px;
        }
        
        .totals-section {
            flex-basis: 45%;
        }

        .totals-table {
            width: 100%;
            margin-bottom: 10px;
        }

        .totals-table td {
            padding: 10px 15px;
            font-size: 12px;
            border-bottom: 1px solid #ecf0f1;
            color: #34495e;
        }
        
        .totals-table tr.total-ttc td {
            font-weight: 700;
            font-size: 14px;
            background: linear-gradient(135deg, #F88206 0%, #FF9500 100%);
            color: #ffffff;
            border-top: 3px solid #E6740A;
            padding: 12px 15px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        
        .ps-note {
            font-weight: 600;
            color: #F88206;
            text-align: center;
            padding: 12px;
            border: 2px dashed #F88206;
            background-color: rgba(248, 130, 6, 0.05);
            border-radius: 4px;
            margin-bottom: 15px;
            font-size: 12px;
            line-height: 1.3;
        }
        
        .terms {
            font-size: 9px;
            color: #7f8c8d;
            text-align: justify;
            line-height: 1.3;
            padding: 15px;
            background-color: #f8f9fa;
            border-top: 3px solid #003FFF;
            border-radius: 4px;
            margin-top: 30px;
            width: 100%;
        }
        
        .footer-terms {
            position: absolute;
            bottom: 0;
            left: 15mm;
            right: 15mm;
            background-color: #f8f9fa;
            border-top: 3px solid #003FFF;
            padding: 15px;
            font-size: 8px;
            color: #7f8c8d;
            text-align: justify;
            line-height: 1.2;
            margin: 0;
            z-index: 10;
        }

        .signature-section {
            text-align: right;
            margin-top: 15px;
            padding-right: 50px;
        }
        
        .signature-box {
            display: inline-block;
            text-align: center;
            padding-top: 8px;
            border-top: 1px solid #ccc;
            width: 200px;
            position: relative;
        }
        
        .signature-box p {
             margin: 0 0 5px 0;
             font-size: 8px;
             font-weight: bold;
        }

        .stamp-image {
            max-width: 200px;
            height: auto;
            transform: rotate(-8deg);
            transform-origin: center center;
            margin: 5px 0;
        }

        @media print, screen {
            body { 
                background-color: white; 
                padding: 5mm;
                font-size: 8px;
            }
            .invoice-container {
                box-shadow: none;
                border: 1px solid #ddd;
                margin: 0;
                padding: 10px;
                height: calc(100vh - 10mm);
            }
            
            .invoice-table th, .invoice-table td {
                padding: 4px 6px;
                font-size: 10px;
            }
            
            .invoice-table thead th {
                padding: 5px 6px;
                font-size: 8px;
            }
        }
    </style>
</head>
<body>

    <div class="invoice-container">

        <header class="invoice-header">
            <div class="company-details">
                <img src="static/assets/logo.jpeg" alt="Logo de l'entreprise" class="logo">
                <p><strong>Boaz Study Cameroun SAS</strong></p>
                <p>Yaoundé Total Ecole de Police - Tel: (+237) 658 870 473</p>
                <p>389 Rue Toyota Bonapriso, B.P: 1230 Douala - Tel: (+237) 694 186 936</p>
                <p>Email: info@boaz-study.com | Web: www.boaz-study.com</p>
            </div>
            <div class="invoice-title-section">
                <h1 class="invoice-title">FACTURE</h1>
                <p>Date : {{ date }}</p>
                {% if invoice_number %}
                <p>N° : {{ invoice_number }}</p>
                {% endif %}
            </div>
        </header>

        <section class="details-section">
            <div class="billing-info">
                <strong class="block-title">Coordonnées Bancaires</strong>
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
                <hr style="border:0; border-top:1px solid #eee; margin:10px 0;">
                {% endif %}
                {% endfor %}
            </div>
            <div class="customer-info">
                <strong class="block-title">Facturé à</strong>
                <p><strong>{{ customer.name }}</strong></p>
                <p>Adresse: {{ customer.address }}</p>
                <p>Mail: {{ customer.email }}</p>
            </div>
        </section>

        <hr class="orange-separator">

        <table class="invoice-table">
            <thead>
                <tr>
                    <th>Description</th>
                    <th class="text-center">Qté</th>
                    <th class="text-right">Prix unitaire</th>
                    <th class="text-right">Montant</th>
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

        <div class="totals-and-footer">
            <div class="notes-section">
                {% if notes %}
                <p class="ps-note">{{ notes }}</p>
                {% endif %}
            </div>
            <div class="totals-section">
                <table class="totals-table">
                    <tbody>
                        <tr>
                            <td>Total HT</td>
                            <td class="text-right">{{ format_currency(total_ht) }} FCFA</td>
                        </tr>
                        <tr class="total-ttc">
                            <td><strong>Total TTC</strong></td>
                            <td class="text-right"><strong>{{ format_currency(total_ttc) }} FCFA</strong></td>
                        </tr>
                    </tbody>
                </table>
                <div class="signature-section">
                   <div class="signature-box">
                        <p>Boaz-Housing {{ date }}</p>
                        <img src="static/assets/cachet-bs-rouge-rectangle.jpeg" alt="Cachet et Signature" class="stamp-image">
                   </div>
                </div>
            </div>
        </div>

    </div>

    <footer class="footer-terms">
        {% if terms %}
        <strong>Terms and conditions:</strong> {{ terms }}
        {% else %}
        <strong>Terms and conditions:</strong> This invoice will be payable no later than 30 days after receipt. Past due amounts are subject to a late fee of 10% per month, or the maximum amount permitted by law. In accordance with article L441-6 of the Commercial Code, a penalty will be applied calculated at an annual rate of 15%. A lump sum recovery indemnity of 40 Euros will also be payable.
        {% endif %}
    </footer>

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
        result = subprocess.run(['wkhtmltopdf', 
                                 '--version',
                                 '--enable-local-file-access',
                                 '--disable-smart-shrinking',
                                 '--zoom', '1.0',
                                 '--dpi', '300',
                                 '--image-quality', '100',
                                 '--page-size', 'A4',
                                 '--margin-top', '5mm',
                                 '--margin-right', '5mm', 
                                 '--margin-bottom', '5mm',
                                 '--margin-left', '5mm',
                                 '--encoding', 'UTF-8',
                                 '--print-media-type',
                                 '--no-outline',
                                 '--quiet'                   
                                 ], 
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

def generate_pdf_from_html(invoice_data: dict, output_path: str):
    """Génère un PDF à partir du template HTML exact"""
    try:
        # Créer le template Jinja2
        template = Template(get_html_template())
        
        # Fonction helper pour le formatage des devises
        def currency_filter(value):
            return format_currency(value)
        
        # Rendu du template avec les données
        html_content = template.render(
            customer=invoice_data.get('customer', {}),
            items=invoice_data.get('items', []),
            banks=invoice_data.get('banks', []),
            date=invoice_data.get('date', ''),
            invoice_number=invoice_data.get('invoice_number', ''),
            total_ht=invoice_data.get('total_ht', 0),
            total_ttc=invoice_data.get('total_ttc', 0),
            notes=invoice_data.get('notes', ''),
            terms=invoice_data.get('terms', ''),
            format_currency=currency_filter
        )
        
        # Sauvegarder le HTML temporaire
        temp_html_path = f"temp_invoice_{uuid.uuid4()}.html"
        with open(temp_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Essayer wkhtmltopdf d'abord
        wkhtmltopdf_path = find_wkhtmltopdf()
        
        if wkhtmltopdf_path:
            # Utiliser wkhtmltopdf
            # Détecter si on est sur Ubuntu/Linux
            is_linux = platform.system().lower() == 'linux'
            
            if is_linux:
                # Paramètres optimisés pour Ubuntu/Linux
                cmd = [
                    wkhtmltopdf_path,
                    '--page-size', 'A4',
                    '--margin-top', '5mm',
                    '--margin-right', '5mm', 
                    '--margin-bottom', '5mm',
                    '--margin-left', '5mm',
                    '--encoding', 'UTF-8',
                    '--enable-local-file-access',
                    '--disable-smart-shrinking',
                    '--zoom', '1.0',
                    '--dpi', '96',
                    '--image-dpi', '96',
                    '--javascript-delay', '1000',
                    '--no-stop-slow-scripts',
                    '--disable-javascript',
                    '--print-media-type',
                    '--no-outline',
                    '--quiet',
                    temp_html_path,
                    output_path
                ]
            else:
                # Paramètres pour Windows
                cmd = [
                    wkhtmltopdf_path,
                    '--page-size', 'A4',
                    '--margin-top', '5mm',
                    '--margin-right', '5mm', 
                    '--margin-bottom', '5mm',
                    '--margin-left', '5mm',
                    '--encoding', 'UTF-8',
                    '--enable-local-file-access',
                    '--disable-smart-shrinking',
                    '--zoom', '0.95',
                    '--dpi', '300',
                    '--image-dpi', '300',
                    '--image-quality', '100',
                    '--print-media-type',
                    '--no-outline',
                    temp_html_path,
                    output_path
                ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                logger.info(f"PDF généré avec wkhtmltopdf: {output_path}")
            else:
                logger.error(f"Erreur wkhtmltopdf: {result.stderr}")
                raise Exception("Erreur wkhtmltopdf")
        
        else:
            # Fallback: essayer weasyprint
            try:
                import weasyprint
                html = weasyprint.HTML(filename=temp_html_path)
                css = weasyprint.CSS(string='@page { size: A4; margin: 1cm; }')
                html.write_pdf(output_path, stylesheets=[css])
                logger.info(f"PDF généré avec WeasyPrint: {output_path}")
            except ImportError:
                logger.error("Ni wkhtmltopdf ni WeasyPrint disponibles")
                # Copier le HTML comme fallback
                html_output = output_path.replace('.pdf', '.html')
                with open(html_output, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                logger.info(f"HTML généré comme fallback: {html_output}")
        
        # Nettoyer le fichier temporaire
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)
            
    except Exception as e:
        logger.error(f"Erreur génération PDF: {str(e)}")
        # Fallback: créer un HTML
        html_output = output_path.replace('.pdf', '.html')
        template = Template(get_html_template())
        html_content = template.render(
            customer=invoice_data.get('customer', {}),
            items=invoice_data.get('items', []),
            banks=invoice_data.get('banks', []),
            date=invoice_data.get('date', ''),
            invoice_number=invoice_data.get('invoice_number', ''),
            total_ht=invoice_data.get('total_ht', 0),
            total_ttc=invoice_data.get('total_ttc', 0),
            notes=invoice_data.get('notes', ''),
            terms=invoice_data.get('terms', ''),
            format_currency=format_currency
        )
        with open(html_output, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info(f"HTML de fallback créé: {html_output}")

@app.get("/")
async def root():
    return {"message": "API Générateur de Facture Proforma", "version": "1.0.0"}

@app.post("/generate-invoice")
async def generate_invoice(invoice_data: InvoiceData):
    """Génère une facture proforma en PDF"""
    try:
        # Générer un ID unique pour la facture
        invoice_id = str(uuid.uuid4())
        
        # Calculer les totaux si non fournis
        if not invoice_data.total_ht or not invoice_data.total_ttc:
            total_ht, total_ttc = calculate_totals(invoice_data.items)
            invoice_data.total_ht = total_ht
            invoice_data.total_ttc = total_ttc
        
        # Générer le numéro de facture si non fourni
        if not invoice_data.invoice_number:
            invoice_data.invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{invoice_id[:8].upper()}"
        
        # Date par défaut
        if not invoice_data.date:
            invoice_data.date = datetime.now().strftime('%d/%m/%Y')
        
        # Banques par défaut si non fournies
        if not invoice_data.banks:
            invoice_data.banks = [
                BankInfo(
                    bank_name="SOCIETE GENERALE CAMEROUN",
                    iban="CM21 1000 3001 0006 0110 7319 526"
                ),
                BankInfo(
                    bank_name="BANQUE ATLANTIQUE",
                    swift_code="ATCRCMCM",
                    account_number="00012750501"
                )
            ]
        
        # Chemin de sortie du PDF
        pdf_filename = f"invoice_{invoice_id}.pdf"
        pdf_path = f"static/pdfs/{pdf_filename}"
        
        # Convertir les données pour la génération PDF
        invoice_dict = invoice_data.dict()
        
        # Génération du PDF avec le template HTML exact
        generate_pdf_from_html(invoice_dict, pdf_path)
        
        # Vérifier le fichier généré
        if os.path.exists(pdf_path):
            pdf_url = f"/static/pdfs/{pdf_filename}"
        else:
            # Chercher un fichier HTML si PDF a échoué
            html_filename = f"invoice_{invoice_id}.html"
            html_path = f"static/pdfs/{html_filename}"
            if os.path.exists(html_path):
                pdf_url = f"/static/pdfs/{html_filename}"
                pdf_filename = html_filename
            else:
                raise Exception("Aucun fichier généré")
        
        return JSONResponse({
            "success": True,
            "message": "Facture générée avec succès",
            "invoice_id": invoice_id,
            "invoice_number": invoice_data.invoice_number,
            "pdf_url": pdf_url,
            "pdf_filename": pdf_filename
        })
        
    except Exception as e:
        logger.error(f"Erreur lors de la génération de la facture: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération de la facture: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Endpoint de vérification de santé"""
    wkhtmltopdf_path = find_wkhtmltopdf()
    
    try:
        import weasyprint
        weasyprint_available = True
    except ImportError:
        weasyprint_available = False
    
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "wkhtmltopdf_available": wkhtmltopdf_path is not None,
        "wkhtmltopdf_path": wkhtmltopdf_path,
        "weasyprint_available": weasyprint_available
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)