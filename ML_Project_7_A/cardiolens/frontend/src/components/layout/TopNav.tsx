import { motion } from "framer-motion";
import { NavLink } from "react-router-dom";
import { useTheme } from "../../context/ThemeContext";

const LINKS = [
  { to: "/", label: "Home" },
  { to: "/assess", label: "Assess" },
  { to: "/insights", label: "Insights" },
  { to: "/about", label: "About" },
];

export function TopNav() {
  const { theme, toggleTheme } = useTheme();

  return (
    <header
      className="sticky top-0 z-40 border-b backdrop-blur-md"
      style={{
        borderColor: "var(--border)",
        background: "color-mix(in srgb, var(--bg) 85%, transparent)",
      }}
    >
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <NavLink to="/" className="flex items-center gap-3">
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
            className="font-[var(--font-display)] text-lg font-bold tracking-tight"
            style={{ color: "var(--text)" }}
          >
            CardioLens
          </span>
        </NavLink>

        <nav className="hidden items-center gap-1 sm:flex">
          {LINKS.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.to === "/"}
              className="relative px-3 py-2 text-sm font-medium"
              style={({ isActive }) => ({
                color: isActive ? "var(--text)" : "var(--text-muted)",
              })}
            >
              {({ isActive }) => (
                <>
                  {link.label}
                  {isActive && (
                    <motion.span
                      layoutId="nav-active"
                      className="absolute inset-x-3 -bottom-[1px] h-[2px] rounded-full"
                      style={{ background: "var(--signal)" }}
                      transition={{ type: "spring", stiffness: 500, damping: 35 }}
                    />
                  )}
                </>
              )}
            </NavLink>
          ))}
        </nav>

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
      </div>
    </header>
  );
}
