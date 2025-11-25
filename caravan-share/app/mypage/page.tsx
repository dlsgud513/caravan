'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/app/context/AuthContext';
import { useRouter } from 'next/navigation';
import Image from 'next/image';

// Define the shape of the detailed reservation data
interface ReservationDetails {
    reservation_id: number;
    start_date: string;
    end_date: string;
    total_price: number;
    status: string;
    caravan_name: string;
    caravan_image_url?: string | null;
}

const MyPage = () => {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  
  const [reservations, setReservations] = useState<ReservationDetails[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // If auth is done loading and there's no user, redirect to login
    if (!authLoading && !user) {
      router.push('/login');
      return;
    }

    // If there is a user, fetch their reservations
    if (user) {
      const fetchReservations = async () => {
        try {
          const res = await fetch('http://localhost:8000/api/users/me/reservations', {
            credentials: 'include',
          });
          if (!res.ok) {
            throw new Error('Failed to fetch reservations.');
          }
          const data: ReservationDetails[] = await res.json();
          setReservations(data);
        } catch (err: any) {
          setError(err.message);
        } finally {
          setLoading(false);
        }
      };
      fetchReservations();
    }
  }, [user, authLoading, router]);

  if (authLoading || loading) {
    return <p className="text-center">Loading your page...</p>;
  }

  if (!user) {
    // This is a fallback, the useEffect should have already redirected
    return <p className="text-center">Redirecting to login...</p>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">My Page</h1>

      {/* User Profile Section */}
      <div className="bg-white p-6 rounded-lg shadow-md mb-8 flex items-center">
        {user.picture && (
          <Image
            src={user.picture}
            alt={user.name}
            width={80}
            height={80}
            className="rounded-full mr-6"
          />
        )}
        <div>
          <h2 className="text-2xl font-semibold">{user.name}</h2>
          <p className="text-gray-600">{user.email}</p>
          <p className="text-gray-600">Balance: ${user.balance.toFixed(2)}</p>
        </div>
      </div>

      {/* Reservations Section */}
      <h2 className="text-2xl font-bold mb-4 text-gray-800">My Reservations</h2>
      {error && <p className="text-red-500">Error fetching reservations: {error}</p>}
      
      {reservations.length === 0 && !error && (
        <p className="text-gray-500 bg-white p-6 rounded-lg shadow-md">You have no reservations.</p>
      )}

      <div className="space-y-6">
        {reservations.map(res => (
          <div key={res.reservation_id} className="bg-white p-4 rounded-lg shadow-md flex items-center">
            <div className="w-32 h-24 relative mr-4 flex-shrink-0">
              <Image
                src={res.caravan_image_url || 'https://placehold.co/400x300/374151/FFFFFF?text=Caravan'}
                alt={res.caravan_name}
                layout="fill"
                objectFit="cover"
                className="rounded-md"
              />
            </div>
            <div className="flex-grow">
              <h3 className="text-lg font-semibold">{res.caravan_name}</h3>
              <p className="text-sm text-gray-600">
                {new Date(res.start_date).toLocaleDateString()} - {new Date(res.end_date).toLocaleDateString()}
              </p>
              <p className="text-sm text-gray-500">Status: <span className={`font-medium ${res.status === 'confirmed' ? 'text-green-600' : 'text-yellow-600'}`}>{res.status}</span></p>
            </div>
            <div className="text-right">
              <p className="text-lg font-bold">${res.total_price.toFixed(2)}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MyPage;
