"use client";

import { useState, useEffect, useCallback } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import DailyIframe, { DailyCall } from "@daily-co/daily-js";
import { DailyProvider, DailyAudio } from "@daily-co/daily-react";
import {
  prepareInterview,
  createConversation,
  createSession,
  pauseInterview,
  resumeInterview,
  endInterview,
} from "@/lib/api";
import type { InterviewReport as ReportType } from "@/lib/api";
import InterviewRoom from "@/components/InterviewRoom";
import InterviewReportCard from "@/components/InterviewReport";

type PageState =
  | "loading"
  | "intro"
  | "drawing"
  | "resuming"
  | "discussion"
  | "generating_report"
  | "report"
  | "ended"
  | "error";

// Destroy any lingering Daily instance before creating a fresh one.
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
  const [sessionId, setSessionId] = useState<string>("");
  const [callObject, setCallObject] = useState<DailyCall | null>(null);
  const [reportData, setReportData] = useState<ReportType | null>(null);

  // --- Init: prepare interview + create session + start first Tavus call ---
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

        // Create a session for phase tracking
        const taskDescription = preparation.cases
          .map((c) => JSON.stringify(c))
          .join("\n\n");
        const { session_id } = await createSession(
          preparation.system_prompt,
          taskDescription,
        );
        if (cancelled) return;
        setSessionId(session_id);
        console.log("[session] created", session_id);

        // Create first Tavus conversation
        const { conversation_id, conversation_url } = await createConversation(
          interviewType,
          preparation.system_prompt,
        );

        if (!cancelled) {
          setConversationUrl(conversation_url);
          setConversationId(conversation_id);
          setPageState("intro");
        }
      } catch (e) {
        if (!cancelled) {
          const msg = e instanceof Error ? e.message : "Something went wrong";
          console.error("[interview init]", msg);
          setError(msg);
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

  // --- Pause: stop Tavus, switch to drawing phase ---
  const handlePause = useCallback(async () => {
    try {
      // Destroy the Daily call object so video stops
      const instance = DailyIframe.getCallInstance();
      if (instance) {
        await instance.destroy().catch(() => {});
      }
      setCallObject(null);

      await pauseInterview(sessionId);
      setPageState("drawing");
    } catch (e) {
      console.error("[pause]", e);
      setPageState("drawing"); // Still transition even if API fails
    }
  }, [sessionId]);

  // --- Resume: analyze Miro board, start new Tavus call ---
  const handleResume = useCallback(async () => {
    setPageState("resuming");
    try {
      const co = await createFreshCallObject();
      setCallObject(co);

      const { conversation_id, conversation_url } = await resumeInterview(sessionId);
      setConversationId(conversation_id);
      setConversationUrl(conversation_url);
      setPageState("discussion");
    } catch (e) {
      const msg = e instanceof Error ? e.message : "Failed to resume";
      console.error("[resume]", msg);
      setError(msg);
      setPageState("error");
    }
  }, [sessionId]);

  // --- End interview: generate report ---
  const handleEnd = useCallback(async () => {
    // Destroy call object
    const instance = DailyIframe.getCallInstance();
    if (instance) {
      await instance.destroy().catch(() => {});
    }
    setCallObject(null);

    if (!sessionId) {
      setPageState("ended");
      return;
    }

    setPageState("generating_report");
    try {
      const report = await endInterview(sessionId);
      setReportData(report);
      setPageState("report");
    } catch (e) {
      console.error("[end interview]", e);
      // Still show ended state if report generation fails
      setPageState("ended");
    }
  }, [sessionId]);

  const label = interviewType === "system-design" ? "System Design" : "Coding";

  // --- Report view ---
  if (pageState === "report" && reportData) {
    return (
      <div className="min-h-screen bg-white">
        <InterviewReportCard
          report={reportData}
          onBackHome={() => router.push("/")}
        />
      </div>
    );
  }

  // --- Generating report spinner ---
  if (pageState === "generating_report") {
    return (
      <div className="flex flex-col items-center justify-center h-screen gap-4">
        <div className="w-12 h-12 border-4 border-zinc-600 border-t-white rounded-full animate-spin" />
        <p className="text-zinc-400 animate-pulse">
          Generating your interview report...
        </p>
      </div>
    );
  }

  // --- Ended (fallback, no report) ---
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

  // --- Error ---
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
        {pageState === "drawing" && (
          <span className="text-sm text-yellow-400 font-medium">
            Drawing Phase
          </span>
        )}
        {pageState === "discussion" && (
          <span className="text-sm text-green-400 font-medium">
            Discussion Phase
          </span>
        )}
      </header>

      <div className="flex-1 flex min-h-0">
        {/* Left side — Miro whiteboard */}
        <div className="w-1/2 border-r border-zinc-800">
          <iframe
            src="https://miro.com/app/live-embed/uXjVG8tjZTw=/?moveToViewport=-702,-392,1354,846&embedId=583364906355"
            className="w-full h-full border-0"
            allow="fullscreen; clipboard-read; clipboard-write"
            allowFullScreen
          />
        </div>

        {/* Right side — Interview room / Drawing phase / Resuming */}
        <div className="w-1/2 relative">
          {/* Loading */}
          {pageState === "loading" && (
            <div className="absolute inset-0 flex items-center justify-center">
              <p className="text-zinc-400 animate-pulse">
                Preparing your interview...
              </p>
            </div>
          )}

          {/* Intro phase: Tavus call with Pause button */}
          {pageState === "intro" && conversationUrl && callObject && (
            <DailyProvider callObject={callObject}>
              <DailyAudio />
              <InterviewRoom
                conversationUrl={conversationUrl}
                conversationId={conversationId}
                sessionId={sessionId}
                onEnd={handleEnd}
                onPause={handlePause}
              />
            </DailyProvider>
          )}

          {/* Drawing phase: no video, show instructions */}
          {pageState === "drawing" && (
            <div className="absolute inset-0 flex flex-col items-center justify-center gap-6 px-8">
              <div className="text-center space-y-3">
                <div className="w-16 h-16 mx-auto bg-yellow-600/20 rounded-full flex items-center justify-center">
                  <svg className="w-8 h-8 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                </div>
                <h2 className="text-xl font-semibold text-white">
                  Draw Your System Architecture
                </h2>
                <p className="text-zinc-400 max-w-md">
                  Use the Miro board on the left to draw your system design.
                  Include components, data flows, and any key decisions.
                  Click Resume when you&apos;re ready to discuss your design.
                </p>
              </div>
              <button
                onClick={handleResume}
                className="px-8 py-3 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700 transition text-lg"
              >
                Resume Interview
              </button>
            </div>
          )}

          {/* Resuming: loading state while Miro is analyzed */}
          {pageState === "resuming" && (
            <div className="absolute inset-0 flex flex-col items-center justify-center gap-4">
              <div className="w-12 h-12 border-4 border-zinc-600 border-t-green-400 rounded-full animate-spin" />
              <p className="text-zinc-400 animate-pulse text-center px-8">
                Analyzing your diagram and preparing discussion...
              </p>
            </div>
          )}

          {/* Discussion phase: Tavus call, no Pause button */}
          {pageState === "discussion" && conversationUrl && callObject && (
            <DailyProvider callObject={callObject}>
              <DailyAudio />
              <InterviewRoom
                conversationUrl={conversationUrl}
                conversationId={conversationId}
                sessionId={sessionId}
                onEnd={handleEnd}
              />
            </DailyProvider>
          )}
        </div>
      </div>
    </div>
  );
}
