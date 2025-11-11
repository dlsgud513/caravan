import { mockCaravans } from '@/lib/mock-data';
import CaravanCard from '@/components/CaravanCard';

export default function Home() {
  return (
    <div>
      {/* Hero Section */}
      <section className="relative bg-gray-800 text-white py-20 px-4 text-center mb-12 rounded-lg" style={{ backgroundImage: "url('https://placehold.co/1200x400/374151/FFFFFF?text=Find+Your+Next+Adventure')", backgroundSize: 'cover', backgroundPosition: 'center' }}>
        <div className="relative z-10">
          <h1 className="text-5xl font-bold mb-4">Find Your Next Adventure</h1>
          <p className="text-xl mb-8">Rent the perfect caravan for your dream road trip.</p>
          <form className="max-w-2xl mx-auto">
            <div className="flex items-center bg-white rounded-full shadow-lg p-2">
              <input
                type="text"
                placeholder="Search by location, e.g., 'Jeju Island'"
                className="w-full p-3 text-gray-700 rounded-full focus:outline-none"
              />
              <button
                type="submit"
                className="bg-blue-500 text-white rounded-full px-8 py-3 ml-2 hover:bg-blue-600 transition-colors"
              >
                Search
              </button>
            </div>
          </form>
        </div>
        <div className="absolute inset-0 bg-black opacity-40 rounded-lg"></div>
      </section>

      {/* Featured Caravans Section */}
      <section>
        <h2 className="text-3xl font-bold text-gray-800 mb-6">Popular Caravans</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
          {mockCaravans.map((caravan) => (
            <CaravanCard key={caravan.id} caravan={caravan} />
          ))}
        </div>
      </section>
    </div>
  );
}