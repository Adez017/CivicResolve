"use client";

import { useRouter } from "next/navigation";

export default function FeedbackToggle() {
  const router = useRouter();

  return (
    <button
      onClick={() => router.push("/feedback")}
      className="
        fixed bottom-6 right-6
        bg-gradient-to-r from-purple-500 to-pink-500
        text-white
        px-5 py-3
        rounded-full
        shadow-lg
        hover:scale-110
        hover:shadow-purple-500/50
        transition-all duration-300
        z-50
      "
    >
      💬 Feedback
    </button>
  );
}
