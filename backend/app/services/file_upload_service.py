import os
import uuid
from pathlib import Path
from typing import Optional, Tuple
from fastapi import HTTPException, UploadFile
from PIL import Image
import io


class FileUploadService:
    """Service pour l'upload et la conversion de fichiers de preuves de paiement"""
    
    UPLOAD_DIR = "/app/app/uploads/preuves_paiement"
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
    ALLOWED_PDF_EXTENSIONS = {".pdf"}
    ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_PDF_EXTENSIONS
    
    def __init__(self):
        """Initialiser le service et créer le répertoire de stockage"""
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
    
    def validate_file(self, file: UploadFile) -> None:
        """Valider le fichier uploadé"""
        # Vérifier la taille du fichier
        if file.size and file.size > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Fichier trop volumineux. Taille maximale autorisée: {self.MAX_FILE_SIZE // (1024*1024)} MB"
            )
        
        # Vérifier l'extension
        if file.filename:
            file_extension = Path(file.filename).suffix.lower()
            if file_extension not in self.ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Type de fichier non autorisé. Extensions autorisées: {', '.join(self.ALLOWED_EXTENSIONS)}"
                )
        else:
            raise HTTPException(status_code=400, detail="Nom de fichier manquant")
    
    def generate_unique_filename(self, original_filename: str, force_pdf: bool = False) -> str:
        """Générer un nom de fichier unique"""
        file_extension = Path(original_filename).suffix.lower()
        
        # Si on force la conversion en PDF ou si c'est une image, utiliser .pdf
        if force_pdf or file_extension in self.ALLOWED_IMAGE_EXTENSIONS:
            file_extension = ".pdf"
        
        # Générer un nom unique
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{file_extension}"
    
    def convert_image_to_pdf(self, image_bytes: bytes) -> bytes:
        """Convertir une image en PDF"""
        try:
            # Ouvrir l'image avec Pillow
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convertir en RGB si nécessaire (pour PNG avec transparence, etc.)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Créer un buffer pour le PDF
            pdf_buffer = io.BytesIO()
            
            # Sauvegarder en PDF
            image.save(pdf_buffer, format='PDF', quality=85, optimize=True)
            
            return pdf_buffer.getvalue()
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la conversion image vers PDF: {str(e)}"
            )
    
    async def save_file(self, file: UploadFile, convert_to_pdf: bool = True) -> Tuple[str, str]:
        """
        Sauvegarder le fichier uploadé
        
        Returns:
            Tuple[str, str]: (chemin_relatif, chemin_absolu)
        """
        # Valider le fichier
        self.validate_file(file)
        
        # Lire le contenu du fichier
        file_content = await file.read()
        
        # Vérifier la taille après lecture
        if len(file_content) > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Fichier trop volumineux. Taille maximale autorisée: {self.MAX_FILE_SIZE // (1024*1024)} MB"
            )
        
        # Détecter si c'est une image
        file_extension = Path(file.filename).suffix.lower()
        is_image = file_extension in self.ALLOWED_IMAGE_EXTENSIONS
        
        # Générer le nom de fichier
        if convert_to_pdf and is_image:
            filename = self.generate_unique_filename(file.filename, force_pdf=True)
            # Convertir l'image en PDF
            file_content = self.convert_image_to_pdf(file_content)
        else:
            filename = self.generate_unique_filename(file.filename)
        
        # Chemin complet du fichier
        file_path = os.path.join(self.UPLOAD_DIR, filename)
        
        # Sauvegarder le fichier
        try:
            with open(file_path, "wb") as f:
                f.write(file_content)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erreur lors de la sauvegarde: {str(e)}"
            )
        
        # Retourner les chemins relatif et absolu
        relative_path = f"uploads/preuves_paiement/{filename}"
        return relative_path, file_path
    
    def delete_file(self, relative_path: str) -> bool:
        """Supprimer un fichier"""
        try:
            # Construire le chemin complet à partir du chemin relatif
            if relative_path.startswith("uploads/preuves_paiement/"):
                filename = relative_path.replace("uploads/preuves_paiement/", "")
                file_path = os.path.join(self.UPLOAD_DIR, filename)
                
                if os.path.exists(file_path):
                    os.remove(file_path)
                    return True
            return False
        except Exception:
            return False
    
    def file_exists(self, relative_path: str) -> bool:
        """Vérifier si un fichier existe"""
        try:
            if relative_path.startswith("uploads/preuves_paiement/"):
                filename = relative_path.replace("uploads/preuves_paiement/", "")
                file_path = os.path.join(self.UPLOAD_DIR, filename)
                return os.path.exists(file_path)
            return False
        except Exception:
            return False
    
    def get_file_info(self, relative_path: str) -> Optional[dict]:
        """Récupérer les informations d'un fichier"""
        try:
            if relative_path.startswith("uploads/preuves_paiement/"):
                filename = relative_path.replace("uploads/preuves_paiement/", "")
                file_path = os.path.join(self.UPLOAD_DIR, filename)
                
                if os.path.exists(file_path):
                    stat = os.stat(file_path)
                    return {
                        "filename": filename,
                        "size": stat.st_size,
                        "created_at": stat.st_ctime,
                        "modified_at": stat.st_mtime,
                        "path": file_path
                    }
            return None
        except Exception:
            return None


# Instance globale
file_upload_service = FileUploadService()