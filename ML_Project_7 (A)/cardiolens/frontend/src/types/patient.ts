export interface PatientInput {
  age: number;
  sex: 0 | 1;
  cp: 0 | 1 | 2 | 3;
  trestbps: number;
  chol: number;
  fbs: 0 | 1;
  restecg: 0 | 1 | 2;
  thalach: number;
  exang: 0 | 1;
  oldpeak: number;
  slope: 0 | 1 | 2;
  ca: 0 | 1 | 2 | 3;
  thal: 0 | 1 | 2 | 3;
}

export type RiskTier = "low" | "moderate" | "high";

export interface Driver {
  feature: string;
  label: string;
  value: number;
}

export interface PredictionResponse {
  prediction: 0 | 1;
  probability: number;
  risk_tier: RiskTier;
  drivers: Driver[];
  timestamp: string;
}

export interface Metrics {
  model: string;
  model_version: string;
  accuracy: number;
  f1: number;
  feature_count?: number;
  training_rows?: number;
  last_trained?: string;
}

export interface HistoryRow {
  timestamp: string;
  age: number;
  sex: "M" | "F";
  max_hr: number;
  probability: number;
  risk_label: string;
}

export interface HistorySummary {
  total: number;
  high_risk: number;
  avg_risk: number;
  recent: HistoryRow[];
}

export const DEFAULT_PATIENT: PatientInput = {
  age: 52,
  sex: 0,
  cp: 0,
  trestbps: 125,
  chol: 212,
  fbs: 0,
  restecg: 0,
  thalach: 168,
  exang: 0,
  oldpeak: 1.0,
  slope: 0,
  ca: 0,
  thal: 0,
};
