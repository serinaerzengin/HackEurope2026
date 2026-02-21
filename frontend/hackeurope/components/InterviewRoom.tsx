"use client";

import { useEffect, useCallback } from "react";
import { DailyVideo, useParticipantIds, useLocalSessionId } from "@daily-co/daily-react";
import { useCVICall } from "@/hooks/use-cvi-call";
import { useObservableEvent, useSendAppMessage } from "@/hooks/cvi-events-hooks";
import { sendUtterance } from "@/lib/api";

type InterviewRoomProps = {
  conversationUrl: string;
  conversationId: string;
  onEnd: () => void;
};

export default function InterviewRoom({
  conversationUrl,
  conversationId,
  onEnd,
}: InterviewRoomProps) {
  const { joinCall, leaveCall } = useCVICall();
  const sendMessage = useSendAppMessage();
  const localSessionId = useLocalSessionId();
  const remoteParticipantIds = useParticipantIds({ filter: "remote" });

  useEffect(() => {
    joinCall({ url: conversationUrl });
  }, [conversationUrl, joinCall]);

  const handleEvent = useCallback(
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    async (event: any) => {
      if (event.event_type !== "conversation.utterance") return;

      const { role, speech } = event.properties;
      console.log(`[utterance] role=${role} speech="${speech}"`);

      // Only process user utterances — send to backend for a response
      if (role === "user" && speech.trim()) {
        try {
          const result = await sendUtterance(speech, role, conversationId);
          console.log("[backend response]", result.response);

          // Echo the backend response through the Tavus avatar
          sendMessage({
            message_type: "conversation",
            event_type: "conversation.echo",
            conversation_id: conversationId,
            properties: {
              modality: "text",
              text: result.response,
              done: true,
            },
          });
        } catch (err) {
          console.error("[utterance error]", err);
        }
      }
    },
    [conversationId, sendMessage],
  );

  useObservableEvent(handleEvent);

  const handleEnd = useCallback(async () => {
    await leaveCall();
    onEnd();
  }, [leaveCall, onEnd]);

  const replicaId = remoteParticipantIds[0];

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 relative bg-zinc-900 rounded-xl overflow-hidden">
        {replicaId ? (
          <DailyVideo
            sessionId={replicaId}
            type="video"
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center">
            <p className="text-zinc-400 animate-pulse">
              Connecting to interviewer...
            </p>
          </div>
        )}

        {/* Local video (picture-in-picture) */}
        {localSessionId && (
          <div className="absolute bottom-4 right-4 w-48 h-36 rounded-lg overflow-hidden border-2 border-zinc-700 bg-zinc-800">
            <DailyVideo
              sessionId={localSessionId}
              type="video"
              mirror
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
            />
          </div>
        )}
      </div>

      <div className="flex justify-center py-4">
        <button
          onClick={handleEnd}
          className="px-6 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 transition"
        >
          End Interview
        </button>
      </div>
    </div>
  );
}
