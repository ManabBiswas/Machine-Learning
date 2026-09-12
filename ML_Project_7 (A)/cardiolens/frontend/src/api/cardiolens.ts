import { apiClient } from "./client";
import type {
  HistorySummary,
  Metrics,
  PatientInput,
  PredictionResponse,
} from "../types/patient";

export const cardiolensApi = {
  async health(): Promise<{ status: string }> {
    const { data } = await apiClient.get("/health");
    return data;
  },

  async metrics(): Promise<Metrics> {
    const { data } = await apiClient.get("/metrics");
    return data;
  },

  async examplePatient(): Promise<PatientInput> {
    const { data } = await apiClient.get("/example-patient");
    return data;
  },

  async predict(patient: PatientInput): Promise<PredictionResponse> {
    const { data } = await apiClient.post("/predict", patient);
    return data;
  },

  async history(limit = 8): Promise<HistorySummary> {
    const { data } = await apiClient.get("/history", { params: { limit } });
    return data;
  },

  async exportHistoryCsv(): Promise<string> {
    const { data } = await apiClient.get("/history/export");
    return data.csv;
  },
};
