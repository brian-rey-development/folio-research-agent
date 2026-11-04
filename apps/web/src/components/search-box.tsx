import { SearchIcon } from "@/components/search-icon";

const PLACEHOLDER = "Search companies, sectors, or questions...";

export function SearchBox() {
  return (
    <div className="relative w-full">
      <SearchIcon className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-ink/70" />
      <input
        type="search"
        disabled
        aria-label="Search companies, sectors, or questions"
        placeholder={PLACEHOLDER}
        className="h-14 w-full rounded-xl border border-ink/20 bg-white pl-12 pr-4 text-base text-ink placeholder:text-ink/70 disabled:cursor-not-allowed"
      />
    </div>
  );
}
