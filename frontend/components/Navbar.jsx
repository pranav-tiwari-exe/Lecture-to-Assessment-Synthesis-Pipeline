import Link from "next/link";
import ThemeToggler from "./ThemeToggler";

export default function Navbar() {

  return (
    <nav className="px-6 py-8 mb-6 flex justify-between items-center rounded-lg">
      <Link href="/" className="text-2xl font-bold">
        myQ
      </Link>
      <div className="flex space-x-6">
        <Link href="/generate" className="hover:text-blue-400 transition-colors">
          Generate
        </Link>
        <ThemeToggler/>
      </div>
        
    </nav>
  );
}