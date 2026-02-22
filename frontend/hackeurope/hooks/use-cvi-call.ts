'use client';

import { useDaily } from "@daily-co/daily-react";
import { useCallback } from "react";

export function useCVICall() {
  const daily = useDaily();

  const joinCall = useCallback(
    async ({ url }: { url: string }) => {
      if (!daily) return;
      await daily.join({ url });
    },
    [daily],
  );

  const leaveCall = useCallback(async () => {
    if (!daily) return;
    await daily.leave();
  }, [daily]);

  return { joinCall, leaveCall };
}
