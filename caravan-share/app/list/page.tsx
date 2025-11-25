'use client';

import { useState, useEffect } from 'react';
import { Caravan } from '@/app/lib/types';
import CaravanCard from '@/components/CaravanCard';

const AllCaravansPage = () => {
  const [caravans, setCaravans] = useState<Caravan[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCaravans = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/caravans');
        if (!res.ok) {
          throw new Error('Failed to fetch caravans');
        }
        const data: Caravan[] = await res.json();
        setCaravans(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCaravans();
  }, []);

  if (loading) {
    return <p className="text-center text-gray-500">Loading caravans...</p>;
  }

  if (error) {
    return <p className="text-center text-red-500">Error: {error}</p>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">Explore Our Caravans</h1>
      
      {caravans.length === 0 ? (
        <p className="text-center text-gray-500">No caravans available at the moment.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
          {caravans.map((caravan) => (
            <CaravanCard key={caravan.caravan_id} caravan={caravan} />
          ))}
        </div>
      )}
    </div>
  );
};

export default AllCaravansPage;