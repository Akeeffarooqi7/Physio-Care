# Oriva — The Art of Dentistry

A premium, frontend-only landing site for **Oriva**, a fictional luxury dental atelier. Designed to feel like a ₹15L+ hospitality brand — quiet, precise, and art-directed — rather than a conventional clinic website.

> Crafting perfect smiles with precision.

🌐 Live Demo
https://oriva-dental-production.up.railway.app/

---

## Overview

Oriva is a single-page, static website built with **HTML, Tailwind CSS, and vanilla JavaScript**, enhanced with **GSAP** for scroll-based motion. No backend, no build step, no framework — just open `index.html` and it runs.

The design language draws from editorial print, quiet-luxury hospitality, and high-end cosmetic brands: an ivory canvas, soft-gold accents, Cormorant Garamond serif headings, and deliberately generous whitespace.

---

## Features

### Sections
- Fullscreen hero with Ken Burns background and staggered GSAP intro
- Founder profile (*Dr. Arjun Veer*) with signature card + "Why Choose Us" pillars
- Services grid — 8 disciplines with hover lift, gradient fill, and arrow reveal
- Parallax studio quote
- Draggable Before / After comparison slider (mouse + touch)
- Four-tile hover-zoom case-study gallery
- Auto-scrolling testimonial marquee on dark with glass cards
- Three-article journal preview
- Floating-label appointment form with animated SVG tick success modal
- WhatsApp CTA + floating WhatsApp bubble
- Desaturated Google Maps embed, hours, socials, dark footer with newsletter

### Interactions & Motion
- Branded page loader with letter stagger and progress bar
- Sticky blurring navbar with underline-grow nav links
- Custom cursor glow (desktop)
- Mobile hamburger with staggered menu reveal
- Infinite marquee strip between hero and about
- Scroll-reveal fades via `IntersectionObserver`
- GSAP `ScrollTrigger` parallax on quote image
- Subtle floating-orb ambience in the hero
- Smooth anchor scrolling

### Design system
- **Palette** — ivory, porcelain, ink, gold (soft / light / dark variants)
- **Type** — Cormorant Garamond (display) + Inter (UI)
- **Components** — glassmorphism cards, soft shadows, hairline dividers
- **Responsive** down to 360px with a dedicated mobile menu
- **SEO** — semantic landmarks, meta/OG tags, descriptive alts

---

## Tech stack

| Layer | Tool |
|-------|------|
| Markup | HTML5 |
| Styling | Tailwind CSS (CDN) + custom CSS |
| Motion | GSAP 3 + ScrollTrigger (CDN) |
| Scripts | Vanilla JS (no bundler) |
| Fonts | Google Fonts — Cormorant Garamond, Inter |
| Imagery | Unsplash |

No package manager, no build pipeline — everything loads via CDN.

---

## Getting started

Clone and open:

```bash
git clone https://github.com/<your-username>/oriva-dental.git
cd oriva-dental
```

Then either:

**Option A — open directly**
```bash
# macOS
open index.html
# Windows
start index.html
```

**Option B — serve locally (recommended, for iframe + CORS behaviour)**
```bash
python -m http.server 5500
# visit http://localhost:5500
```

---

## Project structure

```
oriva_dental/
├── index.html          # All sections, markup, and SEO meta
├── css/
│   └── style.css       # Custom styles, animations, component styling
├── js/
│   └── main.js         # GSAP intros, scroll reveal, BA slider, form, menu
└── README.md
```

---

## Customization

- **Brand** — swap the logo SVG and `ORIVA` wordmark in the navbar and footer
- **Palette** — edit the Tailwind `theme.extend.colors` block in `index.html`
- **Images** — replace Unsplash URLs with your own CDN or local assets
- **Contact** — the dummy phone `+91 00000 00000` and email are placeholders; swap them in the hero card, contact, footer, and `wa.me` links
- **Founder** — update the profile image, name, credentials, and signature card text in the About section

---

## Browser support

Tested on recent Chrome, Safari, Firefox, and Edge. Uses modern features (`backdrop-filter`, CSS grid, `IntersectionObserver`, GSAP 3) — graceful on iOS Safari 14+ and Chrome 90+.

---

## Credits

- **Design & Development** — [Akeef Farooqi](https://www.linkedin.com/in/akeeffarooqi7/)
- **Imagery** — [Unsplash](https://unsplash.com) contributors
- **Typography** — [Google Fonts](https://fonts.google.com)
- **Motion** — [GSAP](https://gsap.com) by GreenSock

---

## License

Released under the **MIT License**. Oriva is a fictional brand created for portfolio and demonstration purposes — not affiliated with any real dental practice.
