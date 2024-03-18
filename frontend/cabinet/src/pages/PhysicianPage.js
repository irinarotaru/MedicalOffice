import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../AuthContext';
import { Link } from 'react-router-dom';

const PhysicianPage = () => {
  const [physicianData, setPhysician] = useState({});
  const { isAuthenticated, userRole, userToken, userId } = useAuth();
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
  }, [isAuthenticated, userRole, userId]);

  useEffect(() => {
    const fetchPhysicianData = async () => {
      try {
        const token = userToken;
        const config = {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        };
        console.log(id_doctor);
        const response = await axios.get(`http://127.0.0.1:8000/api/medical_office/physicians/${id_doctor}`, config);
        console.log(response.data);
        setPhysician(response.data);
      } catch (error) {
        console.error('Error fetching doctor data:', error);
      }
    };

    fetchPhysicianData();
  }, [id_doctor]);

  return (
    <div>
      <h2>Profilul Doctorului</h2>
      {Object.keys(physicianData).length > 0? (
        <>
          <p>Id: {physicianData.doctor.id_doctor}</p>
          <p>Nume: {physicianData.doctor.nume}</p>
          <p>Prenume: {physicianData.doctor.prenume}</p>
          <p>Email: {physicianData.doctor.email}</p>
          <p>Telefon: {physicianData.doctor.telefon}</p>
          <p>Data Nasterii: {physicianData.doctor.specializare}</p>
        </>
      ) : (
        <p>Loading...</p>
      )}
       <Link to="/">Pagina principala</Link><br/>
    </div>
  );
};

export default PhysicianPage;