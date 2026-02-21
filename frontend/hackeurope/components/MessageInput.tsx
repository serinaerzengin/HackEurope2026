"use client";

import { useState } from "react";

type Props = {
  onSend: (text: string) => void;
  disabled?: boolean;
};

export default function MessageInput({ onSend, disabled }: Props) {
  const [value, setValue] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!value.trim()) return;
    onSend(value.trim());
    setValue("");
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 pt-2 border-t border-zinc-200 dark:border-zinc-700">
      <input
        className="flex-1 rounded-full border border-zinc-300 dark:border-zinc-600 bg-white dark:bg-zinc-900 px-4 py-2 text-sm outline-none focus:ring-2 focus:ring-black dark:focus:ring-white"
        placeholder="Type your answer..."
        value={value}
        onChange={(e) => setValue(e.target.value)}
        disabled={disabled}
      />
      <button
        type="submit"
        disabled={disabled || !value.trim()}
        className="rounded-full bg-black dark:bg-white text-white dark:text-black px-5 py-2 text-sm font-medium disabled:opacity-40"
      >
        Send
      </button>
    </form>
  );
}
