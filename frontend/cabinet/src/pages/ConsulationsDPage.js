import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../AuthContext';
import { Link } from 'react-router-dom';

const ConsulationsDPage = () => {
  const [consulations, setConsulations] = useState([]);
  const { isAuthenticated, userRole, userId, userToken } = useAuth();
  const [id_doctor, setID] = useState(0);
  useEffect(() => {
    if (isAuthenticated && userRole === 'doctor') {
      const getId = async () => {
        try {
          const response = await axios.get(`http://127.0.0.1:8003/get_id_doctor/${userId}`);
          console.log(response.data.id_doctor);
          setID(response.data.id_doctor);
          console.log(id_doctor);
        } catch (error) {
          console.error('Eroare în obținerea id-ului:', error);
        }
      };
      getId();
    }
  }, [isAuthenticated, userRole, userId, id_doctor]);
  useEffect(() => {
    const fetchPhysiciansList = async () => {
      try {
        const token = userToken;
        const config = {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        };
        const response = await axios.get(`http://127.0.0.1:8001/api/medical_office/physicians/${id_doctor}/consult`, config);
        console.log(response.data);
        setConsulations(response.data.consultations);
      } catch (error) {
        console.error('Error fetching appointments list:', error);
      }
    };

    fetchPhysiciansList();
  }, [id_doctor, userToken]);

  return (
    <div>
      <h2>Lista de Consulatii</h2>
      <ul>
        {(() => {
          const consulationsElement = [];
          console.log(consulations);
          for (let i = 0; i < consulations.length; i++) {
            const consultation = consulations[i];
            const investigationsElement = [];
            for (let j = 0; j < consultation.investigatii.length; j++) {
                const investigation = consultation.investigatii[j];
                investigationsElement.push(
                  <li key={investigation.id}>
                    Investigatie: {investigation.denumire}, Durata de procesare: {investigation.durata_de_procesare}, Rezultat: {investigation.rezultat}
                  </li>
                );
              }
            consulationsElement.push(
              <li key={consultation.id_doctor}>
                Pacientului: {consultation.id_pacient}, Data: {consultation.data}, Diagnostic: {consultation.diagnostic} , 
                <ul>{investigationsElement}</ul>
                <Link to={`/update_consultation/${consultation.id_pacient}/${consultation.data}`}>Modifică Consultația</Link>
              </li>
            );
          }
          return consulationsElement;
        })()}
      </ul>
      <Link to="/">Pagina principala</Link><br/>
    </div>
  );
};

export default ConsulationsDPage;