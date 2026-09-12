import type { HistorySummary } from "../../types/patient";
import { SectionLabel } from "../layout/SectionLabel";

interface Props {
  history: HistorySummary | null;
}

export function HistoryTable({ history }: Props) {
  if (!history || history.total === 0) return null;

  return (
    <div
      className="rounded-2xl border p-6"
      style={{ borderColor: "var(--border)", background: "var(--surface)" }}
    >
      <div className="mb-4 flex items-center justify-between">
        <SectionLabel>Recent predictions</SectionLabel>
        <span className="text-[11px]" style={{ color: "var(--text-muted)" }}>
          {history.total} total · {history.high_risk} flagged high risk
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-left text-[13px]">
          <thead>
            <tr style={{ color: "var(--text-muted)" }}>
              {["Time", "Age", "Sex", "Max HR", "Risk", "Result"].map((h) => (
                <th key={h} className="pb-2 pr-4 text-[11px] font-medium">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="font-[var(--font-mono)]">
            {history.recent.map((row, i) => (
              <tr
                key={i}
                className="border-t"
                style={{ borderColor: "var(--border)" }}
              >
                <td className="py-2 pr-4" style={{ color: "var(--text-muted)" }}>
                  {row.timestamp.split(" ")[1] ?? row.timestamp}
                </td>
                <td className="py-2 pr-4" style={{ color: "var(--text)" }}>
                  {row.age}
                </td>
                <td className="py-2 pr-4" style={{ color: "var(--text)" }}>
                  {row.sex}
                </td>
                <td className="py-2 pr-4" style={{ color: "var(--text)" }}>
                  {row.max_hr}
                </td>
                <td className="py-2 pr-4" style={{ color: "var(--text)" }}>
                  {(row.probability * 100).toFixed(1)}%
                </td>
                <td
                  className="py-2 pr-4 font-semibold"
                  style={{
                    color:
                      row.risk_label === "High Risk"
                        ? "var(--pulse)"
                        : "var(--signal)",
                  }}
                >
                  {row.risk_label}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
