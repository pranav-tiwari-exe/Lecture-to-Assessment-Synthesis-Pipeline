"use client";
import { createContext, useState, useContext, useEffect } from "react";
import { ThemeProvider } from "next-themes";

export const AppContext = createContext();

export const AppContextProvider = ({ children }) => {
  
  const values = {}

  return (
    <AppContext.Provider value={values}>
      <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
      </ThemeProvider>
    </AppContext.Provider>
  );
};

export const useAppContext = () => useContext(AppContext);