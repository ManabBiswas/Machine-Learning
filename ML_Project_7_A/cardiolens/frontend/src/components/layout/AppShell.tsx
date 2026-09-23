import { AnimatePresence, motion } from "framer-motion";
import { Outlet, useLocation } from "react-router-dom";
import { TopNav } from "./TopNav";
import { Footer } from "./Footer";

export function AppShell() {
  const location = useLocation();

  return (
    <div className="min-h-screen" style={{ background: "var(--bg)" }}>
      <TopNav />
      {/* <ScrollRail /> */}
      <AnimatePresence mode="wait">
        <motion.main
          key={location.pathname}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -8 }}
          transition={{ duration: 0.2, ease: "easeOut" }}
        >
          <Outlet />
        </motion.main>
      </AnimatePresence>
      <Footer />
    </div>
  );
}
