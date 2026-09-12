import { useEffect, useState } from "react";
import { Hero } from "../components/landing/Hero";
import { HowItWorks } from "../components/landing/HowItWorks";
import { StatShowcase } from "../components/landing/StatShowcase";
import { cardiolensApi } from "../api/cardiolens";
import type { Metrics } from "../types/patient";
import { ScrollRail } from "../components/layout/ScrollRail";


export default function Home() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);

  useEffect(() => {
    cardiolensApi
      .metrics()
      .then(setMetrics)
      .catch(() => setMetrics(null));
  }, []);

  return (
    <div>
      <ScrollRail />
      <Hero />
      <HowItWorks />
      <StatShowcase metrics={metrics} />
    </div>
  );
}
