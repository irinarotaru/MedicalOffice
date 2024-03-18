import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../AuthContext';
import { Link } from 'react-router-dom';

const ResultsPage = () => {
  const [results, setResults] = useState([]);
  const { isAuthenticated, userRole, userId, userToken } = useAuth();
  const [cnp, setCnp] = useState('');
  useEffect(() => {
    if (isAuthenticated && userRole === 'pacient') {
      const getCnp = async () => {
        try {
          const response = await axios.get(`http://127.0.0.1:8003/get_cnp/${userId}`);
          setCnp(response.data.cnp);
        } catch (error) {
          console.error('Eroare în obținerea CNP-ului:', error);
        }
      };
      getCnp();
    }
  }, [isAuthenticated, userRole, userId]);
  useEffect(() => {
    const ResultsList = async () => {
      try {
        const token = userToken;
        const config = {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        };
        const response = await axios.get(`http://127.0.0.1:8000/api/medical_office/patients/${cnp}/results`, config);
        console.log(response.data.results.investigatii);
        setResults(response.data.results.investigatii);
      } catch (error) {
        console.error('Error fetching results list:', error);
      }
    };

    ResultsList();
  }, [cnp, userToken]);

  return (
    <div>
      <h2>Rezultate anterioare</h2>
      <ul>
      {results.map((investigatie, index) => (
          <li key={index}>
            Denumirea: {investigatie[0].denumire}, Durata de procesare: {investigatie[0].durata_de_procesare}, Rezultat: {investigatie[0].rezultat}
          </li>
        ))}
      </ul>
      <Link to="/">Pagina principala</Link><br/>
    </div>
  );
};

export default ResultsPage;