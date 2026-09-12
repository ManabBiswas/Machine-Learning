import { useState } from "react";
import type { PatientInput } from "../../types/patient";
import { DEFAULT_PATIENT } from "../../types/patient";
import { NumberField } from "./NumberField";
import { SelectField } from "./SelectField";
import { SectionLabel } from "../layout/SectionLabel";

interface Props {
  onSubmit: (patient: PatientInput) => void;
  onLoadExample: () => PatientInput | Promise<PatientInput>;
  loading: boolean;
}

export function PatientForm({ onSubmit, onLoadExample, loading }: Props) {
  const [patient, setPatient] = useState<PatientInput>(DEFAULT_PATIENT);

  const set = <K extends keyof PatientInput>(key: K, value: PatientInput[K]) =>
    setPatient((prev) => ({ ...prev, [key]: value }));

  const handleExample = async () => {
    const example = await onLoadExample();
    setPatient(example);
  };

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(patient);
      }}
      className="flex flex-col gap-6"
    >
      <div className="flex items-center justify-between">
        <SectionLabel>Demographics</SectionLabel>
        <button
          type="button"
          onClick={handleExample}
          className="text-xs font-medium underline-offset-4 hover:underline"
          style={{ color: "var(--signal)" }}
        >
          Load example patient
        </button>
      </div>
      <div className="grid grid-cols-2 gap-4">
        <NumberField
          label="Age"
          value={patient.age}
          onChange={(v) => set("age", v)}
          min={18}
          max={100}
          unit="yrs"
        />
        <SelectField
          label="Sex"
          value={patient.sex}
          onChange={(v) => set("sex", v as 0 | 1)}
          options={[
            { value: 0, label: "Female" },
            { value: 1, label: "Male" },
          ]}
        />
        <SelectField
          label="Chest pain type"
          value={patient.cp}
          onChange={(v) => set("cp", v as 0 | 1 | 2 | 3)}
          options={[
            { value: 0, label: "Typical angina" },
            { value: 1, label: "Atypical angina" },
            { value: 2, label: "Non-anginal pain" },
            { value: 3, label: "Asymptomatic" },
          ]}
          helper="Asymptomatic carries the highest risk weight"
        />
        <NumberField
          label="Resting blood pressure"
          value={patient.trestbps}
          onChange={(v) => set("trestbps", v)}
          min={80}
          max={220}
          unit="mmHg"
          helper="Normal < 120"
        />
      </div>

      <SectionLabel>Vitals &amp; labs</SectionLabel>
      <div className="grid grid-cols-2 gap-4">
        <NumberField
          label="Cholesterol"
          value={patient.chol}
          onChange={(v) => set("chol", v)}
          min={100}
          max={600}
          unit="mg/dl"
          helper="Desirable < 200"
        />
        <SelectField
          label="Fasting blood sugar"
          value={patient.fbs}
          onChange={(v) => set("fbs", v as 0 | 1)}
          options={[
            { value: 0, label: "≤ 120 mg/dl" },
            { value: 1, label: "> 120 mg/dl" },
          ]}
        />
        <SelectField
          label="Resting ECG"
          value={patient.restecg}
          onChange={(v) => set("restecg", v as 0 | 1 | 2)}
          options={[
            { value: 0, label: "Normal" },
            { value: 1, label: "ST-T abnormality" },
            { value: 2, label: "LV hypertrophy" },
          ]}
        />
        <NumberField
          label="Max heart rate"
          value={patient.thalach}
          onChange={(v) => set("thalach", v)}
          min={60}
          max={220}
          unit="bpm"
          helper="Achieved during exercise"
        />
      </div>

      <SectionLabel>ECG &amp; exercise</SectionLabel>
      <div className="grid grid-cols-2 gap-4">
        <SelectField
          label="Exercise-induced angina"
          value={patient.exang}
          onChange={(v) => set("exang", v as 0 | 1)}
          options={[
            { value: 0, label: "No" },
            { value: 1, label: "Yes" },
          ]}
        />
        <NumberField
          label="Oldpeak (ST depression)"
          value={patient.oldpeak}
          onChange={(v) => set("oldpeak", v)}
          min={0}
          max={7}
          step={0.1}
          unit="mm"
        />
        <SelectField
          label="ST slope"
          value={patient.slope}
          onChange={(v) => set("slope", v as 0 | 1 | 2)}
          options={[
            { value: 0, label: "Upsloping" },
            { value: 1, label: "Flat" },
            { value: 2, label: "Downsloping" },
          ]}
        />
        <SelectField
          label="Major vessels"
          value={patient.ca}
          onChange={(v) => set("ca", v as 0 | 1 | 2 | 3)}
          options={[0, 1, 2, 3].map((n) => ({ value: n, label: String(n) }))}
          helper="Colored by fluoroscopy"
        />
        <SelectField
          label="Thalassemia"
          value={patient.thal}
          onChange={(v) => set("thal", v as 0 | 1 | 2 | 3)}
          options={[
            { value: 0, label: "None" },
            { value: 1, label: "Fixed defect" },
            { value: 2, label: "Normal" },
            { value: 3, label: "Reversible defect" },
          ]}
          helper="Reversible defect is a strong risk marker"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="mt-2 rounded-lg py-3 font-[var(--font-display)] text-sm font-semibold transition-opacity disabled:opacity-60"
        style={{ background: "var(--signal)", color: "#04110f" }}
      >
        {loading ? "Analyzing…" : "Predict risk"}
      </button>
    </form>
  );
}
