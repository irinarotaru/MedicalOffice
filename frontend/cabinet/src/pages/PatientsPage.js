import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../AuthContext';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

const PatientsPage = () => {
  const [patientsData, setPatients] = useState({});
  const { isAuthenticated, userRole, userToken, userId } = useAuth();
  const [id_doctor, setID] = useState(0);
  const navigate = useNavigate();
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
  }, [isAuthenticated, userRole, userId,id_doctor]);
  useEffect(() => {
    const fetchPatientsData = async () => {
      try {
        const token = userToken;
        const config = {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        };
        console.log(id_doctor);
        const response = await axios.get(`http://127.0.0.1:8000/api/medical_office/physicians/${id_doctor}/patients`, config);
        console.log(response.data.patients);
        setPatients(response.data.patients);
      } catch (error) {
        console.error('Error fetching doctor data:', error);
      }
    };

    fetchPatientsData();
  }, [id_doctor, userToken]);
  const makePatientInactive = async (cnp) => {
    try {
      const token = userToken;
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      const response = await axios.patch(`http://127.0.0.1:8000/api/medical_office/physicians/${id_doctor}/patients/${cnp}`,null, config);
      navigate('/physicians/:id_doctor/see_patients');
      console.log(response.data);
    } catch (error) {
      console.error('Error fetching appointments list:', error);
    }
  };
  return (
    <div>
      <h2>Pacientii dumneavoastra:</h2>
      <ul>
        {(() => {
          const patientsElements = [];
          for (let i = 0; i < patientsData.length; i++) {
            const patient = patientsData[i];
            patientsElements.push(
              <li key={patient.cnp}>
                <p>CNP: {patient.cnp}</p>
                <p>Nume: {patient.nume}</p>
                <p>Prenume: {patient.prenume}</p>
                <p>Email: {patient.email}</p>
                <p>Telefon: {patient.telefon}</p>
                <p>Data Nasterii: {patient.data_nasterii}</p>
                <p>Activ: {patient.is_active ? 'Da' : 'Nu'}</p>
                <button onClick={() => makePatientInactive(patient.cnp)}>Setează ca inactiv</button>
              </li>
            );
          }
          return patientsElements;
        })()}
      </ul>
      <Link to="/">Pagina principala</Link><br/>
    </div>
  );
};

export default PatientsPage;