import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../AuthContext';

const HomePage = () => {
  const { isAuthenticated, userRole, userId, logout } = useAuth();
  return (
    <div>
      <h2>Bine ați venit la cabinetul medical</h2>
      <p>Aici găsiți cele mai bune servicii medicale.</p>
      {isAuthenticated ? (
        <div>
          <p>Utilizatorul este autentificat.</p>
          <button onClick={logout}>Ieșiți din cont</button>
          {userRole === 'pacient' && (
            <div>
              <Link to="/see_physicians">Vezi medicii</Link><br/>
              <Link to="/patients/${userId}">Profilul tau</Link><br/>
              <Link to="/patients/${userId}/physicians">Programarile tale</Link><br/>
              <Link to="/patients/${userID}/results">Istoricul medical propriu</Link><br/>
              <Link to="/patients/${userID}/create_app">Creati o programare</Link>
            </div>
          )}
          {userRole === 'doctor' && (
            <div>
              <Link to="/physicians/${userId}">Profilul tau</Link><br/>
              <Link to="physicians/${userId}/see_patients">Vizualizati pacientii proprii</Link><br/>
              <Link to="/physicians/${userId}/patients">Programarile tale</Link><br/>
              <Link to="/consultations/${userId}">Consultatiile tale</Link><br/>
              <Link to="/create_consult">Creeaza o consulatie</Link><br/>
            </div>
          )}
        </div>
      ) : (
        <div>
        <Link to="/login">
          <button>Intrați în cont</button>
        </Link><br/>
        <Link to="/create_account">
          <button>Creați un cont</button>
        </Link>
        </div>
      )}
    </div>
  );
};

export default HomePage;