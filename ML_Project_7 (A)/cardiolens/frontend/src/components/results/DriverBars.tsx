import { motion } from "framer-motion";
import type { Driver } from "../../types/patient";

interface Props {
  drivers: Driver[];
}

export function DriverBars({ drivers }: Props) {
  const maxAbs = Math.max(...drivers.map((d) => Math.abs(d.value)), 0.01);

  return (
    <div className="flex flex-col gap-2.5">
      {drivers.map((d, i) => {
        const widthPct = (Math.abs(d.value) / maxAbs) * 50;
        const positive = d.value >= 0;
        return (
          <div key={d.feature} className="flex items-center gap-3">
            <span
              className="w-28 shrink-0 text-right text-[12px]"
              style={{ color: "var(--text-muted)" }}
            >
              {d.label}
            </span>
            <div className="relative h-5 flex-1">
              <div
                className="absolute left-1/2 top-0 h-full w-px"
                style={{ background: "var(--border-strong)" }}
              />
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${widthPct}%` }}
                transition={{ duration: 0.6, delay: i * 0.05, ease: "easeOut" }}
                className="absolute top-0.5 h-4 rounded-sm"
                style={{
                  [positive ? "left" : "right"]: "50%",
                  background: positive ? "var(--pulse)" : "var(--signal)",
                }}
              />
            </div>
          </div>
        );
      })}
      <div className="mt-1 flex items-center justify-center gap-4 text-[11px]" style={{ color: "var(--text-muted)" }}>
        <span className="flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-sm" style={{ background: "var(--pulse)" }} />
          Increases risk
        </span>
        <span className="flex items-center gap-1.5">
          <span className="h-2 w-2 rounded-sm" style={{ background: "var(--signal)" }} />
          Lowers risk
        </span>
      </div>
    </div>
  );
}
