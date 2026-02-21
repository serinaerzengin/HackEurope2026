"use client";

import Link from "next/link";
import { Home } from "lucide-react";
import { Dock, DockIcon } from "@/components/ui/dock";

export function NavDock() {
  return (
    <div className="fixed top-8 left-0 right-0 z-50 flex justify-center pointer-events-none">
      <Dock
        disableMagnification
        iconSize={28}
        className="pointer-events-auto !mt-0 bg-white border-zinc-200 shadow-sm gap-3"
      >
        {/* Home — greyed icon with subtle bg to mark current page */}
        <DockIcon className="rounded-lg bg-zinc-100 dark:bg-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-800">
          <Link href="/" aria-label="Home" className="flex items-center justify-center text-zinc-500 dark:text-zinc-400">
            <Home size={14} strokeWidth={1.75} />
          </Link>
        </DockIcon>

        {/* Pipe separator */}
        <span className="text-zinc-400 select-none text-sm leading-none">|</span>

        {/* About Us */}
        <Link
          href="#"
          className="text-xs font-medium text-zinc-700"
        >
          About Us
        </Link>

        {/* Pipe separator */}
        <span className="text-zinc-400 select-none text-sm leading-none">|</span>

        {/* Contact Us */}
        <Link
          href="#"
          className="text-xs font-medium text-zinc-700"
        >
          Contact Us
        </Link>
      </Dock>
    </div>
  );
}
