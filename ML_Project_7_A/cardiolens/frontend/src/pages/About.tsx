import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { cardiolensApi } from "../api/cardiolens";
import { GlowPanel } from "../components/interaction/GlowPanel";
import type { Metrics } from "../types/patient";

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 12 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-60px" }}
      transition={{ duration: 0.5 }}
      className="mb-10"
    >
      <h2
        className="mb-3 font-[var(--font-display)] text-lg font-semibold"
        style={{ color: "var(--text)" }}
      >
        {title}
      </h2>
      <div className="space-y-3 text-sm leading-relaxed" style={{ color: "var(--text-muted)" }}>
        {children}
      </div>
    </motion.section>
  );
}

export default function About() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);

  useEffect(() => {
    cardiolensApi
      .metrics()
      .then(setMetrics)
      .catch(() => setMetrics(null));
  }, []);

  return (
    <div className="mx-auto max-w-3xl px-6 pb-20 pt-10">
      <h1
        className="mb-8 font-[var(--font-display)] text-2xl font-bold"
        style={{ color: "var(--text)" }}
      >
        About CardioLens
      </h1>

      <Section title="The model">
        <p>
          A {metrics?.model ?? "logistic regression"} classifier trained on
          the UCI Heart Disease dataset (302 patients after deduplication),
          using standard clinical measurements: age, sex, chest pain type,
          resting blood pressure, cholesterol, fasting blood sugar, resting
          ECG, max heart rate, exercise-induced angina, ST depression
          (oldpeak), ST slope, number of major vessels, and thalassemia.
        </p>
        <p>
          Held-out test performance: {metrics ? `${(metrics.accuracy * 100).toFixed(1)}% accuracy, ${(metrics.f1 * 100).toFixed(1)}% F1 score` : "loading…"}.
        </p>
      </Section>

      <Section title="A bug worth documenting">
        <p>
          This dataset's release ships with an inverted target label —{" "}
          <code>target = 1</code> actually means <em>no disease</em>, and{" "}
          <code>target = 0</code> means disease is present, backwards from
          the assumption nearly every public notebook on this dataset makes.
        </p>
        <p>
          It surfaced when a clearly high-risk clinical profile (elevated ST
          depression, exercise-induced angina, multiple affected vessels)
          came back as "2.4% — low risk." Grouping the raw data by the
          target column confirmed it: the group labeled{" "}
          <code>1</code> had the healthier clinical profile — younger, higher
          max heart rate, lower ST depression — the opposite of what the
          label name implies.
        </p>
        <p>
          The fix was a one-line relabel before training, not a change to
          the model or preprocessing logic — both were correct all along.
          All three project notebooks now document and reflect this.
        </p>
      </Section>

      <Section title="Limitations">
        <ul className="list-disc space-y-2 pl-5">
          <li>Trained on 302 records — small by clinical ML standards.</li>
          <li>
            The source population may not represent every demographic;
            treat outputs as illustrative, not diagnostic.
          </li>
          <li>
            Logistic regression was chosen for interpretability over raw
            accuracy — the driver breakdown is a direct readout of the
            model's coefficients, not a post-hoc explanation.
          </li>
        </ul>
      </Section>

      <GlowPanel className="p-6">
        <p className="text-sm" style={{ color: "var(--text-muted)" }}>
          This is a portfolio project, not a certified medical device. It
          does not diagnose, and it should never replace a conversation
          with a clinician.
        </p>
      </GlowPanel>
    </div>
  );
}
