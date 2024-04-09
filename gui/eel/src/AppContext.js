// AppContext.js
import React, { createContext, useState, useRef } from 'react';

// Create a context
const AppContext = createContext();

// Create a Provider component
const AppProvider = ({ children }) => {
  const [theme, setTheme] = useState('light');
  const showingRef = useRef("")
  const prevShowingRef = useRef("")

  return (
    <AppContext.Provider value={{ showingRef,prevShowingRef }}>
      {children}
    </AppContext.Provider>
  );
};

export { AppProvider, AppContext };
