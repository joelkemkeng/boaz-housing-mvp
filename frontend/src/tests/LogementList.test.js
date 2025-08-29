import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import LogementList from '../components/LogementList';
import { logementService } from '../services/logementService';

// Mock du service
jest.mock('../services/logementService');
const mockedService = logementService;

// Mock de window.confirm
global.confirm = jest.fn();

describe('LogementList', () => {
  const mockLogements = [
    {
      id: 1,
      adresse: '123 Rue Test',
      ville: 'Paris',
      code_postal: '75001',
      loyer: 500,
      statut: 'disponible',
      created_at: '2025-01-01T00:00:00Z'
    },
    {
      id: 2,
      adresse: '456 Avenue Test',
      ville: 'Lyon',
      code_postal: '69001',
      loyer: 600,
      statut: 'occupe',
      created_at: '2025-01-01T00:00:00Z'
    }
  ];

  const mockProps = {
    onEdit: jest.fn(),
    onView: jest.fn()
  };

  beforeEach(() => {
    jest.clearAllMocks();
    mockedService.getLogements.mockResolvedValue(mockLogements);
    mockedService.deleteLogement.mockResolvedValue({ message: 'Supprimé' });
    mockedService.changeStatutLogement.mockResolvedValue({ message: 'Statut modifié' });
  });

  test('should render logements list', async () => {
    render(<LogementList {...mockProps} />);

    await waitFor(() => {
      expect(screen.getByText('123 Rue Test')).toBeInTheDocument();
      expect(screen.getByText('456 Avenue Test')).toBeInTheDocument();
      expect(screen.getByText('Paris')).toBeInTheDocument();
      expect(screen.getByText('Lyon')).toBeInTheDocument();
    });
  });

  test('should handle filter by status', async () => {
    render(<LogementList {...mockProps} />);

    await waitFor(() => {
      const statusFilter = screen.getByDisplayValue('Tous les statuts');
      fireEvent.change(statusFilter, { target: { value: 'disponible' } });
    });

    expect(mockedService.getLogements).toHaveBeenCalledWith({
      statut: 'disponible',
      ville: '',
      skip: 0,
      limit: 20
    });
  });

  test('should handle filter by ville', async () => {
    render(<LogementList {...mockProps} />);

    await waitFor(() => {
      const villeFilter = screen.getByPlaceholderText('Rechercher une ville...');
      fireEvent.change(villeFilter, { target: { value: 'Paris' } });
    });

    expect(mockedService.getLogements).toHaveBeenCalledWith({
      statut: '',
      ville: 'Paris',
      skip: 0,
      limit: 20
    });
  });

  test('should handle edit button click', async () => {
    render(<LogementList {...mockProps} />);

    await waitFor(() => {
      const editButtons = screen.getAllByText('Modifier');
      fireEvent.click(editButtons[0]);
    });

    expect(mockProps.onEdit).toHaveBeenCalledWith(mockLogements[0]);
  });

  test('should handle view button click', async () => {
    render(<LogementList {...mockProps} />);

    await waitFor(() => {
      const viewButtons = screen.getAllByText('Voir');
      fireEvent.click(viewButtons[0]);
    });

    expect(mockProps.onView).toHaveBeenCalledWith(mockLogements[0]);
  });

  test('should handle delete with confirmation', async () => {
    global.confirm.mockReturnValue(true);
    render(<LogementList {...mockProps} />);

    await waitFor(() => {
      const deleteButtons = screen.getAllByText('Supprimer');
      fireEvent.click(deleteButtons[0]);
    });

    expect(global.confirm).toHaveBeenCalledWith('Êtes-vous sûr de vouloir supprimer ce logement ?');
    expect(mockedService.deleteLogement).toHaveBeenCalledWith(1);
  });

  test('should not delete when confirmation is cancelled', async () => {
    global.confirm.mockReturnValue(false);
    render(<LogementList {...mockProps} />);

    await waitFor(() => {
      const deleteButtons = screen.getAllByText('Supprimer');
      fireEvent.click(deleteButtons[0]);
    });

    expect(global.confirm).toHaveBeenCalled();
    expect(mockedService.deleteLogement).not.toHaveBeenCalled();
  });

  test('should handle status change', async () => {
    render(<LogementList {...mockProps} />);

    await waitFor(() => {
      const statusSelects = screen.getAllByDisplayValue('disponible');
      fireEvent.change(statusSelects[0], { target: { value: 'occupe' } });
    });

    expect(mockedService.changeStatutLogement).toHaveBeenCalledWith(1, 'occupe');
  });

  test('should show loading spinner initially', () => {
    render(<LogementList {...mockProps} />);
    
    expect(screen.getByRole('status')).toBeInTheDocument(); // spinner animation
  });

  test('should show empty state when no logements', async () => {
    mockedService.getLogements.mockResolvedValue([]);
    render(<LogementList {...mockProps} />);

    await waitFor(() => {
      expect(screen.getByText('Aucun logement trouvé')).toBeInTheDocument();
    });
  });

  test('should handle pagination', async () => {
    render(<LogementList {...mockProps} />);

    await waitFor(() => {
      const nextButton = screen.getByText('Suivant');
      fireEvent.click(nextButton);
    });

    expect(mockedService.getLogements).toHaveBeenCalledWith({
      statut: '',
      ville: '',
      skip: 20,
      limit: 20
    });
  });
});