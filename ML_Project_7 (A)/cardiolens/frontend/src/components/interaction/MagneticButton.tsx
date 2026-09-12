import { useRef } from "react";
import { motion, useMotionValue, useSpring } from "framer-motion";

interface Props {
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
  style?: React.CSSProperties;
  type?: "button" | "submit";
  disabled?: boolean;
}

export function MagneticButton({
  children,
  onClick,
  className,
  style,
  type = "button",
  disabled,
}: Props) {
  const ref = useRef<HTMLButtonElement>(null);
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const springX = useSpring(x, { stiffness: 300, damping: 20 });
  const springY = useSpring(y, { stiffness: 300, damping: 20 });

  const handleMove = (e: React.MouseEvent<HTMLButtonElement>) => {
    const rect = ref.current?.getBoundingClientRect();
    if (!rect) return;
    const relX = e.clientX - (rect.left + rect.width / 2);
    const relY = e.clientY - (rect.top + rect.height / 2);
    x.set(relX * 0.25);
    y.set(relY * 0.35);
  };

  const handleLeave = () => {
    x.set(0);
    y.set(0);
  };

  return (
    <motion.button
      ref={ref}
      type={type}
      onClick={onClick}
      disabled={disabled}
      onMouseMove={handleMove}
      onMouseLeave={handleLeave}
      className={className}
      style={{ x: springX, y: springY, ...style }}
    >
      {children}
    </motion.button>
  );
}
