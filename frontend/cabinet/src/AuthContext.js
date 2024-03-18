import { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setAuthenticated] = useState(false);
  const [userRole, setUserRole] = useState(null);
  const [userId, setUserID] = useState(null);
  const [userToken, setUserToken] = useState(null);

  const login = (role, id, token) => {
    setAuthenticated(true);
    setUserRole(role);
    setUserID(id);
    setUserToken(token);
  };
  const logout = () => {
    setAuthenticated(false);
    setUserRole(null);
    setUserID(null);
    setUserToken(null);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, userRole, userId, userToken, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};