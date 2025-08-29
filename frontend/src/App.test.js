import { render, screen } from '@testing-library/react';
import App from './App';

// Mock the LogementsPage component to avoid complex dependencies
jest.mock('./pages/LogementsPage', () => {
  return function MockLogementsPage() {
    return <div>Gestion des logements</div>;
  };
});

test('renders application with logements page', () => {
  render(<App />);
  const logementElement = screen.getByText(/Gestion des logements/i);
  expect(logementElement).toBeInTheDocument();
});
