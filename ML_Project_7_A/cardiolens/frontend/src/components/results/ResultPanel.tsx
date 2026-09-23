import { AnimatePresence, motion } from "framer-motion";
import type { PredictionResponse } from "../../types/patient";
import { RiskGauge } from "./RiskGauge";
import { DriverBars } from "./DriverBars";
import { EmptyState } from "./EmptyState";
import { SectionLabel } from "../layout/SectionLabel";

interface Props {
  result: PredictionResponse | null;
  loading: boolean;
  error: string | null;
}

export function ResultPanel({ result, loading, error }: Props) {
  return (
    <div
      className="sticky top-6 flex flex-col gap-6 rounded-2xl border p-6"
      style={{
        borderColor: "var(--border)",
        background: "var(--surface)",
        boxShadow: "var(--shadow-ambient)",
      }}
    >
      <SectionLabel>Risk assessment</SectionLabel>

      <AnimatePresence mode="wait">
        {error ? (
          <motion.div
            key="error"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="rounded-lg border px-4 py-3 text-sm"
            style={{
              borderColor: "var(--pulse)",
              background: "var(--pulse-soft)",
              color: "var(--pulse)",
            }}
          >
            {error}
          </motion.div>
        ) : loading ? (
          <motion.div
            key="loading"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex flex-col items-center gap-3 py-16"
          >
            <motion.span
              className="h-10 w-10 rounded-full border-2 border-t-transparent"
              style={{ borderColor: "var(--signal)", borderTopColor: "transparent" }}
              animate={{ rotate: 360 }}
              transition={{ duration: 0.9, repeat: Infinity, ease: "linear" }}
            />
            <span className="text-sm" style={{ color: "var(--text-muted)" }}>
              Running inference…
            </span>
          </motion.div>
        ) : result ? (
          <motion.div
            key="result"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="flex flex-col gap-6"
          >
            <RiskGauge probability={result.probability} tier={result.risk_tier} />
            <div>
              <p
                className="mb-3 text-center text-[12px] font-medium"
                style={{ color: "var(--text-muted)" }}
              >
                Top contributing factors
              </p>
              <DriverBars drivers={result.drivers} />
            </div>
            <p
              className="text-center text-[11px]"
              style={{ color: "var(--text-muted)" }}
            >
              Evaluated {result.timestamp} · not a clinical diagnosis
            </p>
          </motion.div>
        ) : (
          <motion.div key="empty" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <EmptyState />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
