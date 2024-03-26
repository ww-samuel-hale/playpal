// src/contexts/MyProvider.js or src/contexts/MyContext.js
import React, { useState } from 'react';
import MyContext from './Context';

export const MyProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const login = (userData) => {
    setUser(userData);
  }

  const logout = () => {
    setUser(null);
  }

  return (
    <MyContext.Provider value={{ user, login, logout }}>
      {children}
    </MyContext.Provider>
  );
};
