
'use client';

import { useState } from 'react';
import Link from 'next/link';

const SignUpPage = () => {
  const [role, setRole] = useState('guest'); // 'guest' or 'host'

  return (
    <div className="flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Or{' '}
            <Link href="/login" className="font-medium text-blue-600 hover:text-blue-500">
              sign in to your existing account
            </Link>
          </p>
        </div>
        <form className="mt-8 space-y-6" action="#" method="POST">
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="full-name" className="sr-only">Full Name</label>
              <input id="full-name" name="name" type="text" required className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" placeholder="Full Name" />
            </div>
            <div>
              <label htmlFor="email-address" className="sr-only">Email address</label>
              <input id="email-address" name="email" type="email" autoComplete="email" required className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" placeholder="Email address" />
            </div>
            <div>
              <label htmlFor="password" className="sr-only">Password</label>
              <input id="password" name="password" type="password" autoComplete="current-password" required className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" placeholder="Password" />
            </div>
          </div>

          <div className="flex items-center justify-around">
            <div
              onClick={() => setRole('guest')}
              className={`cursor-pointer p-4 border-2 rounded-lg w-1/2 text-center ${role === 'guest' ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}`}
            >
              <h3 className="font-medium text-gray-900">I want to rent</h3>
              <p className="text-sm text-gray-500">Sign up as a Guest</p>
            </div>
            <div
              onClick={() => setRole('host')}
              className={`cursor-pointer p-4 border-2 rounded-lg w-1/2 text-center ml-4 ${role === 'host' ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}`}
            >
              <h3 className="font-medium text-gray-900">I want to list</h3>
              <p className="text-sm text-gray-500">Sign up as a Host</p>
            </div>
          </div>

          <div>
            <button type="submit" className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
              Sign up
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SignUpPage;
