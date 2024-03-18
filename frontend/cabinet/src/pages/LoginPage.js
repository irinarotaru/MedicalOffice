import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import {useAuth} from '../AuthContext';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        'http://127.0.0.1:8002/api/medical_office/login',
        {
          username: username,
          password: password,
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Expose-Headers': 'Access-Token, Uid'
          },
          withCredentials: true
        }
      );
      console.log(response.data);
      if(response.data && response.data.role && response.data.id, response.data.token)
      {
        console.log(response.data.token);
        login(response.data.role, response.data.id, response.data.token);
      }
      navigate('/');
    } catch (error) {
      console.error('Error:', error);
      setMessage('Utilizator sau parola incorecte.')
    }
  };

  return (
    <div>
      <h2>Pagina de login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Utilizator:</label>
          <input
            type="text"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label>Parola:</label>
          <input
            type="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">Login</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default LoginPage;