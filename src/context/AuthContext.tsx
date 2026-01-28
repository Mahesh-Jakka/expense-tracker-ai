'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { AuthUser } from '@/types/auth';
import {
  login as authLogin,
  signup as authSignup,
  getSession,
  clearSession,
  seedAdmin,
} from '@/utils/auth';

interface AuthContextType {
  user: AuthUser | null;
  isLoading: boolean;
  login: (username: string, password: string) => string | null;
  signup: (username: string, password: string) => string | null;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    seedAdmin();
    const session = getSession();
    setUser(session);
    setIsLoading(false);
  }, []);

  const login = (username: string, password: string): string | null => {
    const result = authLogin(username, password);
    if (typeof result === 'string') return result;
    setUser(result);
    return null;
  };

  const signup = (username: string, password: string): string | null => {
    const result = authSignup(username, password);
    if (typeof result === 'string') return result;
    setUser(result);
    return null;
  };

  const logout = () => {
    clearSession();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
