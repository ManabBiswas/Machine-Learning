import { useRef, type ReactNode } from "react";
import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";

interface Props {
  children: ReactNode;
  className?: string;
  style?: React.CSSProperties;
}

const MAX_TILT = 4; // degrees — kept subtle, never full 3D-flip territory

export function TiltCard({ children, className, style }: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const rawX = useMotionValue(0.5);
  const rawY = useMotionValue(0.5);
  const rotateX = useTransform(
    useSpring(rawY, { stiffness: 250, damping: 25 }),
    [0, 1],
    [MAX_TILT, -MAX_TILT]
  );
  const rotateY = useTransform(
    useSpring(rawX, { stiffness: 250, damping: 25 }),
    [0, 1],
    [-MAX_TILT, MAX_TILT]
  );

  const handleMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = ref.current?.getBoundingClientRect();
    if (!rect) return;
    rawX.set((e.clientX - rect.left) / rect.width);
    rawY.set((e.clientY - rect.top) / rect.height);
  };

  const handleLeave = () => {
    rawX.set(0.5);
    rawY.set(0.5);
  };

  return (
    <motion.div
      ref={ref}
      onMouseMove={handleMove}
      onMouseLeave={handleLeave}
      style={{ rotateX, rotateY, transformPerspective: 800, ...style }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
