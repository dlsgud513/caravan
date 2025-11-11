
'use client';

import { useState } from 'react';

const ListCaravanPage = () => {
  // In a real app, you'd have a more complex state management for a multi-step form
  const [formData, setFormData] = useState({
    name: '',
    type: 'Motorhome',
    sleeps: 2,
    location: '',
    pricePerDay: 100,
    description: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-md">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">List Your Caravan</h1>
      <p className="text-gray-600 mb-8">Fill out the details below to put your caravan on the market.</p>

      <form className="space-y-8">
        {/* Section 1: Basic Info */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold border-b pb-2">Basic Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">Caravan Name</label>
              <input type="text" name="name" id="name" placeholder='e.g., "The Voyager"' className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm" />
            </div>
            <div>
              <label htmlFor="location" className="block text-sm font-medium text-gray-700">Location</label>
              <input type="text" name="location" id="location" placeholder="e.g., Seoul, South Korea" className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm" />
            </div>
            <div>
              <label htmlFor="type" className="block text-sm font-medium text-gray-700">Caravan Type</label>
              <select name="type" id="type" className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm">
                <option>Motorhome</option>
                <option>Campervan</option>
                <option>Trailer</option>
              </select>
            </div>
            <div>
              <label htmlFor="sleeps" className="block text-sm font-medium text-gray-700">Sleeps (Capacity)</label>
              <input type="number" name="sleeps" id="sleeps" min="1" className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm" />
            </div>
          </div>
        </div>

        {/* Section 2: Details & Pricing */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold border-b pb-2">Details & Pricing</h2>
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700">Description</label>
            <textarea name="description" id="description" rows={4} placeholder="Tell guests about your caravan..." className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm"></textarea>
          </div>
          <div>
            <label htmlFor="pricePerDay" className="block text-sm font-medium text-gray-700">Price per Day ($)</label>
            <input type="number" name="pricePerDay" id="pricePerDay" min="0" placeholder="100" className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm" />
          </div>
        </div>

        {/* Section 3: Photos */}
        <div className="space-y-4">
            <h2 className="text-xl font-semibold border-b pb-2">Photos</h2>
            <div>
                <label className="block text-sm font-medium text-gray-700">Upload photos</label>
                <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                    <div className="space-y-1 text-center">
                        <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                            <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                        <div className="flex text-sm text-gray-600">
                            <label htmlFor="file-upload" className="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500">
                                <span>Upload a file</span>
                                <input id="file-upload" name="file-upload" type="file" className="sr-only" multiple />
                            </label>
                            <p className="pl-1">or drag and drop</p>
                        </div>
                        <p className="text-xs text-gray-500">PNG, JPG, GIF up to 10MB</p>
                    </div>
                </div>
            </div>
        </div>

        <div className="pt-5">
          <div className="flex justify-end">
            <button type="button" className="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50">
              Cancel
            </button>
            <button type="submit" className="ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
              Submit for Review
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default ListCaravanPage;
