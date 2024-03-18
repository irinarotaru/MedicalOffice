import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../AuthContext';
import { Link } from 'react-router-dom';

const AppointmentsDPage = () => {
  const [appointments, setAppointments] = useState([]);
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
        const response = await axios.get(`http://127.0.0.1:8000/api/medical_office/physicians/${id_doctor}/appointments`, config);
        console.log(response.data);
        setAppointments(response.data.appointments);
      } catch (error) {
        console.error('Error fetching appointments list:', error);
      }
    };

    fetchPhysiciansList();
  }, [id_doctor, userToken]);

  const updateAppointmentStatus = async (id_pacient,id_doctor,data, newStatus) => {
    try {
      const token = userToken;
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      const response = await axios.patch(
        `http://127.0.0.1:8000/api/medical_office/physicians/${id_doctor}/appointment/${id_pacient}/${data}`,
        {status: newStatus},
        config
      );
      console.log(response.data);

    } catch (error) {
      console.error('Error updating appointment status:', error);
    }
  };


  return (
    <div>
      <h2>Lista de Programari</h2>
      <ul>
        {(() => {
          const appointmentElements = [];
          for (let i = 0; i < appointments.length; i++) {
            const appointment = appointments[i];
            appointmentElements.push(
              <li key={appointment.id_doctor}>
                Pacientului: {appointment.id_pacient}, Data: {appointment.data}, Status: {appointment.status}<br/>
                <button onClick={() => updateAppointmentStatus(appointment.id_pacient,appointment.id_doctor,appointment.data, "onorata")}>Onorată</button>
                <button onClick={() => updateAppointmentStatus(appointment.id_pacient,appointment.id_doctor,appointment.data, "neprezentat")}>Neprezentat</button>
                <button onClick={() => updateAppointmentStatus(appointment.id_pacient,appointment.id_doctor,appointment.data, "anulata")}>Anulată</button> 
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

export default AppointmentsDPage;