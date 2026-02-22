"use client";

import { useState, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import DailyIframe, { DailyCall } from "@daily-co/daily-js";
import { DailyProvider, DailyAudio } from "@daily-co/daily-react";
import { prepareInterview, createConversation } from "@/lib/api";
import InterviewRoom from "@/components/InterviewRoom";

type PageState = "loading" | "active" | "ended" | "error";

// Destroy any lingering Daily instance before creating a fresh one.
// This handles React strict mode where the previous cleanup's async
// destroy() may not have completed yet.
async function createFreshCallObject(): Promise<DailyCall> {
  const existing = DailyIframe.getCallInstance();
  if (existing) {
    await existing.destroy();
  }
  return DailyIframe.createCallObject({
    audioSource: true,
    videoSource: true,
  });
}

export default function InterviewPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const interviewType = searchParams.get("type") ?? "coding";

  const [pageState, setPageState] = useState<PageState>("loading");
  const [error, setError] = useState<string>("");
  const [conversationUrl, setConversationUrl] = useState<string>("");
  const [conversationId, setConversationId] = useState<string>("");
  const [callObject, setCallObject] = useState<DailyCall | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function init() {
      try {
        const co = await createFreshCallObject();
        if (cancelled) {
          co.destroy().catch(() => {});
          return;
        }
        setCallObject(co);

        const taskType = interviewType === "system-design" ? "design" : "dsa";
        const preparation = await prepareInterview(taskType);
        console.log("[preparation] got system prompt and cases", preparation.cases.length);

        const { conversation_id, conversation_url } = await createConversation(
          interviewType,
          preparation.system_prompt,
        );

        if (!cancelled) {
          setConversationUrl(conversation_url);
          setConversationId(conversation_id);
          setPageState("active");
        }
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "Something went wrong");
          setPageState("error");
        }
      }
    }

    init();

    return () => {
      cancelled = true;
      const instance = DailyIframe.getCallInstance();
      if (instance) {
        instance.destroy().catch(() => {});
      }
    };
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
      </header>

      <div className="flex-1 flex min-h-0">
        {/* Left side — Miro whiteboard */}
        <div className="w-1/2 border-r border-zinc-800">
          <iframe
            src="https://miro.com/app/live-embed/uXjVG8tjZTw=/?moveToViewport=-698,-388,1354,846&embedId=236013957724"
            className="w-full h-full border-0"
            allow="fullscreen; clipboard-read; clipboard-write"
            allowFullScreen
          />
        </div>

        {/* Right side — Interview room */}
        <div className="w-1/2 relative">
          {pageState === "loading" && (
            <div className="absolute inset-0 flex items-center justify-center">
              <p className="text-zinc-400 animate-pulse">
                Preparing your interview...
              </p>
            </div>
          )}
          {pageState === "active" && conversationUrl && callObject && (
            <DailyProvider callObject={callObject}>
              <DailyAudio />
              <InterviewRoom
                conversationUrl={conversationUrl}
                conversationId={conversationId}
                onEnd={() => setPageState("ended")}
              />
            </DailyProvider>
          )}
        </div>
      </div>
    </div>
  );
}
