// AppContext.js
import React, { createContext, useState } from 'react';

// Create a context
const AppContext = createContext();

// Create a Provider component
const AppProvider = ({ children }) => {
  const [theme, setTheme] = useState('light');
  const [attemptShow, setAttemptShow] = useState('error'); //none, error, all

  return (
    <AppContext.Provider value={{ attemptShow, setAttemptShow }}>
      {children}
    </AppContext.Provider>
  );
};

export { AppProvider, AppContext };
