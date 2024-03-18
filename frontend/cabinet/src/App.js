import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './AuthContext';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import ProfilePage from './pages/ProfilPage';
import PhysiciansPage from './pages/PhysiciansPage';
import AppointmentPage from './pages/AppointmentsPage';
import PhysicianPage from './pages/PhysicianPage';
import AppointmentsDPage from './pages/AppointmentsDPage';
import ConsulationsDPage from './pages/ConsulationsDPage';
import CreateConsPage from './pages/CreateCons';
import ResultsPage from './pages/ResultsPage';
import PatientsPage from './pages/PatientsPage';
import AccountPage from './pages/AccountPage';
import CreateAppPage from './pages/CreateAppPage';
import UpdateConsulationPage from './pages/UpdateConsPage';

const App = () => {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />}/>
          <Route path='/patients/:cnp' element={<ProfilePage/>}/>
          <Route path='/patients/:cnp/physicians' element={<AppointmentPage/>}/>
          <Route path='/patients/:cnp/create_app' element={<CreateAppPage/>}/>
          <Route path='/see_physicians' element={<PhysiciansPage/>}/>
          <Route path='/physicians/:id_doctor' element={<PhysicianPage/>}/>
          <Route path='/physicians/:id_doctor/patients' element={<AppointmentsDPage/>}/>
          <Route path='/consultations/:id_doctor' element={<ConsulationsDPage/>}/>
          <Route path="/create_consult" element={<CreateConsPage />}/>
          <Route path="/patients/:cnp/results" element={<ResultsPage />}/>
          <Route path='/physicians/:id_doctor/see_patients' element={<PatientsPage/>}/>
          <Route path="/create_account" element={<AccountPage />}/>
          <Route path="update_consultation/:cnp/:data" element={<UpdateConsulationPage/>}/>
        </Routes>
      </AuthProvider>
    </Router>
  );
};

export default App;
