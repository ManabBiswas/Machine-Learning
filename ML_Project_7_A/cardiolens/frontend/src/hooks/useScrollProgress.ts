import { useEffect, useRef, useState } from "react";
import { useLocation } from "react-router-dom";

/**
 * Returns scroll progress (0-1) for the whole document, re-measuring
 * on route change so the rail doesn't carry stale progress between
 * pages of different heights.
 */
export function useScrollProgress() {
  const { pathname } = useLocation();
  const [progress, setProgress] = useState(0);
  const ticking = useRef(false);

  useEffect(() => {
    setProgress(0);
    window.scrollTo(0, 0);

    const measure = () => {
      const doc = document.documentElement;
      const scrollable = doc.scrollHeight - doc.clientHeight;
      const pct = scrollable > 0 ? doc.scrollTop / scrollable : 0;
      setProgress(Math.min(Math.max(pct, 0), 1));
      ticking.current = false;
    };

    const onScroll = () => {
      if (!ticking.current) {
        ticking.current = true;
        requestAnimationFrame(measure);
      }
    };

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", measure);
    measure();

    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", measure);
    };
  }, [pathname]);

  return progress;
}
