import api from './api';

const PROFORMA_BASE_URL = '/souscriptions';

export const generateProforma = async (clientData, serviceIds, logementData) => {
  try {
    const proformaData = {
      client_data: clientData,
      service_ids: serviceIds,
      logement_data: logementData
    };
    
    const response = await api.post(`${PROFORMA_BASE_URL}/generate-proforma`, proformaData, {
      responseType: 'blob', // Important pour recevoir le PDF
      headers: {
        'Accept': 'application/pdf',
        'Content-Type': 'application/json'
      }
    });
    
    // Créer un blob URL pour le PDF
    const pdfBlob = new Blob([response.data], { type: 'application/pdf' });
    const pdfUrl = window.URL.createObjectURL(pdfBlob);
    
    return {
      success: true,
      pdfUrl: pdfUrl,
      pdfBlob: pdfBlob,
      filename: `proforma_${clientData.nom || 'client'}.pdf`
    };
    
  } catch (error) {
    console.error('Erreur lors de la génération de la proforma:', error);
    
    let errorMessage = 'Erreur lors de la génération de la proforma';
    
    if (error.response) {
      // Si l'erreur contient du JSON dans un blob
      if (error.response.data instanceof Blob) {
        try {
          const errorText = await error.response.data.text();
          const errorData = JSON.parse(errorText);
          errorMessage = errorData.detail || errorMessage;
        } catch {
          errorMessage = 'Erreur serveur lors de la génération';
        }
      } else if (error.response.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response.status === 500) {
        errorMessage = 'Erreur interne du serveur';
      } else if (error.response.status === 400) {
        errorMessage = 'Données invalides pour la génération';
      }
    } else if (error.request) {
      errorMessage = 'Impossible de contacter le serveur';
    }
    
    return {
      success: false,
      error: errorMessage
    };
  }
};

export const downloadPdf = (pdfBlob, filename) => {
  try {
    const url = window.URL.createObjectURL(pdfBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Erreur lors du téléchargement:', error);
    throw new Error('Erreur lors du téléchargement du fichier');
  }
};

export const previewPdf = (pdfUrl) => {
  try {
    window.open(pdfUrl, '_blank');
  } catch (error) {
    console.error('Erreur lors de l\'ouverture de la prévisualisation:', error);
    throw new Error('Erreur lors de l\'ouverture de la prévisualisation');
  }
};

export const previewAttestation = async (souscriptionId) => {
  try {
    const response = await api.post(`${PROFORMA_BASE_URL}/${souscriptionId}/generate-attestation`, {}, {
      responseType: 'blob', // Important pour recevoir le PDF
      headers: {
        'Accept': 'application/pdf'
      }
    });
    
    // Créer un blob URL pour le PDF
    const pdfBlob = new Blob([response.data], { type: 'application/pdf' });
    const pdfUrl = window.URL.createObjectURL(pdfBlob);
    
    return {
      success: true,
      pdfUrl: pdfUrl,
      pdfBlob: pdfBlob,
      filename: `attestation_preview_${souscriptionId}.pdf`
    };
    
  } catch (error) {
    console.error('Erreur lors de la génération de l\'attestation:', error);
    
    let errorMessage = 'Erreur lors de la génération de l\'attestation';
    
    if (error.response) {
      // Si l'erreur contient du JSON dans un blob
      if (error.response.data instanceof Blob) {
        try {
          const errorText = await error.response.data.text();
          const errorData = JSON.parse(errorText);
          errorMessage = errorData.detail || errorMessage;
        } catch {
          errorMessage = 'Erreur serveur lors de la génération';
        }
      } else if (error.response.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response.status === 400) {
        errorMessage = 'Souscription non éligible pour l\'attestation';
      } else if (error.response.status === 404) {
        errorMessage = 'Souscription non trouvée';
      } else if (error.response.status === 500) {
        errorMessage = 'Erreur interne du serveur';
      }
    } else if (error.request) {
      errorMessage = 'Impossible de contacter le serveur';
    }
    
    return {
      success: false,
      error: errorMessage
    };
  }
};