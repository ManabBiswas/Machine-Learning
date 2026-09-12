interface Option {
  value: number;
  label: string;
}

interface Props {
  label: string;
  value: number;
  onChange: (value: number) => void;
  options: Option[];
  helper?: string;
}

export function SelectField({ label, value, onChange, options, helper }: Props) {
  return (
    <label className="flex flex-col gap-1.5">
      <span className="text-[13px] font-medium" style={{ color: "var(--text)" }}>
        {label}
      </span>
      <div
        className="rounded-lg border px-3 py-2 transition-colors focus-within:border-[var(--signal)]"
        style={{ borderColor: "var(--border)", background: "var(--bg)" }}
      >
        <select
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="w-full bg-transparent text-sm outline-none"
          style={{ color: "var(--text)" }}
        >
          {options.map((opt) => (
            <option
              key={opt.value}
              value={opt.value}
              style={{ background: "var(--surface-raised)", color: "var(--text)" }}
            >
              {opt.label}
            </option>
          ))}
        </select>
      </div>
      {helper && (
        <span className="text-[11px]" style={{ color: "var(--text-muted)" }}>
          {helper}
        </span>
      )}
    </label>
  );
}
