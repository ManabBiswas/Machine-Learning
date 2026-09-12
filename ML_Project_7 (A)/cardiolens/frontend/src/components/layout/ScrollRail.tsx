import { motion } from "framer-motion";
import { useScrollProgress } from "../../hooks/useScrollProgress";

const RAIL_HEIGHT = 240;

function tintFor(progress: number) {
  if (progress > 0.66) return "var(--pulse)";
  if (progress > 0.33) return "var(--caution)";
  return "var(--signal)";
}

export function ScrollRail() {
  const progress = useScrollProgress();
  const color = tintFor(progress);

  return (
    <>
      {/* Mobile: thin top progress bar */}
      <div
        className="fixed left-0 right-0 top-0 z-50 h-[2px] sm:hidden"
        style={{ background: "var(--border)" }}
      >
        <motion.div
          className="h-full"
          style={{ background: color, width: `${progress * 100}%` }}
          transition={{ ease: "linear", duration: 0.1 }}
        />
      </div>

      {/* Desktop: vertical trace, fixed to viewport edge */}
      <div
        className="fixed left-5 top-1/2 z-40 hidden -translate-y-1/2 sm:block"
        aria-hidden="true"
      >
        <svg width="16" height={RAIL_HEIGHT} viewBox={`0 0 16 ${RAIL_HEIGHT}`}>
          <line
            x1="8"
            y1="0"
            x2="8"
            y2={RAIL_HEIGHT}
            stroke="var(--border)"
            strokeWidth="2"
            strokeLinecap="round"
          />
          <motion.line
            x1="8"
            y1="0"
            x2="8"
            y2={RAIL_HEIGHT}
            stroke={color}
            strokeWidth="2"
            strokeLinecap="round"
            style={{
              pathLength: progress,
              filter: `drop-shadow(0 0 4px ${color})`,
            }}
            transition={{ ease: [0.34, 1.4, 0.4, 1], duration: 0.4 }}
          />
          <motion.circle
            cx="8"
            r="4"
            fill={color}
            style={{ filter: `drop-shadow(0 0 6px ${color})` }}
            animate={{ cy: progress * RAIL_HEIGHT }}
            transition={{ ease: [0.34, 1.4, 0.4, 1], duration: 0.4 }}
          />
        </svg>
      </div>
    </>
  );
}
