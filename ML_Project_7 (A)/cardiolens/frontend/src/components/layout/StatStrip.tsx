import type { Metrics } from "../../types/patient";

interface Props {
  metrics: Metrics | null;
}

function Stat({
  label,
  value,
  hint,
}: {
  label: string;
  value: string;
  hint: string;
}) {
  return (
    <div className="flex flex-1 flex-col gap-0.5 px-5 py-3 first:pl-0 last:pr-0">
      <span
        className="text-[11px] font-medium"
        style={{ color: "var(--text-muted)" }}
      >
        {label}
      </span>
      <span
        className="font-[var(--font-mono)] text-xl font-semibold"
        style={{ color: "var(--text)" }}
      >
        {value}
      </span>
      <span className="text-[11px]" style={{ color: "var(--text-muted)" }}>
        {hint}
      </span>
    </div>
  );
}

export function StatStrip({ metrics }: Props) {
  return (
    <div
      className="flex divide-x rounded-xl border px-1"
      style={{ borderColor: "var(--border)", background: "var(--surface)" }}
    >
      <Stat
        label="Accuracy"
        value={metrics ? `${(metrics.accuracy * 100).toFixed(1)}%` : "—"}
        hint="Holdout test set"
      />
      <Stat
        label="F1 score"
        value={metrics ? `${(metrics.f1 * 100).toFixed(1)}%` : "—"}
        hint="Precision / recall balance"
      />
      <Stat
        label="Model"
        value={metrics?.model ?? "—"}
        hint={metrics ? `v${metrics.model_version} · fully interpretable` : ""}
      />
    </div>
  );
}
