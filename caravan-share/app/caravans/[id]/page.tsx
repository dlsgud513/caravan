'use client';

import { useState, useEffect, FormEvent } from 'react';
import { useParams, notFound } from 'next/navigation';
import Image from 'next/image';
import { Caravan } from '@/app/lib/types';
import DynamicMap from '@/components/DynamicMap';
import L from 'leaflet';
import { useAuth } from '@/app/context/AuthContext';

// Define a type for our Points of Interest, which we'll fetch from the backend
interface PointOfInterest {
  name: string;
  type: 'campground' | 'toilet';
  latitude: number;
  longitude: number;
  address: string;
}

// Custom icons for the map
const campgroundIcon = new L.Icon({
  iconUrl: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzI1NjNFRSI+PHBhdGggZD0iTTEyIDEuNUwzLjUgMTVoMTdMMTIgMS41ek0xMSAxNnYtMmgydjJoLTJ6bS0uNS0zLjVMMTAgOC41bDQuNSA2aC05eiIvPjwvc3ZnPg==',
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const toiletIcon = new L.Icon({
  iconUrl: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzRFNTc3NSI+PHBhdGggZD0iTTIxIDJINGMtMS4xIDAtMiAuOS0yIDJ2MTZjMCAxLjEuOSAyIDIgMmgxNWMxLjEgMCAyLS45IDItMlY0YzAtMS4xLS45LTItMi0yem0tOSA2Yy0xLjY2IDAtMyAxLjM0LTMgM3MxLjM0IDMgMyAzIDMtMS4zNCAzLTMtMS4zNC0zLTMtM3ptNiAxMkg4di0uOThjMC0yIDEuMjUtMy40NyAzLTMuOTVWOS41YzAtLjI4LjIyLS41LjUtLjVoMS41Yy4yOCAwIC41LjIyLjUuNXYxLjA1YzEuNzUuNDggMyAzLjAyIDMgMy45OFYxOHoiLz48L3N2Zz4=',
  iconSize: [28, 28],
  iconAnchor: [14, 28],
  popupAnchor: [0, -28],
});

const CaravanPage = () => {
  const params = useParams();
  const id = params.id as string;
  const { user } = useAuth(); // Get user info for booking

  const [caravan, setCaravan] = useState<Caravan | null>(null);
  const [pois, setPois] = useState<PointOfInterest[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // State for booking form
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [bookingError, setBookingError] = useState<string | null>(null);
  const [bookingSuccess, setBookingSuccess] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;

    const fetchData = async () => {
      try {
        const caravanRes = await fetch(`http://localhost:8000/api/caravans/${id}`);
        if (!caravanRes.ok) {
          if (caravanRes.status === 404) notFound();
          throw new Error('Failed to fetch caravan details');
        }
        const caravanData: Caravan = await caravanRes.json();
        setCaravan(caravanData);

        if (caravanData.location) {
          const poiRes = await fetch(`http://localhost:8000/api/points-of-interest?location=${encodeURIComponent(caravanData.location)}`);
          if (poiRes.ok) {
            const poiData: PointOfInterest[] = await poiRes.json();
            setPois(poiData);
          }
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  const handleBookingSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setBookingError(null);
    setBookingSuccess(null);

    if (!user) {
      setBookingError("Please log in to make a reservation.");
      return;
    }
    if (!startDate || !endDate) {
      setBookingError("Please select both a start and end date.");
      return;
    }
    if (new Date(startDate) >= new Date(endDate)) {
      setBookingError("End date must be after the start date.");
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/reservations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          caravan_id: caravan?.caravan_id,
          start_date: startDate,
          end_date: endDate,
        }),
        credentials: 'include', // Important for sending the auth cookie
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to make reservation.");
      }

      const newReservation = await response.json();
      setBookingSuccess(`Reservation successful! Your booking ID is ${newReservation.reservation_id}.`);

    } catch (err: any) {
      setBookingError(err.message);
    }
  };

  if (loading) return <p className="text-center">Loading...</p>;
  if (error) return <p className="text-center text-red-500">Error: {error}</p>;
  if (!caravan) return notFound();

  const mapCenter: [number, number] = pois.length > 0 ? [pois[0].latitude, pois[0].longitude] : [37.5665, 126.9780];
  const markers = pois.map(poi => ({
    position: [poi.latitude, poi.longitude] as [number, number],
    popupText: `${poi.name} (${poi.address})`,
    icon: poi.type === 'campground' ? campgroundIcon : toiletIcon,
  }));

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
      {/* Main Content */}
      <div className="lg:col-span-2">
        <div className="mb-4">
          <Image
            src={caravan.image_url || 'https://placehold.co/800x600/374151/FFFFFF?text=Caravan'}
            alt={caravan.name}
            width={800}
            height={600}
            className="rounded-lg object-cover w-full"
            priority
          />
        </div>
        <div>
          <h1 className="text-4xl font-bold text-gray-800">{caravan.name}</h1>
          <p className="text-lg text-gray-500">{caravan.location}</p>
        </div>
        <hr className="my-8" />
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">About this caravan</h2>
        <p className="text-gray-600 mb-8">{caravan.description}</p>
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Nearby Facilities</h2>
        <div className="mb-8 rounded-lg overflow-hidden shadow-md">
          <DynamicMap center={mapCenter} markers={markers} />
        </div>
      </div>

      {/* Booking Sidebar */}
      <div className="lg:col-span-1">
        <div className="sticky top-24 p-6 border rounded-lg shadow-lg bg-white">
          <p className="text-2xl font-bold text-gray-800 mb-4">
            ${caravan.price_per_day} <span className="text-lg font-normal text-gray-600">/ day</span>
          </p>
          <form onSubmit={handleBookingSubmit}>
            <div className="mb-4">
              <label htmlFor="start-date" className="block text-sm font-medium text-gray-700">Start Date</label>
              <input type="date" id="start-date" value={startDate} onChange={e => setStartDate(e.target.value)} required className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" />
            </div>
            <div className="mb-4">
              <label htmlFor="end-date" className="block text-sm font-medium text-gray-700">End Date</label>
              <input type="date" id="end-date" value={endDate} onChange={e => setEndDate(e.target.value)} required className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" />
            </div>
            <button type="submit" className="w-full bg-blue-500 text-white py-3 rounded-lg font-semibold hover:bg-blue-600 transition-colors disabled:bg-gray-400" disabled={!user}>
              {user ? 'Request to Book' : 'Log in to Book'}
            </button>
          </form>
          {bookingSuccess && <p className="text-center text-sm text-green-600 mt-4">{bookingSuccess}</p>}
          {bookingError && <p className="text-center text-sm text-red-600 mt-4">{bookingError}</p>}
          {!bookingSuccess && <p className="text-center text-sm text-gray-500 mt-4">You won't be charged yet</p>}
        </div>
      </div>
    </div>
  );
};

export default CaravanPage;
