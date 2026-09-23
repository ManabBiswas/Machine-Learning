import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { cardiolensApi } from "../api/cardiolens";
import { HistoryTable } from "../components/history/HistoryTable";
import { TiltCard } from "../components/interaction/TiltCard";
import type { HistorySummary } from "../types/patient";

function SummaryCard({
  label,
  value,
  accent,
}: {
  label: string;
  value: string;
  accent?: string;
}) {
  return (
    <TiltCard
      className="rounded-2xl border p-6"
      style={{ borderColor: "var(--border)", background: "var(--surface)" }}
    >
      <span className="text-xs font-medium" style={{ color: "var(--text-muted)" }}>
        {label}
      </span>
      <div
        className="mt-2 font-[var(--font-mono)] text-3xl font-semibold"
        style={{ color: accent ?? "var(--text)" }}
      >
        {value}
      </div>
    </TiltCard>
  );
}

export default function Insights() {
  const [history, setHistory] = useState<HistorySummary | null>(null);

  useEffect(() => {
    cardiolensApi
      .history(20)
      .then(setHistory)
      .catch(() => setHistory(null));
  }, []);

  return (
    <div className="mx-auto max-w-5xl px-6 pb-20 pt-10">
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <h1
          className="font-[var(--font-display)] text-2xl font-bold"
          style={{ color: "var(--text)" }}
        >
          Insights
        </h1>
        <p className="mt-1 max-w-xl text-sm" style={{ color: "var(--text-muted)" }}>
          A running view of every assessment run through the tool this
          session.
        </p>
      </motion.div>

      <div className="my-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
        <SummaryCard label="Total assessments" value={String(history?.total ?? 0)} />
        <SummaryCard
          label="Flagged high risk"
          value={String(history?.high_risk ?? 0)}
          accent="var(--pulse)"
        />
        <SummaryCard
          label="Average risk"
          value={history ? `${(history.avg_risk * 100).toFixed(1)}%` : "0%"}
          accent="var(--caution)"
        />
      </div>

      <HistoryTable history={history} />

      {(!history || history.total === 0) && (
        <p className="mt-6 text-center text-sm" style={{ color: "var(--text-muted)" }}>
          No assessments yet — run one on the{" "}
          <a href="/assess" className="underline" style={{ color: "var(--signal)" }}>
            Assess
          </a>{" "}
          page to see it here.
        </p>
      )}
    </div>
  );
}
