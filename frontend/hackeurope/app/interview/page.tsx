"use client";

import { useState, useEffect, useRef } from "react";
import { useSearchParams } from "next/navigation";
import ChatWindow from "@/components/ChatWindow";
import MessageInput from "@/components/MessageInput";
import { sendMessage, type Message } from "@/lib/api";

export default function InterviewPage() {
  const searchParams = useSearchParams();
  const interviewType = searchParams.get("type") ?? "coding";

  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  // Kick off the interview when the page loads
  useEffect(() => {
    async function startInterview() {
      setLoading(true);
      try {
        const reply = await sendMessage([], interviewType);
        setMessages([{ role: "assistant", content: reply }]);
      } finally {
        setLoading(false);
      }
    }
    startInterview();
  }, [interviewType]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend(text: string) {
    const updated: Message[] = [...messages, { role: "user", content: text }];
    setMessages(updated);
    setLoading(true);
    try {
      const reply = await sendMessage(updated, interviewType);
      setMessages([...updated, { role: "assistant", content: reply }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto px-4 py-6">
      <h1 className="text-xl font-semibold mb-4">Mock Interview</h1>
      <ChatWindow messages={messages} />
      {loading && (
        <p className="text-xs text-zinc-400 py-2">Interviewer is typing...</p>
      )}
      <div ref={bottomRef} />
      <MessageInput onSend={handleSend} disabled={loading} />
    </div>
  );
}
