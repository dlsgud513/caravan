
export interface Host {
  name: string;
  avatarUrl: string;
}

export interface Caravan {
  id: string;
  name: string;
  location: string;
  pricePerDay: number;
  sleeps: number;
  type: 'Motorhome' | 'Campervan' | 'Trailer';
  imageUrl: string;
  description: string;
  amenities: string[];
  host: Host;
}

export const mockCaravans: Caravan[] = [
  {
    id: '1',
    name: 'Modern Motorhome "The Voyager"',
    location: 'Seoul, South Korea',
    pricePerDay: 150,
    sleeps: 4,
    type: 'Motorhome',
    imageUrl: 'https://placehold.co/600x400/E2E8F0/4A5568?text=Caravan+1',
    description: 'Experience the future of road trips with this state-of-the-art motorhome. Fully equipped with a modern kitchen, a comfortable sleeping area, and a spacious bathroom. Perfect for families or a group of friends.',
    amenities: ['Kitchen', 'Wi-Fi', 'Air Conditioning', 'Shower', 'TV'],
    host: {
      name: 'Min-jun Kim',
      avatarUrl: 'https://placehold.co/100x100/3182CE/FFFFFF?text=MK'
    }
  },
  {
    id: '2',
    name: 'Vintage Campervan "Daisy"',
    location: 'Busan, South Korea',
    pricePerDay: 90,
    sleeps: 2,
    type: 'Campervan',
    imageUrl: 'https://placehold.co/600x400/E2E8F0/4A5568?text=Caravan+2',
    description: 'Travel back in time with Daisy, a beautifully restored vintage campervan. It\'s cozy, full of character, and perfect for a romantic getaway along the coast.',
    amenities: ['Kitchenette', 'Heating', 'Sound System'],
    host: {
      name: 'Seo-yeon Park',
      avatarUrl: 'https://placehold.co/100x100/3182CE/FFFFFF?text=SP'
    }
  },
  {
    id: '3',
    name: 'Family Sized Trailer "The Nomad"',
    location: 'Jeju Island, South Korea',
    pricePerDay: 120,
    sleeps: 6,
    type: 'Trailer',
    imageUrl: 'https://placehold.co/600x400/E2E8F0/4A5568?text=Caravan+3',
    description: 'The Nomad is your home away from home. With bunk beds for the kids and a master sleeping area, this trailer is ideal for family adventures in the beautiful landscapes of Jeju.',
    amenities: ['Full Kitchen', 'Bunk Beds', 'Awning', 'Outdoor Grill'],
    host: {
      name: 'Ji-hoon Lee',
      avatarUrl: 'https://placehold.co/100x100/3182CE/FFFFFF?text=JL'
    }
  },
  {
    id: '4',
    name: 'Compact Camper "The Adventurer"',
    location: 'Gyeongju, South Korea',
    pricePerDay: 80,
    sleeps: 2,
    type: 'Campervan',
    imageUrl: 'https://placehold.co/600x400/E2E8F0/4A5568?text=Caravan+4',
    description: 'Easy to drive and park, The Adventurer is perfect for exploring historical cities and narrow country roads. It has everything you need for a simple and flexible trip.',
    amenities: ['Basic Kitchenette', 'Portable Toilet', 'Heating'],
    host: {
      name: 'Ha-eun Choi',
      avatarUrl: 'https://placehold.co/100x100/3182CE/FFFFFF?text=HC'
    }
  },
];
