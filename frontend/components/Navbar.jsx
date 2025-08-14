import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="bg-gray-900 text-white px-6 py-4 flex justify-between items-center shadow-md">
      {/* Logo */}
      <Link href="/" className="text-2xl font-bold">
        myQ
      </Link>

      {/* Navigation Links */}
      <div className="flex space-x-6">
        <Link href="/" className="hover:text-blue-400 transition-colors">
          Home
        </Link>
        <Link href="/generate" className="hover:text-blue-400 transition-colors">
          About
        </Link>
        <Link href="/contact" className="hover:text-blue-400 transition-colors">
          Contact
        </Link>
      </div>
    </nav>
  );
}
