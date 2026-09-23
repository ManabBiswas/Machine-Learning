import { useCallback, useState } from "react";
import { cardiolensApi } from "../api/cardiolens";
import type { PatientInput, PredictionResponse } from "../types/patient";

interface UsePredictionState {
  result: PredictionResponse | null;
  loading: boolean;
  error: string | null;
}

export function usePrediction() {
  const [state, setState] = useState<UsePredictionState>({
    result: null,
    loading: false,
    error: null,
  });

  const predict = useCallback(async (patient: PatientInput) => {
    setState({ result: null, loading: true, error: null });
    try {
      const result = await cardiolensApi.predict(patient);
      setState({ result, loading: false, error: null });
      return result;
    } catch (err) {
      const message = err instanceof Error ? err.message : "Prediction failed.";
      setState({ result: null, loading: false, error: message });
      return null;
    }
  }, []);

  const reset = useCallback(() => {
    setState({ result: null, loading: false, error: null });
  }, []);

  return { ...state, predict, reset };
}
