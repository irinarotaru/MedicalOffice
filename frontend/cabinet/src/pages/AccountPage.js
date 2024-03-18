import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

const AccountPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    cnp: '',
    nume: '',
    prenume: '',
    email: '',
    telefon: '',
    data_nasterii: '',
    username: '',
    password: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.put('http://127.0.0.1:8000/api/medical_office/patient', formData);
      console.log(response.data);
      navigate('/');
    } catch (error) {
      console.error('Eroare la efectuarea cererii:', error);
    }
  };

  return (
    <div>
      <h1>Creare Utilizator</h1>
      <form onSubmit={handleSubmit}>
      <label>
          CNP:
          <input type="text" name="cnp" value={formData.cnp} onChange={handleChange} />
        </label>
        <br />

        <label>
          Nume:
          <input type="text" name="nume" value={formData.nume} onChange={handleChange} />
        </label>
        <br />

        <label>
          Prenume:
          <input type="text" name="prenume" value={formData.prenume} onChange={handleChange} />
        </label>
        <br />

        <label>
          Email:
          <input type="email" name="email" value={formData.email} onChange={handleChange} />
        </label>
        <br />

        <label>
          Telefon:
          <input type="tel" name="telefon" value={formData.telefon} onChange={handleChange} />
        </label>
        <br />

        <label>
          Data Nasterii:
          <input type="date" name="data_nasterii" value={formData.data_nasterii} onChange={handleChange} />
        </label>
        <br />

        <label>
          Username:
          <input type="text" name="username" value={formData.username} onChange={handleChange} />
        </label>
        <br />

        <label>
          Parola:
          <input type="password" name="password" value={formData.parola} onChange={handleChange} />
        </label>
        <br />
        <button type="submit">Creare Utilizator</button>
      </form>
      <Link to="/">Pagina principala</Link><br/>
    </div>
  );
};

export default AccountPage;