import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { useAuth } from '../AuthContext';

const PhysiciansPage = () => {
  const [physicians, setPhysicians] = useState([]);
  const { userToken } = useAuth();

  useEffect(() => {
    const fetchPhysiciansList = async () => {
      try {
        const token = userToken;
        const config = {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        };
        const response = await axios.get(`http://127.0.0.1:8000/api/medical_office/physicians`, config);
        console.log(response.data);
        setPhysicians(response.data.doctors);
      } catch (error) {
        console.error('Error fetching physicians list:', error);
      }
    };

    fetchPhysiciansList();
  }, []);

  return (
    <div>
      <h2>Lista de Medici</h2>
      <ul>
        {(() => {
          const physiciansElements = [];
          for (let i = 0; i < physicians.length; i++) {
            const physician = physicians[i];
            physiciansElements.push(
              <li key={physician.id_doctor}>
                Id: {physician.id_doctor}, Nume: {physician.nume}, Prenume: {physician.prenume}, Email: {physician.email}, Telefon: {physician.telefon} Specializare: {physician.specializare}
              </li>
            );
          }
          return physiciansElements;
        })()}
      </ul>
      <Link to="/">Pagina principala</Link><br/>
    </div>
  );
};

export default PhysiciansPage;