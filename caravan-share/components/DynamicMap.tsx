import dynamic from 'next/dynamic';

const DynamicMap = dynamic(() => import('./Map'), {
  ssr: false,
  loading: () => <div style={{ height: '400px', background: '#e0e0e0' }} />,
});

export default DynamicMap;
