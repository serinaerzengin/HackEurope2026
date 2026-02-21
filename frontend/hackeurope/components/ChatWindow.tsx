import { Message } from "@/lib/api";

type Props = {
  messages: Message[];
};

export default function ChatWindow({ messages }: Props) {
  return (
    <div className="flex flex-col gap-4 overflow-y-auto flex-1 py-4">
      {messages.map((msg, i) => (
        <div
          key={i}
          className={`max-w-xl px-4 py-3 rounded-2xl text-sm leading-relaxed ${
            msg.role === "assistant"
              ? "self-start bg-zinc-100 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100"
              : "self-end bg-black text-white dark:bg-white dark:text-black"
          }`}
        >
          {msg.content}
        </div>
      ))}
    </div>
  );
}
