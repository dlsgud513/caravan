
import Link from 'next/link';

const Header = () => {
  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="text-2xl font-bold text-gray-800">
          <Link href="/">CaravanShare</Link>
        </div>
        <nav className="space-x-6 text-gray-600">
          <Link href="/search" className="hover:text-gray-900">Search Caravans</Link>
          <Link href="/list" className="hover:text-gray-900">List Your Caravan</Link>
          <Link href="/signup" className="hover:text-gray-900">Sign Up</Link>
          <Link href="/login" className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Log In</Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
