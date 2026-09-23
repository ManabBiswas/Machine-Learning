import { useEffect, useState } from "react";
import { motion, useMotionValue, animate } from "framer-motion";
import type { RiskTier } from "../../types/patient";

interface Props {
  probability: number;
  tier: RiskTier;
}

const TIER_COLOR: Record<RiskTier, string> = {
  low: "var(--signal)",
  moderate: "var(--caution)",
  high: "var(--pulse)",
};

const TIER_LABEL: Record<RiskTier, string> = {
  low: "Low risk",
  moderate: "Moderate risk",
  high: "High risk",
};

const RADIUS = 82;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

export function RiskGauge({ probability, tier }: Props) {
  const pct = Math.min(Math.max(probability, 0), 1);
  const color = TIER_COLOR[tier];
  const [display, setDisplay] = useState(0);
  const motionVal = useMotionValue(0);

  useEffect(() => {
    const controls = animate(motionVal, pct * 100, {
      duration: 1.2,
      ease: [0.16, 1, 0.3, 1],
      onUpdate: (v) => setDisplay(v),
    });
    return () => controls.stop();
  }, [pct, motionVal]);

  return (
    <div className="flex flex-col items-center">
      <div className="relative h-[200px] w-[200px]">
        <svg viewBox="0 0 200 200" className="h-full w-full -rotate-90">
          <circle
            cx="100"
            cy="100"
            r={RADIUS}
            fill="none"
            stroke="var(--border)"
            strokeWidth="13"
          />
          <motion.circle
            cx="100"
            cy="100"
            r={RADIUS}
            fill="none"
            stroke={color}
            strokeWidth="13"
            strokeLinecap="round"
            strokeDasharray={CIRCUMFERENCE}
            strokeDashoffset={CIRCUMFERENCE - (display / 100) * CIRCUMFERENCE}
            style={{ filter: `drop-shadow(0 0 8px ${color})` }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span
            className="font-[var(--font-mono)] text-4xl font-semibold tabular-nums"
            style={{ color: "var(--text)" }}
          >
            {display.toFixed(1)}%
          </span>
          <span
            className="mt-1 text-[11px] font-medium tracking-wide"
            style={{ color: "var(--text-muted)" }}
          >
            Predicted risk
          </span>
          <span
            className="mt-1 text-xs font-semibold"
            style={{ color }}
          >
            {TIER_LABEL[tier]}
          </span>
        </div>
      </div>
    </div>
  );
}
