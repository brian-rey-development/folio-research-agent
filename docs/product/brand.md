# Folio brand

Folio is market intelligence and investment research from SEC filings, and its tagline is "From filings to evidence." The visual direction is professional B2B financial research software that is restrained, precise and research-oriented. The interface has no AI gradients, no decorative neural networks, no stock charts that suggest trading, no unnecessary animation and no serif or italic display fonts.

## Voice

Folio writes like a careful analyst. It states a number with its period and its source, and it attributes each company statement to the company that made it, for example "CrowdStrike states that it is a leader." It names its uncertainty in plain words, it never says "buy" or "sell", and it never claims to give personal investment advice. A sentence is short enough to check, and the interface has no hype words.

## Colors

| Token | Hex | Use |
|---|---|---|
| Forest | `#0F3D33` | Primary brand color, logo, primary buttons |
| Teal | `#146B5B` | Interactive accents, links, focus rings |
| Mint | `#B7D6CC` | Subtle highlights, selected rows, citation marks |
| Sand | `#EDECE7` | Neutral surfaces and page background |
| Ink | `#1F2933` | Body text and high-contrast elements |

## Typography

Inter from Google Fonts is the only typeface, in the Regular, Medium, Semibold and Bold weights. Headings use Semibold or Bold, and body text uses Regular at a size that gives long passages comfortable reading space.

## Logo

The logo is a geometric connected-block symbol with an upright sans-serif wordmark in Inter Bold. The symbol is two rounded blocks that join on a diagonal, which stands for the link from a claim to its source. The files live in `docs/brand`, and the wordmark is outlined as paths so it renders with no installed fonts.

| File | Use |
|---|---|
| `logo.svg` | Symbol and wordmark in Forest, for light backgrounds |
| `mark.svg` | Symbol only, at 16px or larger |
| `icon.svg` | App icon, a Sand symbol on a rounded Forest square |
| `icon.png` | App icon at 512px, for avatars and stores |
| `banner.svg`, `banner.png` | README banner and GitHub social preview, 1280x640 |

## Interface principles

- Dense but readable research screens with a clear hierarchy of information.
- Wide reading space for documents and source passages.
- Visible citations on every claim, with one click to the source passage.
- Structured tables for numbers and risks, with consistent 8px spacing.
- Restrained line icons, and contrast that meets WCAG AA.

The reference components are the research sidebar, filing search, source cards, citation inspector, competitor matrix, competitive map, artifact viewer, conversation panel and project memory settings.
