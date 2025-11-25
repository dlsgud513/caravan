'use client';

import { useState, FormEvent } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/app/context/AuthContext';

const LoginPage = () => {
  const router = useRouter();
  const { login } = useAuth(); // Assuming AuthContext provides a login function
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleDirectLogin = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      await login(email, password);
      // Use a full page reload to ensure the auth state is re-evaluated
      window.location.href = '/';
    } catch (err: any) {
      setError(err.message || "Failed to log in.");
    }
  };

  const handleGoogleLogin = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/auth/url/google');
      if (!res.ok) throw new Error('Failed to get Google auth URL');
      const data = await res.json();
      window.location.href = data.url;
    } catch (error) {
      console.error('Error during Google login:', error);
      setError("Could not connect to Google login.");
    }
  };

  const handleKakaoLogin = () => alert('Kakao login is not implemented yet.');
  const handleNaverLogin = () => alert('Naver login is not implemented yet.');

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Or{' '}
            <Link href="/signup" className="font-medium text-blue-600 hover:text-blue-500">
              create a new account
            </Link>
          </p>
        </div>

        {/* Direct Login Form */}
        <form className="mt-8 space-y-6" onSubmit={handleDirectLogin}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="email-address" className="sr-only">Email address</label>
              <input id="email-address" name="email" type="email" autoComplete="email" required value={email} onChange={e => setEmail(e.target.value)} className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" placeholder="Email address" />
            </div>
            <div>
              <label htmlFor="password" className="sr-only">Password</label>
              <input id="password" name="password" type="password" autoComplete="current-password" required value={password} onChange={e => setPassword(e.target.value)} className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" placeholder="Password" />
            </div>
          </div>

          {error && <p className="text-sm text-center text-red-600">{error}</p>}

          <div>
            <button type="submit" className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
              Sign in
            </button>
          </div>
        </form>

        {/* Divider */}
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-gray-50 text-gray-500">Or continue with</span>
          </div>
        </div>

        {/* Social Logins */}
        <div className="space-y-4">
          <button onClick={handleGoogleLogin} className="w-full flex items-center justify-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
            <svg className="w-5 h-5 mr-2" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"></path><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"></path><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"></path><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.82l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"></path><path fill="none" d="M0 0h48v48H0z"></path></svg>
            Sign in with Google
          </button>
          <button onClick={handleKakaoLogin} className="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-black bg-[#FEE500] hover:bg-yellow-400">
            <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10c5.52 0 10-4.48 10-10S17.52 2 12 2zm-1.2 14.4c-2.4 0-4.32-1.92-4.32-4.32s1.92-4.32 4.32-4.32c1.12 0 2.16.44 2.96 1.16l-1.2 1.2c-.4-.4-.96-.64-1.76-.64-1.44 0-2.64 1.2-2.64 2.6s1.2 2.64 2.64 2.64c1.68 0 2.4-1.04 2.56-1.6h-2.56v-2h4.32c.08.24.16.48.16.8 0 2.56-1.76 4.4-4.48 4.4z"/></svg>
            Sign in with Kakao
          </button>
          <button onClick={handleNaverLogin} className="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-[#03C75A] hover:bg-green-600">
            <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24" fill="currentColor"><path d="M16.28 9.52H7.72v4.96h5.44V9.52z M7.72 4h8.56v4.52h-8.56V4z m0 11.48h8.56V20H7.72v-4.52z"/></svg>
            Sign in with Naver
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
