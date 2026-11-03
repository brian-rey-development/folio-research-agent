import { BrandHeader } from "@/components/brand-header";
import { SearchBox } from "@/components/search-box";

export default function Home() {
  return (
    <main className="flex flex-1 items-center justify-center px-6">
      <div className="flex w-full max-w-2xl flex-col items-center gap-8">
        <BrandHeader />
        <SearchBox />
        <p className="text-sm text-ink/70">
          The research agent arrives in stage 1.
        </p>
      </div>
    </main>
  );
}
