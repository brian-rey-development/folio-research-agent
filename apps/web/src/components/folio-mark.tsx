const MARK_PATH =
  "M55,5 H85 A10,10 0 0 1 95,15 V45 A10,10 0 0 1 85,55 H65 A10,10 0 0 0 55,65 V85 A10,10 0 0 1 45,95 H15 A10,10 0 0 1 5,85 V55 A10,10 0 0 1 15,45 H35 A10,10 0 0 0 45,35 V15 A10,10 0 0 1 55,5 Z";

const DEFAULT_SIZE = 32;

type FolioMarkProps = {
  size?: number;
  className?: string;
  title?: string;
};

export function FolioMark({
  size = DEFAULT_SIZE,
  className,
  title,
}: FolioMarkProps) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 100 100"
      width={size}
      height={size}
      fill="currentColor"
      className={className}
      role={title ? "img" : undefined}
      aria-hidden={title ? undefined : true}
    >
      {title ? <title>{title}</title> : null}
      <path d={MARK_PATH} />
    </svg>
  );
}
