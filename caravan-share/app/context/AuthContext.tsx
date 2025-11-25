'use client';

import { createContext, useState, useEffect, useContext, ReactNode } from 'react';
import { User } from '@/app/lib/types';

// Define the shape of the context
interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  fetchUser: () => Promise<void>;
}

// Create the context with a default value
const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  login: async () => {},
  logout: () => {},
  fetchUser: async () => {},
});

// Create a custom hook to use the auth context
export const useAuth = () => {
  return useContext(AuthContext);
};

// Create the provider component
interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchUser = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/users/me', { credentials: 'include' });
      if (res.ok) {
        const userData = await res.json();
        setUser(userData);
      } else {
        setUser(null);
      }
    } catch (error) {
      console.error('Failed to fetch user', error);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUser();
  }, []);

  const login = async (email: string, password: string) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch('http://localhost:8000/api/auth/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData.toString(),
      credentials: 'include', // Crucial for cross-origin cookie setting
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to log in");
    }
    
    // After successful login, the cookie is set by the backend.
    // We will now re-fetch the user data to update the context state.
    // This ensures the UI updates correctly *before* any redirection.
    await fetchUser();
  };

  const logout = () => {
    // TODO: Implement a backend logout endpoint that clears the HttpOnly cookie.
    setUser(null);
    alert("Logged out (client-side). A backend logout endpoint is needed for full logout.");
  };

  const value = {
    user,
    loading,
    login,
    logout,
    fetchUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};