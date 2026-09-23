import { motion, useMotionValue, animate } from "framer-motion";
import { useEffect, useState } from "react";
import { MagneticButton } from "../interaction/MagneticButton";
import { useNavigate } from "react-router-dom";

// Anatomical-ish silhouette (stylized, single continuous path)
const HEART_PATH =
  "M100 176 C40 132 12 96 12 62 C12 34 34 14 60 14 C78 14 92 24 100 40 C108 24 122 14 140 14 C166 14 188 34 188 62 C188 96 160 132 100 176 Z";

const COLORS = ["var(--signal)", "var(--caution)", "var(--pulse)"];

export function Hero() {
  const navigate = useNavigate();
  const [colorIdx, setColorIdx] = useState(0);
  const beat = useMotionValue(1);

  useEffect(() => {
    // lub-DUB: quick contraction, hold, slower release, rest
    const sequence = async () => {
      while (true) {
        await animate(beat, 1.08, { duration: 0.12, ease: [0.34, 1.4, 0.4, 1] }).finished;
        await animate(beat, 0.98, { duration: 0.1, ease: "easeIn" }).finished;
        await animate(beat, 1.05, { duration: 0.14, ease: [0.34, 1.4, 0.4, 1] }).finished;
        await animate(beat, 1, { duration: 0.5, ease: "easeOut" }).finished;
        await new Promise((r) => setTimeout(r, 700));
      }
    };
    const controls = sequence();
    return () => {
      controls.catch(() => {});
    };
  }, [beat]);

  useEffect(() => {
    const id = setInterval(() => setColorIdx((i) => (i + 1) % COLORS.length), 3200);
    return () => clearInterval(id);
  }, []);

  return (
    <section className="mx-auto flex max-w-4xl flex-col items-center px-6 pb-20 pt-16 text-center sm:pt-24">
      <motion.div style={{ scale: beat }} className="relative mb-8 h-[200px] w-[200px]">
        <svg viewBox="0 0 200 190" className="h-full w-full overflow-visible">
          <defs>
            <filter id="heroGlow" x="-60%" y="-60%" width="220%" height="220%">
              <feGaussianBlur stdDeviation="10" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>
          <motion.path
            d={HEART_PATH}
            fill="none"
            strokeWidth="3.5"
            strokeLinecap="round"
            strokeLinejoin="round"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{
              pathLength: 1,
              opacity: 1,
              stroke: COLORS[colorIdx],
            }}
            transition={{
              pathLength: { duration: 2, ease: [0.16, 1, 0.3, 1] },
              opacity: { duration: 0.6 },
              stroke: { duration: 1.2, ease: "easeInOut" },
            }}
            style={{ filter: "url(#heroGlow)" }}
          />
        </svg>
      </motion.div>

      <motion.h1
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.6 }}
        className="max-w-2xl font-[var(--font-display)] text-4xl font-bold leading-tight sm:text-5xl"
        style={{ color: "var(--text)" }}
      >
        Explainable heart disease risk, from routine vitals.
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.55, duration: 0.6 }}
        className="mt-4 max-w-xl text-base"
        style={{ color: "var(--text-muted)" }}
      >
        CardioLens runs an interpretable logistic regression model against
        standard clinical measurements and shows exactly which factors moved
        the number — no black box.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7, duration: 0.6 }}
        className="mt-8"
      >
        <MagneticButton
          onClick={() => navigate("/assess")}
          className="rounded-full px-7 py-3 font-[var(--font-display)] text-sm font-semibold"
          style={{ background: "var(--signal)", color: "#04110f" }}
        >
          Run an assessment
        </MagneticButton>
      </motion.div>
    </section>
  );
}
