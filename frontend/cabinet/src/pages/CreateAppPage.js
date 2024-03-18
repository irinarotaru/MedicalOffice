import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';

const CreateAppPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    id_pacient: '',
    id_doctor: '',
    data: '',
  });
  const { isAuthenticated, userRole, userId, userToken } = useAuth();
  const [cnp, setCnp] = useState('');
  useEffect(() => {
    if (isAuthenticated && userRole === 'pacient') {
      const getCnp = async () => {
        try {
          const response = await axios.get(`http://127.0.0.1:8003/get_cnp/${userId}`);
          setCnp(response.data.cnp);
          setFormData((prevFormData) => ({
            ...prevFormData,
            id_pacient: response.data.cnp,
          }));
          } catch (error) {
          console.error('Eroare în obținerea CNP-ului:', error);
        }
      };
      getCnp();
    }
  }, [isAuthenticated, userRole, userId]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        const token = userToken;
        const config = {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        };  
      const response = await axios.post('http://127.0.0.1:8000/api/medical_office/appointment', formData, config);
      console.log(response.data);
      navigate('/');
    } catch (error) {
      console.error('Eroare la efectuarea cererii:', error);
    }
  };

  return (
    <div>
      <h1>Creare Programare</h1>
      <form onSubmit={handleSubmit}>
      <label>
          CNP:
          <input type="text" name="id_pacient" value={cnp} readOnly/>
        </label>
        <br />

        <label>
          Id-ul doctorului:
          <input type="text" name="id_doctor" value={formData.id_doctor} onChange={handleChange} />
        </label>
        <br />

        <label>
          Data:
          <input type="date" name="data" value={formData.data} onChange={handleChange} />
        </label>
        <br />
        <button type="submit">Creare Programare</button>
      </form>
      <Link to="/">Pagina principala</Link><br/>
    </div>
  );
};

export default CreateAppPage;