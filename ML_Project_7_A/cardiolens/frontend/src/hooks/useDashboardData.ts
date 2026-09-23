import { useCallback, useEffect, useState } from "react";
import { cardiolensApi } from "../api/cardiolens";
import type { HistorySummary, Metrics } from "../types/patient";

export function useDashboardData() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [history, setHistory] = useState<HistorySummary | null>(null);

  const refreshHistory = useCallback(async () => {
    try {
      const h = await cardiolensApi.history(8);
      setHistory(h);
    } catch {
      // Non-critical — history strip just stays empty.
    }
  }, []);

  useEffect(() => {
    cardiolensApi
      .metrics()
      .then(setMetrics)
      .catch(() => setMetrics(null));
    refreshHistory();
  }, [refreshHistory]);

  return { metrics, history, refreshHistory };
}
