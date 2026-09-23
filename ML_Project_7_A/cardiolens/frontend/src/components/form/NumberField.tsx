interface Props {
  label: string;
  value: number;
  onChange: (value: number) => void;
  min: number;
  max: number;
  step?: number;
  unit?: string;
  helper?: string;
}

export function NumberField({
  label,
  value,
  onChange,
  min,
  max,
  step = 1,
  unit,
  helper,
}: Props) {
  return (
    <label className="flex flex-col gap-1.5">
      <span className="text-[13px] font-medium" style={{ color: "var(--text)" }}>
        {label}
      </span>
      <div
        className="flex items-center gap-2 rounded-lg border px-3 py-2 transition-colors focus-within:border-[var(--signal)]"
        style={{ borderColor: "var(--border)", background: "var(--bg)" }}
      >
        <input
          type="number"
          value={value}
          min={min}
          max={max}
          step={step}
          onChange={(e) => onChange(Number(e.target.value))}
          className="w-full bg-transparent font-[var(--font-mono)] text-sm outline-none"
          style={{ color: "var(--text)" }}
        />
        {unit && (
          <span
            className="shrink-0 text-xs"
            style={{ color: "var(--text-muted)" }}
          >
            {unit}
          </span>
        )}
      </div>
      {helper && (
        <span className="text-[11px]" style={{ color: "var(--text-muted)" }}>
          {helper}
        </span>
      )}
    </label>
  );
}
