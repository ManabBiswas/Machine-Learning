import { motion, useMotionValue, animate, useInView } from "framer-motion";
import { useEffect, useRef, useState } from "react";
import type { Metrics } from "../../types/patient";

interface Props {
  metrics: Metrics | null;
}

function CountUp({ target, suffix = "" }: { target: number; suffix?: string }) {
  const ref = useRef<HTMLSpanElement>(null);
  const inView = useInView(ref, { once: true, margin: "-40px" });
  const [display, setDisplay] = useState(0);
  const mv = useMotionValue(0);

  useEffect(() => {
    if (!inView) return;
    const controls = animate(mv, target, {
      duration: 1.4,
      ease: [0.16, 1, 0.3, 1],
      onUpdate: (v) => setDisplay(v),
    });
    return () => controls.stop();
  }, [inView, target, mv]);

  return (
    <span ref={ref} className="font-[var(--font-mono)] tabular-nums">
      {display.toFixed(1)}
      {suffix}
    </span>
  );
}

export function StatShowcase({ metrics }: Props) {
  const items = [
    { label: "Accuracy", value: metrics ? metrics.accuracy * 100 : 0, suffix: "%" },
    { label: "F1 score", value: metrics ? metrics.f1 * 100 : 0, suffix: "%" },
  ];

  return (
    <section className="mx-auto max-w-4xl px-6 py-20 text-center">
      <motion.h2
        initial={{ opacity: 0, y: 12 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-80px" }}
        transition={{ duration: 0.5 }}
        className="mb-3 font-[var(--font-display)] text-2xl font-bold"
        style={{ color: "var(--text)" }}
      >
        Honest about its own accuracy
      </motion.h2>
      <p className="mx-auto mb-12 max-w-md text-sm" style={{ color: "var(--text-muted)" }}>
        Measured on a held-out test split — not tuned to look better than it
        performs.
      </p>

      <div className="flex justify-center gap-16">
        {items.map((item) => (
          <div key={item.label}>
            <div className="text-5xl font-semibold" style={{ color: "var(--signal)" }}>
              <CountUp target={item.value} suffix={item.suffix} />
            </div>
            <div className="mt-2 text-xs" style={{ color: "var(--text-muted)" }}>
              {item.label}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
