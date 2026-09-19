# CAT Quant Practice

669 practice questions from CAT past papers (2000–2024) across 4 topics.

## Features

- **669 questions** from 24 years of CAT papers
- **4 topics**: Algebra, Averages & Ratio, PPL, Time Speed Distance
- **Topic + Year + Type filters** — MCQ, TITA, Correct, Incorrect
- **Redo Incorrects** — re-answer wrong questions to improve score
- **Bookmarks** — star questions for later review
- **Virtual scrolling** — lazy rendering via IntersectionObserver for fast load
- **Keyboard shortcuts** — A/B/C/D to answer, S for solution, N for next unsolved
- **40-min section timer** with warning colors
- **Copy button** — copy question text for AI help
- **Mobile responsive** with collapsible sidebar
- **Progress sidebar** — color-coded dots, question jump, search

## Deploy

### Vercel (recommended)

1. Push this repo to GitHub
2. Import repo on [vercel.com](https://vercel.com)
3. Framework: **Other**
4. Root directory: `./`
5. Deploy — done

### Local

```bash
python -m http.server 3000
# open http://localhost:3000
```

## Rebuild from source

```bash
python scripts/build.py
# outputs index.html
```

## Tech

- Single HTML file (no build step for production)
- Vanilla JS — no frameworks, no dependencies
- CSS custom properties for theming
- IntersectionObserver for virtual scrolling
- localStorage for progress persistence
