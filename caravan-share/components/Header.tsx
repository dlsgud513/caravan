'use client';

import Link from 'next/link';
import { useAuth } from '@/app/context/AuthContext';
import Image from 'next/image';

const Header = () => {
  const { user, loading, logout } = useAuth();

  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="text-2xl font-bold text-gray-800">
          <Link href="/">CaravanShare</Link>
        </div>
        <nav className="space-x-4 flex items-center text-gray-600">
          <Link href="/list" className="hover:text-gray-900">All Caravans</Link>
          
          {loading ? (
            <div className="h-8 w-24 bg-gray-200 rounded-md animate-pulse"></div>
          ) : user ? (
            <>
              {/* This link is for the feature that is NOT being restored */}
              {/* <Link href="/caravans/new" className="hover:text-gray-900">List Your Caravan</Link> */}
              <Link href="/mypage" className="hover:text-gray-900">My Page</Link>
              <span className="text-sm">Welcome, {user.name}!</span>
              {user.picture && (
                <Image 
                  src={user.picture} 
                  alt={user.name}
                  width={32}
                  height={32}
                  className="rounded-full"
                />
              )}
              <button 
                onClick={logout} 
                className="hover:text-gray-900"
              >
                Log Out
              </button>
            </>
          ) : (
            <>
              <Link href="/signup" className="hover:text-gray-900">Sign Up</Link>
              <Link href="/login" className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">
                Log In
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Header;