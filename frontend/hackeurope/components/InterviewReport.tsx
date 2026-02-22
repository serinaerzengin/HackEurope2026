"use client";

import type { InterviewReport as ReportType } from "@/lib/api";

type Props = {
  report: ReportType;
  onBackHome: () => void;
};

function ScoreBar({ label, score }: { label: string; score: number }) {
  const pct = (score / 10) * 100;
  const color =
    score >= 7 ? "bg-green-500" : score >= 4 ? "bg-yellow-500" : "bg-red-500";

  return (
    <div className="space-y-1">
      <div className="flex justify-between text-sm">
        <span className="text-zinc-600">{label}</span>
        <span className="font-semibold text-zinc-900">{score.toFixed(1)}/10</span>
      </div>
      <div className="h-2 bg-zinc-200 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all ${color}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

function scoreColor(score: number): string {
  if (score >= 7) return "text-green-600";
  if (score >= 4) return "text-yellow-600";
  return "text-red-600";
}

export default function InterviewReportCard({ report, onBackHome }: Props) {
  return (
    <div className="max-w-2xl mx-auto py-10 px-6 space-y-8">
      {/* Overall score */}
      <div className="text-center space-y-2">
        <h1 className="text-2xl font-bold text-zinc-900">Interview Report</h1>
        <p
          className={`text-6xl font-extrabold ${scoreColor(report.overall_score)}`}
        >
          {report.overall_score.toFixed(1)}
        </p>
        <p className="text-zinc-500 text-sm">Overall Score / 10</p>
      </div>

      {/* Score bars */}
      <div className="space-y-4">
        <ScoreBar label="Communication" score={report.communication_score} />
        <ScoreBar label="Technical" score={report.technical_score} />
      </div>

      {/* Strengths */}
      <div>
        <h2 className="text-lg font-semibold text-green-600 mb-2">Strengths</h2>
        <ul className="space-y-1">
          {report.strengths.map((s, i) => (
            <li key={i} className="text-zinc-700 text-sm flex gap-2">
              <span className="text-green-600 shrink-0">+</span>
              {s}
            </li>
          ))}
        </ul>
      </div>

      {/* Weaknesses */}
      <div>
        <h2 className="text-lg font-semibold text-red-600 mb-2">
          Areas for Improvement
        </h2>
        <ul className="space-y-1">
          {report.weaknesses.map((w, i) => (
            <li key={i} className="text-zinc-700 text-sm flex gap-2">
              <span className="text-red-600 shrink-0">-</span>
              {w}
            </li>
          ))}
        </ul>
      </div>

      {/* Diagram feedback */}
      {report.diagram_feedback && (
        <div>
          <h2 className="text-lg font-semibold text-blue-600 mb-2">
            Diagram Feedback
          </h2>
          <p className="text-zinc-700 text-sm leading-relaxed">
            {report.diagram_feedback}
          </p>
        </div>
      )}

      {/* Detailed feedback */}
      <div>
        <h2 className="text-lg font-semibold text-zinc-800 mb-2">
          Detailed Feedback
        </h2>
        <p className="text-zinc-600 text-sm leading-relaxed whitespace-pre-wrap">
          {report.detailed_feedback}
        </p>
      </div>

      {/* Back button */}
      <div className="flex justify-center pt-4">
        <button
          onClick={onBackHome}
          className="px-8 py-3 bg-zinc-900 text-white rounded-lg font-medium hover:bg-zinc-700 transition"
        >
          Back to Home
        </button>
      </div>
    </div>
  );
}
