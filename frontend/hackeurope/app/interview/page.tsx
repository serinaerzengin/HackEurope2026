"use client";

import { useState, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { createConversation } from "@/lib/api";

type PageState = "loading" | "active" | "ended" | "error";

export default function InterviewPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const interviewType = searchParams.get("type") ?? "coding";

  const [pageState, setPageState] = useState<PageState>("loading");
  const [error, setError] = useState<string>("");
  const [conversationUrl, setConversationUrl] = useState<string>("");

  useEffect(() => {
    let cancelled = false;

    async function start() {
      try {
        const { conversation_url } = await createConversation(interviewType);
        if (!cancelled) {
          setConversationUrl(conversation_url);
          setPageState("active");
        }
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "Something went wrong");
          setPageState("error");
        }
      }
    }

    start();
    return () => { cancelled = true; };
  }, [interviewType]);

  const label = interviewType === "system-design" ? "System Design" : "Coding";

  if (pageState === "ended") {
    return (
      <div className="flex flex-col items-center justify-center h-screen gap-4">
        <h1 className="text-2xl font-semibold">Interview Ended</h1>
        <p className="text-zinc-400">Thanks for practicing!</p>
        <button
          onClick={() => router.push("/")}
          className="px-6 py-2 bg-white text-black rounded-lg font-medium hover:bg-zinc-200 transition"
        >
          Back to Home
        </button>
      </div>
    );
  }

  if (pageState === "error") {
    return (
      <div className="flex flex-col items-center justify-center h-screen gap-4">
        <h1 className="text-2xl font-semibold text-red-400">Error</h1>
        <p className="text-zinc-400">{error}</p>
        <button
          onClick={() => router.push("/")}
          className="px-6 py-2 bg-white text-black rounded-lg font-medium hover:bg-zinc-200 transition"
        >
          Back to Home
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen">
      <header className="flex items-center justify-between px-6 py-4 border-b border-zinc-800">
        <h1 className="text-lg font-semibold">{label} Interview</h1>
        <button
          onClick={() => setPageState("ended")}
          className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 transition"
        >
          End Interview
        </button>
      </header>

      <div className="flex-1 relative">
        {pageState === "loading" && (
          <div className="absolute inset-0 flex items-center justify-center">
            <p className="text-zinc-400 animate-pulse">
              Setting up your interview...
            </p>
          </div>
        )}
        {conversationUrl && (
          <iframe
            src={conversationUrl}
            allow="camera; microphone; autoplay; display-capture"
            className="w-full h-full border-0 rounded-xl"
          />
        )}
      </div>
    </div>
  );
}
