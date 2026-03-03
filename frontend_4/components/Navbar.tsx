"use client";

import Link from "next/link";
import { useState } from "react";
import { Menu, X, Activity } from "lucide-react";

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 backdrop-blur-xl bg-[#030712]/80 border-b border-violet-500/10">
      <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">

        {/* Logo */}
        <Link href="/" className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-violet-600 to-indigo-600 rounded-lg">
            <Activity className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-black tracking-tight text-white">
            Civic<span className="text-violet-400">Resolve</span>
          </span>
        </Link>

        {/* Desktop Links */}
        <nav className="hidden md:flex items-center gap-8 text-sm font-bold text-slate-400">
          <Link href="/" className="hover:text-violet-400 transition-colors">
            Home
          </Link>
          <Link href="/privacy-policy" className="hover:text-violet-400 transition-colors">
            Privacy
          </Link>
          <Link href="/terms-conditions" className="hover:text-violet-400 transition-colors">
            Terms
          </Link>
          <Link href="/disclaimer" className="hover:text-violet-400 transition-colors">
            Disclaimer
          </Link>
        </nav>

        {/* Mobile Toggle */}
        <button
          onClick={() => setOpen(!open)}
          className="md:hidden text-slate-400"
        >
          {open ? <X /> : <Menu />}
        </button>
      </div>

      {/* Mobile Menu */}
      {open && (
        <div className="md:hidden px-6 pb-6 space-y-4 text-sm font-bold text-slate-400 bg-[#030712]/95 border-t border-violet-500/10">
          <Link href="/" onClick={() => setOpen(false)}>Home</Link>
          <Link href="/privacy-policy" onClick={() => setOpen(false)}>Privacy</Link>
          <Link href="/terms-conditions" onClick={() => setOpen(false)}>Terms</Link>
          <Link href="/disclaimer" onClick={() => setOpen(false)}>Disclaimer</Link>
        </div>
      )}
    </header>
  );
}
