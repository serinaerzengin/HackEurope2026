"use client";

import Link from "next/link";
import Image from "next/image";
import { useState } from "react";
import { StripedPattern } from "@/components/magicui/striped-pattern";
import { TypingAnimation } from "@/components/ui/typing-animation";
import { CodeXmlIcon } from "@/components/icons/lucide-code-xml";
import { NetworkIcon } from "@/components/icons/lucide-network";
import { NavDock } from "@/components/nav-dock";

const TYPES = [
  {
    id: "coding",
    icon: CodeXmlIcon,
    title: "Coding Interview",
    description: "Algorithms, data structures & problem solving.",
  },
  {
    id: "system-design",
    icon: NetworkIcon,
    title: "System Design",
    description: "Architecture, scalability & design patterns.",
  },
] as const;

type InterviewType = (typeof TYPES)[number]["id"];

export default function Home() {
  const [selected, setSelected] = useState<InterviewType | null>(null);

  return (
    <div className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden px-6">
      <NavDock />
      <StripedPattern className="text-slate-200 dark:text-slate-900" />

      {/* Logo */}
      <div className="relative z-10 mb-8">
        <Image src="/logo..png" alt="Intervox" width={320} height={80} priority style={{ width: "320px", height: "auto" }} />
      </div>

      {/* Subtitle */}
      <div className="relative z-10 mb-16 text-center">
        <TypingAnimation className="text-zinc-500 dark:text-zinc-400 text-base" duration={30}>
          Practice your interview skills with an AI interviewer.
        </TypingAnimation>
      </div>

      {/* Stacked rows */}
      <div className="relative z-10 w-[380px] mb-10">
        <div className="border-t border-zinc-200 dark:border-zinc-800" />
        {TYPES.map(({ id, icon: Icon, title, description }) => {
          const isSelected = selected === id;
          return (
            <button
              key={id}
              onClick={() => setSelected(id)}
              className={`
                relative w-full flex items-center gap-4 px-4 py-5 text-left outline-none
                transition-colors duration-200
                ${isSelected ? "bg-zinc-50 dark:bg-zinc-900/50" : "hover:bg-zinc-50/60 dark:hover:bg-zinc-900/30"}
              `}
            >
              {/* Left accent bar */}
              <span
                className={`absolute left-0 top-0 bottom-0 w-0.5 bg-black dark:bg-white transition-opacity duration-200 ${isSelected ? "opacity-100" : "opacity-0"}`}
              />

              {/* Icon */}
              <Icon
                size={20}
                className={`shrink-0 transition-colors duration-200 ${isSelected ? "text-black dark:text-white" : "text-zinc-400"}`}
              />

              {/* Text */}
              <div className="flex-1 min-w-0">
                <p className={`text-sm font-medium transition-colors duration-200 ${isSelected ? "text-black dark:text-white" : "text-zinc-700 dark:text-zinc-300"}`}>
                  {title}
                </p>
                <p className="text-xs text-zinc-400 mt-0.5">{description}</p>
              </div>

              {/* Radio circle */}
              <span
                className={`
                  shrink-0 w-4 h-4 rounded-full border transition-all duration-200 flex items-center justify-center
                  ${isSelected
                    ? "border-black bg-black dark:border-white dark:bg-white"
                    : "border-zinc-300 dark:border-zinc-600 bg-transparent"
                  }
                `}
              >
                {isSelected && (
                  <span className="w-1.5 h-1.5 rounded-full bg-white dark:bg-black" />
                )}
              </span>
            </button>
          );
        })}
        <div className="border-t border-zinc-200 dark:border-zinc-800" />
      </div>

      {/* Start button */}
      <div className="relative z-10 h-12">
        {selected && (
          <Link
            href={`/interview?type=${selected}`}
            className="rounded-full bg-black text-white dark:bg-white dark:text-black px-10 py-3 text-sm font-medium hover:opacity-80 transition-opacity animate-in fade-in slide-in-from-bottom-2 duration-300"
          >
            Start Interview →
          </Link>
        )}
      </div>
    </div>
  );
}
