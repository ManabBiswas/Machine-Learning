import { motion } from "framer-motion";

const STEPS = [
  {
    n: "01",
    title: "Enter vitals",
    body: "Age, blood pressure, cholesterol, ECG readings, and a handful of other routine clinical measurements — the same inputs a cardiologist would look at.",
  },
  {
    n: "02",
    title: "Model infers",
    body: "A logistic regression model trained on the UCI Heart Disease dataset estimates the probability of disease from those inputs in real time.",
  },
  {
    n: "03",
    title: "See what drove it",
    body: "Every prediction ships with the top contributing factors, so the number is never a black box — you can see exactly why.",
  },
];

export function HowItWorks() {
  return (
    <section className="mx-auto max-w-5xl px-6 py-20">
      <motion.h2
        initial={{ opacity: 0, y: 12 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-80px" }}
        transition={{ duration: 0.5 }}
        className="mb-12 text-center font-[var(--font-display)] text-2xl font-bold"
        style={{ color: "var(--text)" }}
      >
        How it works
      </motion.h2>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
        {STEPS.map((step, i) => (
          <motion.div
            key={step.n}
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-60px" }}
            transition={{ duration: 0.5, delay: i * 0.08 }}
            className="rounded-2xl border p-6"
            style={{ borderColor: "var(--border)", background: "var(--surface)" }}
          >
            <span
              className="font-[var(--font-mono)] text-xs font-medium"
              style={{ color: "var(--signal)" }}
            >
              {step.n}
            </span>
            <h3
              className="mt-2 font-[var(--font-display)] text-lg font-semibold"
              style={{ color: "var(--text)" }}
            >
              {step.title}
            </h3>
            <p className="mt-2 text-sm leading-relaxed" style={{ color: "var(--text-muted)" }}>
              {step.body}
            </p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
