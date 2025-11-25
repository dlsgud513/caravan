export interface User {
  user_id: number;
  email: string;
  name: string;
  picture?: string | null;
  balance: number;
  provider?: string | null;
  social_id?: string | null;
}

export interface Caravan {
  caravan_id: number;
  name: string;
  type: string;
  price_per_day: number;
  location?: string;
  sleeps?: number;
  owner_id: number;
  is_available: boolean;
  average_rating: number;
  review_count: number;
  image_url?: string;
}