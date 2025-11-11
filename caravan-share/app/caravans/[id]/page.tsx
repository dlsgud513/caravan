
import { mockCaravans } from '@/lib/mock-data';
import { notFound } from 'next/navigation';
import Image from 'next/image';

interface CaravanPageProps {
  params: {
    id: string;
  };
}

const CaravanPage = ({ params }: CaravanPageProps) => {
  const caravan = mockCaravans.find((c) => c.id === params.id);

  if (!caravan) {
    notFound();
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
      {/* Main Content */}
      <div className="lg:col-span-2">
        <div className="mb-4">
          <Image
            src={caravan.imageUrl}
            alt={caravan.name}
            width={800}
            height={600}
            className="rounded-lg object-cover w-full"
            priority
          />
        </div>
        <div className="flex justify-between items-start mb-4">
            <div>
                <h1 className="text-4xl font-bold text-gray-800">{caravan.name}</h1>
                <p className="text-lg text-gray-500">{caravan.location}</p>
            </div>
            <div className="text-right">
                <div className="flex items-center">
                    <Image src={caravan.host.avatarUrl} alt={caravan.host.name} width={50} height={50} className="rounded-full" />
                    <span className="ml-2 text-gray-700">{caravan.host.name}</span>
                </div>
                <p className="text-sm text-gray-500">Host</p>
            </div>
        </div>

        <hr className="my-8" />

        <h2 className="text-2xl font-semibold text-gray-800 mb-4">About this caravan</h2>
        <p className="text-gray-600 mb-8">{caravan.description}</p>

        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Amenities</h2>
        <ul className="grid grid-cols-2 gap-4 mb-8">
          {caravan.amenities.map((amenity) => (
            <li key={amenity} className="flex items-center text-gray-600">
              <svg className="w-5 h-5 mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
              {amenity}
            </li>
          ))}
        </ul>
      </div>

      {/* Booking Sidebar */}
      <div className="lg:col-span-1">
        <div className="sticky top-24 p-6 border rounded-lg shadow-lg bg-white">
          <p className="text-2xl font-bold text-gray-800 mb-4">
            ${caravan.pricePerDay} <span className="text-lg font-normal text-gray-600">/ day</span>
          </p>
          <form>
            <div className="mb-4">
              <label htmlFor="start-date" className="block text-sm font-medium text-gray-700">Start Date</label>
              <input type="date" id="start-date" className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" />
            </div>
            <div className="mb-4">
              <label htmlFor="end-date" className="block text-sm font-medium text-gray-700">End Date</label>
              <input type="date" id="end-date" className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" />
            </div>
            <button type="submit" className="w-full bg-blue-500 text-white py-3 rounded-lg font-semibold hover:bg-blue-600 transition-colors">
              Request to Book
            </button>
          </form>
          <p className="text-center text-sm text-gray-500 mt-4">You won't be charged yet</p>
        </div>
      </div>
    </div>
  );
};

export default CaravanPage;
