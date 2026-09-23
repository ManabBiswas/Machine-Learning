import { motion } from "framer-motion";

export function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-16 text-center">
      <svg width="180" height="60" viewBox="0 0 180 60" fill="none">
        <motion.path
          d="M0 30 L40 30 L52 8 L64 52 L76 18 L84 30 L180 30"
          stroke="var(--signal)"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
          initial={{ pathLength: 0, opacity: 0.3 }}
          animate={{ pathLength: 1, opacity: 1 }}
          transition={{ duration: 2.2, repeat: Infinity, ease: "easeInOut" }}
        />
      </svg>
      <p className="max-w-[260px] text-sm" style={{ color: "var(--text-muted)" }}>
        Fill in the patient panel and run a prediction to see the risk
        breakdown here.
      </p>
    </div>
  );
}
