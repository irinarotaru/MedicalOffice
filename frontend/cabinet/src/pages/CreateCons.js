import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import { useNavigate } from 'react-router-dom';

const CreateConsPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated, userRole, userToken, userId } = useAuth();
  const [id_doctor, setID] = useState(0);
  const [formData, setFormData] = useState({
    id_pacient: '',
    id_doctor: 0,
    data: '',
    diagnostic: '',
    investigatii: [
      {
        id: 0,
        denumire: '',
        durata_de_procesare: 0,
        rezultat: ''
      }
    ]
  });
  useEffect(() => {
    if (isAuthenticated && userRole === 'doctor') {
      const getId = async () => {
        try {
          const response = await axios.get(`http://127.0.0.1:8003/get_id_doctor/${userId}`);
          console.log(response.data.id_doctor);
          setID(response.data.id_doctor);
          console.log(id_doctor);
          setFormData((prevFormData) => ({
            ...prevFormData,
            id_doctor: response.data.id_doctor,
          }));
        } catch (error) {
          console.error('Eroare în obținerea id-ului:', error);
        }
      };
      getId();
    }
  }, [isAuthenticated, userRole, userId,id_doctor]);

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: name === 'id_doctor' ? parseInt(value, 10) : value
    });
  };

  const handleInvestigationChange = (event, index) => {
    const { name, value } = event.target;
    const newInvestigations = [...formData.investigatii];
    newInvestigations[index] = {
      ...newInvestigations[index],
      [name]: name === 'id' || name === 'durata_de_procesare' ? parseInt(value, 10) : value
    };
    setFormData({
      ...formData,
      investigatii: newInvestigations
    });
  };

  const handleAddInvestigation = () => {
    const newId = formData.investigatii.length + 1;
    setFormData({
      ...formData,
      investigatii: [...formData.investigatii, {
        id: newId,
        denumire: '',
        durata_de_procesare: '',
        rezultat: ''
      }]
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = userToken;
    try {
      const response = await axios.post(
        'http://127.0.0.1:8001/api/medical_office/consult',
        formData,
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          withCredentials: true,
        }
      );
      console.log(response.data);
      navigate('/');
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h2>Datele consultației</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>ID Pacient:</label>
          <input
            type="text"
            name="id_pacient"
            value={formData.id_pacient}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label>ID Doctor:</label>
          <input
            type="number"
            name="id_doctor"
            value={id_doctor}
            readOnly
          />
        </div>
        <div>
          <label>Data:</label>
          <input
            type="text"
            name="data"
            value={formData.data}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label>Diagnostic:</label>
          <input
            type="text"
            name="diagnostic"
            value={formData.diagnostic}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label>Investigații:</label>
          <ul>
            {formData.investigatii.map((investigation, index) => (
              <li key={index}>
                <label>
                  Denumire:
                  <input
                    type="text"
                    name="denumire"
                    value={investigation.denumire}
                    onChange={(e) => handleInvestigationChange(e, index)}
                  />
                </label>
                <label>
                  Durata de procesare:
                  <input
                    type="number"
                    name="durata_de_procesare"
                    value={investigation.durata_de_procesare}
                    onChange={(e) => handleInvestigationChange(e, index)}
                  />
                </label>
                <label>
                  Rezultat:
                  <input
                    type="text"
                    name="rezultat"
                    value={investigation.rezultat}
                    onChange={(e) => handleInvestigationChange(e, index)}
                  />
                </label>
              </li>
            ))}
          </ul>
          <button type="button" onClick={handleAddInvestigation}>
            Adaugă Investigatie
          </button>
        </div>
        <button type="submit">Submit</button>
      </form>
      <Link to="/">Pagina principala</Link>
    </div>
  );
};

export default CreateConsPage;