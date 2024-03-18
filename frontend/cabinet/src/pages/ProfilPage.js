import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../AuthContext';
import { Link } from 'react-router-dom';

const ProfilePage = () => {
  const [patientData, setPatientData] = useState({});
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
    const fetchPatientData = async () => {
      try {
        const token = userToken;
        const config = {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        };
        const response = await axios.get(`http://127.0.0.1:8000/api/medical_office/patients/${cnp}`, config);
        console.log(response.data);
        setPatientData(response.data);
      } catch (error) {
        console.error('Error fetching patient data:', error);
      }
    };

    fetchPatientData();
  }, [cnp]);

  return (
    <div>
      <h2>Profilul Pacientului</h2>
      <p>CNP: {cnp}</p>
      {Object.keys(patientData).length > 0 ? (
        <>
          <p>Nume: {patientData.patient.nume}</p>
          <p>Prenume: {patientData.patient.prenume}</p>
          <p>Email: {patientData.patient.email}</p>
          <p>Telefon: {patientData.patient.telefon}</p>
          <p>Data Nasterii: {patientData.patient.data_nasterii}</p>
          <p>Activ: {patientData.patient.is_active ? 'Da' : 'Nu'}</p>
        </>
      ) : (
        <p>Loading...</p>
      )}
      <Link to="/">Pagina principala</Link><br/>
    </div>
  );
};

export default ProfilePage;