import { FolioMark } from "@/components/folio-mark";

const MARK_SIZE = 48;

export function BrandHeader() {
  return (
    <div className="flex flex-col items-center gap-2">
      <div className="flex items-center gap-2">
        <FolioMark size={MARK_SIZE} className="text-forest" />
        <span className="text-5xl font-bold text-ink">Folio</span>
      </div>
      <p className="text-lg text-ink/70">From filings to evidence.</p>
    </div>
  );
}
