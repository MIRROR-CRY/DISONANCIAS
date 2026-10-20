# DISONANCIAS Publication — Data & Decisions

**Date:** 2026-09-24  
**Context:** Decision session on pricing, Bandcamp landing page, and single release

## FINAL DECISIONS

### Pricing
- **Minimum:** $1.50 USD
- **Strategy:** Pay-what-you-want (PWYW) enabled
- **Rationale:**
  - Bandcamp default (April 2025) for singles: $1.50
  - 40% of fans pay more on average
  - Round number, not fake (avoids 0.99/0.50 marketing sound)
  - Accessible but respects the work
  - Goal: ~48 purchases to reach $100 USD (minimum withdrawal)

### Landing Page
- **File:** `/home/user/Emma-HQ/MIRROR-CRY_DISONANCIAS/bandcamp-landing.html`
- **Status:** Merged to main on Emma-HQ (PR #2)
- **Features:**
  - Professional Bandcamp-style design
  - Header with waveform
  - Complete tracklist with roles (V1, Bridge, V2, Chorus)
  - Album concept section
  - Artist info (MIRROR CRY)
  - Links to GitHub, Spotify, Apple Music
  - Responsive + Bloomberg dark theme (#0a0a0a)

### DISONANCIAS Album — Structure
| # | Short Name | Full Name | Duration | Role | Theme |
|---|---|---|---|---|---|
| 1 | Kicking Stones | Second Floor (Kicking Stones) | 3:15 | Verse 1 | Political lie: systems fail but we pretend they work |
| 2 | Rescue Us | Rescue Us | 4:12 | Bridge | Personal lie: cognitive dissonance we knowingly maintain |
| 3 | Medio Limón | Medio Limón | 3:45 | Verse 2 | Inherited lie: traditions are constructions, not eternal |
| 4 | Sin Título | Sin Título | 2:58 | Chorus | Collective admission: we're all living these lies |

### Separate GitHub Repository
- **Target:** `MIRROR-CRY/DISONANCIAS` (organization name in all caps)
- **Status:** Push blocked, Claude GitHub App not authorized for `mirror-cry` org yet
- **Needed:** Install app at https://github.com/apps/claude/installations/select_target OR reconnect GitHub at https://claude.ai/customize/connectors
- **Workaround used:** Code-only zip (186KB, docs + .py + .ly files, no audio) delivered for manual upload
- **Album cover:** `ALBUM_DISONANCIAS.jpg` (zapatillas + reloj), to use as artist avatar

---

## TRACK 1: SECOND FLOOR (KICKING STONES)

### Publication Model
- **Type:** Released as standalone single on Bandcamp (no album references in description/about)
- **Conceptually:** Still Verse 1 of the DISONANCIAS macro-structure, but not marketed that way in this release
- **Price:** $1.50 or more (individual track purchase enabled)
- **Featured track:** Yes (cued up for Discover)

### Metadata
- **Full Title:** Second Floor (Kicking Stones)
- **Artist:** MIRROR CRY
- **Duration:** 3:15
- **BPM:** 148

### Audio File
- **Bandcamp upload:** `KickingStonesv8.wav` (26MB, lossless) — already uploaded to Bandcamp draft
- **Repo copy (older):** `/home/user/Emma-HQ/MIRROR-CRY_DISONANCIAS/Kicking Stones v2/final_master/KickingStonesv5.mp3`

### Bandcamp Description (FINAL, no em dashes, no album references)
```
Kicking stones against grey walls. The gesture of being surplus to the system's design.

A critique of institutions that promise reconstruction and deliver only more ruins. 
The phrase "national reconstruction" appears twice in Chilean history, 53 years apart: 
once from a law faculty celebrating a coup in 1973, once from a president's plan in 2026. 
Same words, opposite memories. Forgotten by most, treasured by some.

Chilean youth unemployment sits at 24.6% in 2026. Almost 40 years after Los Prisioneros 
sang about a generation left "kicking stones," the number of young people left out of 
the system's design hasn't moved.

The song names its targets directly. The pulpit mic, a nod to ex-minister Mara Sedini. 
The second floor's assessors, the unelected advisors who work from La Moneda's second 
floor and end up governing more than whoever was elected. The Brick, El Ladrillo, the 
economic plan drafted under the dictatorship that still frames the model today.

Code-generated hip-hop rhythm at 148 BPM. Vocals deliberately declamatory (parlato), 
not melodically pitched. Thinking aloud, not performing.
```

### Bandcamp "About This Track" (FINAL, no em dashes, no album references)
```
Backing track composed in Python (librosa, music21, NumPy). 
Syncopated hip-hop rhythm with stochastic variations and minimalist synthesis.

The vocal delivery (32% of frames within ±20 cents of defined pitch) is a deliberate 
choice for a song about systems we know are broken but maintain anyway. Synthesis 
is more honest than pretending to play guitar.

Visual concept: brutalist San Borja, Santiago, paired with Humberstone, a ghost town 
that was once a saltpeter company town where workers were paid in tokens redeemable 
only at the company store. The same closed-loop control echoed today in subsidies 
that can only be spent on one thing.
```

### Track Credits (FINAL for Bandcamp)
```
Composition, production, vocals: Emmanuel Ángel Norambuena
Code generator: Python (librosa, music21, NumPy)
Assistance: Claude (code refactoring, lyrics refinement)
Location: Santiago, Chile
```

### Lyrics (FINAL)
```
[Intro]

[Verse 1]
Singers taunting on pulpit mic
keep working the show
While 2nd floor's assessors
continue the mega-reform

[Verse 2]
In the shadow of concrete giants
where shock ink is warm
Like people's blood running
down where only bikes should run

[Pre-Chorus]
Looking at winged solutions
Watching the model decay
From "The Brick" to the rubble
Just improvising the ruins today

[Chorus]
Winged solutions for a failing frame
The architect would die of shame
We have no place in the design
Just kicking stones against grey walls
We're just wasting time
Kicking stones against grey walls...

[Bridge]
"Those who have power make choises that create poverty"

[Chorus]
Winged solutions for a failing frame
The architect would die of shame
We have no place in the design
Just kicking stones against grey walls
We're just wasting time
Kicking stones against grey walls...

[Post-Chorus]
We're just wasting time
Kicking stones against grey walls...
(Kicking stones against grey walls...)

[Outro]
The masterplan
The mega-reform
The architect would die of shame
Just kicking stones
Just hitting rocks
Against grey walls
They will never stop
```

### Lyrics — Real-World References (internal documentation, not on Bandcamp)
- **"pulpit mic"** → ex-minister Mara Sedini
- **"2nd floor's assessors" / "second floor"** → "los asesores del segundo piso": Chilean political term for the second floor of La Moneda (presidential palace), where presidential advisors work. Common shorthand for the unelected advisors who actually govern behind the elected president.
- **"The Brick" ("El Ladrillo")** → the economic plan drafted under the dictatorship (Chicago Boys), foundational document for Chile's neoliberal model.

### Video Concept (internal documentation only, not on Bandcamp track page)
- **Locations:** Split-screen
  - San Borja, Santiago (decaying brutalist buildings)
  - Humberstone Saltpeter Office, Atacama (ghost town)
- **Intro Visual:**
  - UC Law School clipping from 1973 (audio of Kast 2026 plays over)
  - Alteration of Humberstone sign → "KICKINGSTONES"

### Tags (Bandcamp, already entered)
experimental, post-punk, spoken word, code-composition, ambient, electronic

### References (for internal documentation, not public-facing)
- **Los Prisioneros — "Pateando Piedras" / "El Baile de los que Sobran"** (1986)
- **Molchat Doma** — Belarusian post-punk/cold wave, sovietwave
- **Txefas — "Demasiau"** — Spanish post-punk, existential exhaustion
- **Candelabro — "Fracaso"** / **"Estación Central"** — Chilean generational catharsis

### Naming note
Original working title was "Kicking Stones" alone, directly matching Los Prisioneros' 
"Pateando Piedras." Changed to "Second Floor (Kicking Stones)" to avoid being seen as 
derivative, since Los Prisioneros (especially Jorge González) are iconoclastic reference 
points in Chile and direct homage risks mockery. New title keeps the stones/ruins metaphor, 
adds a San Borja architectural reference (second floor), and reads as distinct.

---

## TRACKS 2-4 (Pending data compilation)

- [ ] Rescue Us — early composition phase, melody base defined, not mastered
- [ ] Medio Limón — lyrics drafted, backing track in development, Spanish language
- [ ] Sin Título — nothing composed yet, only style reference (Lumineers "Ho Hey")

---

## Git & Branches (Emma-HQ repo, internal docs only)

### Current Status (2026-09-24)
- **Main branch:** main
- **Working branch:** claude/song-landing-code-oj18pi
- **Merged PRs:**
  - #1: docs: browser-optimization-for-claude
  - #2: feat: add Bandcamp landing page for DISONANCIAS

### Key Commits
- e524f6d: feat: add MIRROR-CRY DISONANCIAS album project
- 74daada: Merge PR #1 (browser research)
- 5b0c658: feat: add Bandcamp landing page
- 05c1040: Merge PR #2 (landing page)

---

## Next Steps

- [ ] Authorize Claude GitHub App for `mirror-cry` org (or reconnect connector)
- [ ] Push code-only content to `MIRROR-CRY/DISONANCIAS` once authorized
- [ ] Finish Bandcamp draft for "Second Floor (Kicking Stones)" and publish
- [ ] Compile data for Rescue Us (Track 2)
- [ ] Compile data for Medio Limón (Track 3)
- [ ] Compile data for Sin Título (Track 4)
- [ ] Coordinate with RouteNote for Spotify/Apple Music distribution (full album, later)

---

**Important note:** Update this document after EVERY decision.
No using compaction as excuse to lose data. ✅
