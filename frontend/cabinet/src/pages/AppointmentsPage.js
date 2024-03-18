import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../AuthContext';
import { Link } from 'react-router-dom';

const AppointmentPage = () => {
  const [appointments, setAppointments] = useState([]);
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
    const fetchPhysiciansList = async () => {
      try {
        const token = userToken;
        const config = {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        };
        const response = await axios.get(`http://127.0.0.1:8000/api/medical_office/patients/${cnp}/physicians`, config);
        console.log(response.data);
        setAppointments(response.data.appointments);
      } catch (error) {
        console.error('Error fetching appointments list:', error);
      }
    };

    fetchPhysiciansList();
  }, [cnp, userToken]);

  return (
    <div>
      <h2>Lista de Programari</h2>
      <ul>
        {(() => {
          const appointmentElements = [];
          for (let i = 0; i < appointments.length; i++) {
            const appointment = appointments[i];
            appointmentElements.push(
              <li key={appointment.id_pacient}>
                Doctorul: {appointment.id_doctor}, Data: {appointment.data}, Status: {appointment.status} 
              </li>
            );
          }
          return appointmentElements;
        })()}
      </ul>
      <Link to="/">Pagina principala</Link><br/>
    </div>
  );
};

export default AppointmentPage;