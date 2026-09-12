import { cardiolensApi } from "../api/cardiolens";
import { StatStrip } from "../components/layout/StatStrip";
import { PatientForm } from "../components/form/PatientForm";
import { ResultPanel } from "../components/results/ResultPanel";
import { HistoryTable } from "../components/history/HistoryTable";
import { usePrediction } from "../hooks/usePrediction";
import { useDashboardData } from "../hooks/useDashboardData";
import { DEFAULT_PATIENT, type PatientInput } from "../types/patient";

export default function Assess() {
  const { result, loading, error, predict } = usePrediction();
  const { metrics, history, refreshHistory } = useDashboardData();

  const handleSubmit = async (patient: PatientInput) => {
    const res = await predict(patient);
    if (res) refreshHistory();
  };

  const handleLoadExample = async (): Promise<PatientInput> => {
    try {
      return await cardiolensApi.examplePatient();
    } catch {
      return DEFAULT_PATIENT;
    }
  };

  return (
    <div className="mx-auto max-w-6xl px-6 pb-16 pt-10">
      <h1
        className="font-[var(--font-display)] text-2xl font-bold"
        style={{ color: "var(--text)" }}
      >
        Risk assessment
      </h1>
      <p
        className="mb-6 mt-1 max-w-xl text-sm"
        style={{ color: "var(--text-muted)" }}
      >
        Interpretable heart disease risk estimation from routine clinical
        measurements — powered by a logistic regression model trained on
        the UCI Heart Disease dataset.
      </p>

      <div className="mb-8">
        <StatStrip metrics={metrics} />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1.15fr_0.85fr]">
        <div
          className="rounded-2xl border p-6"
          style={{
            borderColor: "var(--border)",
            background: "var(--surface)",
            boxShadow: "var(--shadow-ambient)",
          }}
        >
          <PatientForm
            onSubmit={handleSubmit}
            onLoadExample={handleLoadExample}
            loading={loading}
          />
        </div>

        <ResultPanel result={result} loading={loading} error={error} />
      </div>

      <div className="mt-8">
        <HistoryTable history={history} />
      </div>
    </div>
  );
}
