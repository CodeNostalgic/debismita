# ICSE Study Hub (Debismita)

A clean, mobile-first, print-friendly static website for ICSE Class 10 students. Built with plain HTML + CSS + JavaScript — perfect for GitHub Pages.

## Current Structure

- **index.html** — Generic hub listing common ICSE subjects. Literature card links to the dedicated Literature page.
- **literature.html** — Separate page for English Literature with clear sections:
  - Prose
  - Poetry
  - Drama (prominent card links to the Drama hub)
- **drama.html** — Drama hub focused on *The Merchant of Venice*. Shows all 5 Acts with a responsive scene grid. Act 1 Scene 3 links to the full interactive guide.
- **act1-scene3.html** — The full original detailed study guide (RTCs, 20+ model Q&As, character sketches, themes, literary devices, key quotations, interactive checklist, search, print styles, dark/light mode). Now lives under proper navigation context with breadcrumbs back to Drama → Literature → Home.

All other scenes currently show “Coming soon” placeholders (easy to expand using the same template).

## Features
- Excellent mobile + tablet experience (collapsible drawer nav, stacked grids, large touch targets)
- Dark (default) + Light (parchment) themes with localStorage persistence
- Real-time search with highlighting (press `/`)
- Collapsible Q&A cards + global “Reveal All”
- Interactive revision checklist with progress bar (saves progress)
- Beautiful print styles (hides nav, expands all answers, clean typography)
- Fully static — works offline once loaded, no build step

## Navigation Flow
Home (Subjects) → Literature → Drama → Merchant of Venice → Act 1 Scene 3 (or any scene)

## How to Host on GitHub
1. Push all files (`index.html`, `literature.html`, `drama.html`, `act1-scene3.html`, `styles.css`, `app.js`) to a repo (or the `docs/` folder).
2. In repo Settings → Pages → Source: “Deploy from a branch” → main (or `/docs`).
3. Your site will be live at `https://<username>.github.io/<repo>/`

No server required. Add more scene files later following the same pattern (copy act1-scene3.html and swap content).

## Future Expansion
- Add individual scene files (act2-scene1.html etc.)
- Fill in Prose/Poetry pages using the same design system
- Add other ICSE subjects as separate folders or pages

Contributions or suggestions welcome!