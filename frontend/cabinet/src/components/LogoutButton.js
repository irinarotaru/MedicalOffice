import React from 'react';

const LogoutButton = () => {
    const { logout } = useAuth();
  
    const handleLogout = () => {
      logout();
    };

  return (
    <button onClick={handleLogout}>Logout</button>
  );
};

export default LogoutButton;