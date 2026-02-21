import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-6">
      <h1 className="text-4xl font-bold tracking-tight">Interview Simulator</h1>
      <p className="text-zinc-500 text-lg">Practice your interview skills with an AI interviewer.</p>
      <Link
        href="/interview"
        className="rounded-full bg-black text-white dark:bg-white dark:text-black px-8 py-3 text-sm font-medium hover:opacity-80 transition-opacity"
      >
        Start Interview
      </Link>
    </div>
  );
}
