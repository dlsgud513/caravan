
import Link from 'next/link';
import Image from 'next/image';
import { Caravan } from '@/lib/mock-data';

interface CaravanCardProps {
  caravan: Caravan;
}

const CaravanCard = ({ caravan }: CaravanCardProps) => {
  return (
    <div className="border rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300">
      <Link href={`/caravans/${caravan.id}`}>
        <div className="relative w-full h-56">
          <Image
            src={caravan.imageUrl}
            alt={caravan.name}
            layout="fill"
            objectFit="cover"
          />
        </div>
        <div className="p-4">
          <h3 className="text-lg font-semibold text-gray-800">{caravan.name}</h3>
          <p className="text-sm text-gray-500">{caravan.type} &middot; {caravan.location}</p>
          <div className="mt-4 flex justify-between items-center">
            <p className="text-lg font-bold text-gray-900">${caravan.pricePerDay}<span className="text-sm font-normal text-gray-600">/day</span></p>
            <span className="text-blue-500 hover:text-blue-600 font-semibold">View Details</span>
          </div>
        </div>
      </Link>
    </div>
  );
};

export default CaravanCard;
