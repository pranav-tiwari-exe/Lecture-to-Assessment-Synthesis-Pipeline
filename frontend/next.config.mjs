/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/proxy/:path*',
        destination: 'http://localhost:8080/:path*',
      },
    ];
  },
};
export default nextConfig;