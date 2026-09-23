export function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <div className="mb-3 flex items-center gap-2">
      <span
        className="h-3.5 w-1 rounded-full"
        style={{ background: "var(--signal)" }}
      />
      <h2
        className="font-[var(--font-display)] text-[15px] font-semibold"
        style={{ color: "var(--text)" }}
      >
        {children}
      </h2>
    </div>
  );
}
