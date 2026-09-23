import { motion } from "framer-motion";
import { useTheme } from "../../context/ThemeContext";

export function TopBar() {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="flex items-center justify-between py-6">
      <div className="flex items-center gap-3">
        <span className="relative flex h-3 w-3">
          <span
            className="absolute inline-flex h-full w-full animate-ping rounded-full opacity-60"
            style={{ background: "var(--signal)" }}
          />
          <span
            className="relative inline-flex h-3 w-3 rounded-full"
            style={{ background: "var(--signal)" }}
          />
        </span>
        <span
          className="font-[var(--font-display)] text-xl font-bold tracking-tight"
          style={{ color: "var(--text)" }}
        >
          CardioLens
        </span>
      </div>

      <button
        onClick={toggleTheme}
        aria-label="Toggle color theme"
        className="relative flex h-9 w-16 items-center rounded-full border px-1 transition-colors"
        style={{
          background: "var(--surface-raised)",
          borderColor: "var(--border)",
        }}
      >
        <motion.span
          layout
          transition={{ type: "spring", stiffness: 500, damping: 32 }}
          className="flex h-7 w-7 items-center justify-center rounded-full text-[11px]"
          style={{
            background: "var(--signal)",
            marginLeft: theme === "light" ? "auto" : 0,
            color: "#04110f",
          }}
        >
          {theme === "dark" ? "🌙" : "☀"}
        </motion.span>
      </button>
    </header>
  );
}
