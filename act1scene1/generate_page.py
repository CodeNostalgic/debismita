import html
from parse_line_by_line import load_sections
from section_overviews import SECTION_OVERVIEWS

sections = []
for sec in load_sections():
    sections.append({
        "title": sec["title"],
        "explanation": "",
        "lines": [
            {"text": line["text"], "translation": line["translation"], "speaker": line.get("speaker")}
            for line in sec["lines"]
        ],
    })

def esc(s):
    return html.escape(s, quote=True)


def render_overview(title, fallback):
    text = SECTION_OVERVIEWS.get(title, fallback)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return f"<p>{esc(fallback)}</p>"
    return "".join(f"<p>{esc(p)}</p>" for p in paragraphs)


line_blocks = []
for i, sec in enumerate(sections):
    sid = f"section-{i+1}"
    lines_html = []
    for line in sec["lines"]:
        speaker = line.get("speaker")
        speaker_html = ""
        if speaker and speaker not in ("STAGE",):
            speaker_html = f'<span class="speaker-badge">{esc(speaker)}</span>'
        elif speaker == "STAGE":
            speaker_html = f'<span class="speaker-badge stage-direction">Stage</span>'
        lines_html.append(f"""          <div class="line-pair searchable-card">
            {speaker_html}
            <p class="line-original">{esc(line['text'])}</p>
            <p class="line-translation">{esc(line['translation'])}</p>
          </div>""")
    line_blocks.append(f"""        <div class="lit-section-block searchable-card" id="{sid}">
          <button class="section-toggle" aria-expanded="true" aria-controls="{sid}-body">
            <div class="section-toggle-text">
              <span class="section-num">Part {i+1}</span>
              <h3 class="section-toggle-title">{esc(sec['title'])}</h3>
            </div>
            <svg class="section-toggle-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
          </button>
          <div class="section-body open" id="{sid}-body">
            <div class="analysis-box" style="margin-bottom:18px;">
              <div class="analysis-title">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                Section Overview
              </div>
              <div class="analysis-text overview-rich">{render_overview(sec['title'], sec['explanation'])}</div>
            </div>
            <div class="line-pairs">
{chr(10).join(lines_html)}
            </div>
          </div>
        </div>""")

nav_items = "\n".join(
    f'      <li class="nav-item"><a href="#section-{i+1}"><svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg> {esc(sec["title"])}</a></li>'
    for i, sec in enumerate(sections)
)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Merchant of Venice • Act 1, Scene 1 • ICSE Study Hub</title>
  <link rel="stylesheet" href="styles.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
</head>
<body>

  <div class="mobile-header">
    <a href="drama.html" class="sidebar-brand">
      <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
      Drama
    </a>
    <button class="menu-toggle-btn" id="menu-toggle" aria-label="Toggle Navigation Menu">
      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
    </button>
  </div>

  <aside id="sidebar">
    <div class="sidebar-header">
      <a href="drama.html" class="sidebar-brand">
        <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
        Merchant of Venice
      </a>
      <span class="sidebar-subtitle">Act 1, Scene 1 • Line-by-Line</span>
      <a href="drama.html" style="font-size:0.75rem;color:#fbbf24;margin-top:4px;display:inline-flex;align-items:center;gap:4px;text-decoration:none;">
        ← All Scenes
      </a>
    </div>
    <ul class="nav-list">
      <li class="nav-item active"><a href="#hero"><svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg> Overview</a></li>
      <li class="nav-item"><a href="#synopsis"><svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg> Synopsis</a></li>
      <li class="nav-item"><a href="#line-by-line"><svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M4 19.5A2.5 2.5 0 0 0 6.5 22H20M4 3.5A2.5 2.5 0 0 1 6.5 1H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5v-14z"/></svg> Line-by-Line</a></li>
{nav_items}
      <li class="nav-item"><a href="#characters"><svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg> Characters</a></li>
      <li class="nav-item"><a href="#themes"><svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/></svg> Themes</a></li>
      <li class="nav-item"><a href="#quotations"><svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M3 21c3 0 7-9 7-14a5 5 0 0 0-10 0c0 5 4 14 7 14zm11 0c3 0 7-9 7-14a5 5 0 0 0-10 0c0 5 4 14 7 14z"/></svg> Key Quotations</a></li>
      <li class="nav-item"><a href="#revision-tracker"><svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg> Revision</a></li>
    </ul>
    <div style="padding:12px 16px;border-top:1px solid var(--border-color);font-size:0.75rem;">
      <a href="drama.html" style="color:#fbbf24;display:block;text-align:center;text-decoration:none;">← Back to Drama Hub</a>
    </div>
  </aside>

  <div class="app-container">
    <header>
      <div class="header-actions">
        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input type="text" id="search-input" class="search-input" placeholder="Search lines, characters, themes... (Press '/' to focus)">
        </div>
        <div class="header-controls">
          <button class="btn-control" id="expand-sections-btn" aria-label="Expand all sections">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
            <span class="tooltip">Expand All</span>
          </button>
          <button class="btn-control" id="theme-toggle" aria-label="Toggle light/dark mode">
            <svg class="theme-icon-dark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
            <span class="tooltip">Toggle Theme</span>
          </button>
          <button class="btn-control" id="print-btn" aria-label="Print Study Guide">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
            <span class="tooltip">Print Guide</span>
          </button>
        </div>
      </div>
    </header>

    <main>
      <div class="breadcrumbs">
        <a href="index.html">Home</a>
        <span class="sep">/</span>
        <a href="literature.html">Literature</a>
        <span class="sep">/</span>
        <a href="drama.html">Drama</a>
        <span class="sep">/</span>
        <a href="drama.html">Merchant of Venice</a>
        <span class="sep">/</span>
        <span style="color:var(--color-primary);">Act 1, Scene 1</span>
      </div>

      <section id="hero">
        <div class="hero-banner">
          <h1>The Merchant of Venice</h1>
          <p>Act 1, Scene 1 • Opening Scene Study Guide</p>
          <div class="hero-meta">
            <div class="meta-tag">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              Standard: <strong>ICSE Literature</strong>
            </div>
            <div class="meta-tag">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              Setting: <strong>Venice</strong>
            </div>
            <div class="meta-tag">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M4 3.5A2.5 2.5 0 0 1 6.5 1H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5v-14z"/></svg>
              Sections: <strong>{len(sections)}</strong>
            </div>
          </div>
        </div>
      </section>

      <section id="synopsis">
        <div class="section-header">
          <h2 class="section-title">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
            Scene Synopsis
          </h2>
          <span class="section-badge">Before the Scene</span>
        </div>
        <div class="card searchable-card">
          <p style="font-size:1.02rem;line-height:1.75;margin-bottom:16px;">
            Antonio, a wealthy Venetian merchant, opens the play in a state of unexplained melancholy. His friends Salarino and Solanio suggest he is worried about his ships at sea, but Antonio denies this. After Gratiano and Lorenzo depart, Bassanio reveals his plan to court Portia, the wealthy heiress of Belmont. Antonio, though his fortune is tied up in overseas trade, promises to borrow money on his credit so Bassanio can pursue her.
          </p>
          <div class="analysis-box">
            <div class="analysis-title">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
              Why This Scene Matters
            </div>
            <div class="analysis-text">
              Act 1 Scene 1 establishes the emotional foundation of the entire play: Antonio's mysterious sadness, the deep bond between Antonio and Bassanio, and the introduction of Portia and the Belmont subplot. Antonio's promise to borrow money for Bassanio directly sets up the bond with Shylock in Scene 3.
            </div>
          </div>
        </div>
      </section>

      <section id="line-by-line">
        <div class="section-header">
          <h2 class="section-title">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M4 3.5A2.5 2.5 0 0 1 6.5 1H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5v-14z"/></svg>
            Line-by-Line Translation
          </h2>
          <span class="section-badge">{sum(len(s['lines']) for s in sections)} Lines</span>
        </div>
        <p style="color:var(--text-muted);margin-bottom:20px;font-size:0.92rem;">Each section includes a brief overview followed by the original Shakespearean text with a clear modern translation. Click any section header to collapse or expand.</p>

{chr(10).join(line_blocks)}
      </section>

      <section id="characters">
        <div class="section-header">
          <h2 class="section-title">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
            Characters Introduced
          </h2>
          <span class="section-badge">Scene 1</span>
        </div>
        <div class="character-container">
          <div class="char-profile searchable-card">
            <div class="char-header">
              <div class="char-avatar" style="border-color: var(--color-primary); color: var(--color-primary); background-color: rgba(251, 191, 36, 0.2);">A</div>
              <div>
                <h3 class="char-title">Antonio</h3>
                <span class="char-subtitle">The Melancholy Merchant</span>
              </div>
            </div>
            <div class="char-body">
              <div class="trait-list">
                <span class="trait-tag">Melancholic</span>
                <span class="trait-tag">Generous</span>
                <span class="trait-tag">Loyal</span>
              </div>
              <p class="char-desc">Opens the play with unexplained sadness. He rejects theories about business worry or love, comparing life to a stage where his role is a sad one. His unconditional offer to help Bassanio drives the plot forward.</p>
            </div>
          </div>
          <div class="char-profile searchable-card">
            <div class="char-header">
              <div class="char-avatar" style="border-color: var(--color-secondary); color: var(--color-secondary); background-color: rgba(99, 102, 241, 0.2);">B</div>
              <div>
                <h3 class="char-title">Bassanio</h3>
                <span class="char-subtitle">The Romantic Adventurer</span>
              </div>
            </div>
            <div class="char-body">
              <div class="trait-list">
                <span class="trait-tag">Extravagant</span>
                <span class="trait-tag">Persuasive</span>
                <span class="trait-tag">Optimistic</span>
              </div>
              <p class="char-desc">Admits he has lived beyond his means and owes Antonio heavily. Uses the arrow analogy to request more money and reveals his plan to win Portia at Belmont, comparing her to the Golden Fleece.</p>
            </div>
          </div>
          <div class="char-profile searchable-card">
            <div class="char-header">
              <div class="char-avatar" style="border-color: var(--color-success); color: var(--color-success); background-color: rgba(16, 185, 129, 0.2);">G</div>
              <div>
                <h3 class="char-title">Gratiano</h3>
                <span class="char-subtitle">The Witty Companion</span>
              </div>
            </div>
            <div class="char-body">
              <div class="trait-list">
                <span class="trait-tag">Talkative</span>
                <span class="trait-tag">Cheerful</span>
                <span class="trait-tag">Philosophical</span>
              </div>
              <p class="char-desc">Delivers a spirited speech urging Antonio to enjoy life rather than brood. His comic energy contrasts sharply with Antonio's melancholy and provides the scene's humour.</p>
            </div>
          </div>
        </div>
      </section>

      <section id="themes">
        <div class="section-header">
          <h2 class="section-title">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/></svg>
            Core Themes
          </h2>
        </div>
        <div class="themes-grid">
          <div class="theme-card searchable-card">
            <div class="theme-icon-container">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            </div>
            <h3 class="theme-title">Friendship &amp; Loyalty</h3>
            <p class="theme-text">Antonio's willingness to risk everything for Bassanio — "My purse, my person, my extremest means lie all unlocked" — establishes friendship as the play's driving force.</p>
          </div>
          <div class="theme-card searchable-card">
            <div class="theme-icon-container" style="color: var(--color-primary); background-color: rgba(251,191,36,0.1); border-color: rgba(251,191,36,0.2);">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>
            </div>
            <h3 class="theme-title">Melancholy</h3>
            <p class="theme-text">Antonio's unexplained sadness sets a reflective tone. The "world as a stage" metaphor suggests fate and predetermined roles in human life.</p>
          </div>
          <div class="theme-card searchable-card">
            <div class="theme-icon-container" style="color: var(--color-success); background-color: rgba(16,185,129,0.1); border-color: rgba(16,185,129,0.2);">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            </div>
            <h3 class="theme-title">Wealth &amp; Risk</h3>
            <p class="theme-text">Salarino's vivid ship imagery highlights the dangers of maritime trade. Antonio's diversified investments and Bassanio's debts introduce the play's economic tensions.</p>
          </div>
          <div class="theme-card searchable-card">
            <div class="theme-icon-container" style="color: #f472b6; background-color: rgba(244,114,182,0.1); border-color: rgba(244,114,182,0.2);">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            </div>
            <h3 class="theme-title">Love &amp; Courtship</h3>
            <p class="theme-text">Bassanio's description of Portia as the Golden Fleece introduces the romantic quest that parallels the financial plot.</p>
          </div>
        </div>
      </section>

      <section id="quotations">
        <div class="section-header">
          <h2 class="section-title">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21c3 0 7-9 7-14a5 5 0 0 0-10 0c0 5 4 14 7 14zm11 0c3 0 7-9 7-14a5 5 0 0 0-10 0c0 5 4 14 7 14z"/></svg>
            Key Quotations
          </h2>
        </div>
        <div class="quote-card searchable-card">
          <div class="quote-text">"In sooth I know not why I am so sad."</div>
          <button class="quote-analysis-toggle">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
            Show Significance
          </button>
          <div class="quote-analysis-container">
            <div class="quote-analysis">Antonio's opening line establishes the play's mood of mystery and melancholy. His sadness has no clear cause, deepening audience curiosity.</div>
          </div>
        </div>
        <div class="quote-card searchable-card">
          <div class="quote-text">"I hold the world but as the world, Gratiano, A stage where every man must play a part, And mine a sad one."</div>
          <button class="quote-analysis-toggle">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
            Show Significance
          </button>
          <div class="quote-analysis-container">
            <div class="quote-analysis">A famous metaphor comparing life to theatre. It reflects Renaissance ideas about fate and reinforces Antonio's acceptance of his sorrowful disposition.</div>
          </div>
        </div>
        <div class="quote-card searchable-card">
          <div class="quote-text">"My purse, my person, my extremest means lie all unlocked to your occasions."</div>
          <button class="quote-analysis-toggle">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
            Show Significance
          </button>
          <div class="quote-analysis-container">
            <div class="quote-analysis">Demonstrates Antonio's extraordinary generosity. This unconditional support leads directly to the bond with Shylock.</div>
          </div>
        </div>
        <div class="quote-card searchable-card">
          <div class="quote-text">"Her sunny locks hang on her temples like a golden fleece, which makes her seat of Belmont Colchos' strond, and many Jasons come in quest of her."</div>
          <button class="quote-analysis-toggle">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
            Show Significance
          </button>
          <div class="quote-analysis-container">
            <div class="quote-analysis">Bassanio uses mythological allusion (Jason and the Golden Fleece) to elevate Portia's importance and frame courtship as a heroic quest.</div>
          </div>
        </div>
        <div class="quote-card searchable-card">
          <div class="quote-text">"Thou know'st that all my fortunes are at sea."</div>
          <button class="quote-analysis-toggle">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
            Show Significance
          </button>
          <div class="quote-analysis-container">
            <div class="quote-analysis">Antonio has no ready cash, yet commits to borrowing on credit. This foreshadows the Shylock bond and the play's central conflict.</div>
          </div>
        </div>
      </section>

      <section id="revision-tracker">
        <div class="section-header">
          <h2 class="section-title">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
            Revision &amp; Exam Tips
          </h2>
        </div>
        <div class="tips-layout">
          <div class="tips-box searchable-card">
            <h3 style="font-family: var(--font-serif); font-size: 1.25rem; margin-bottom: 16px; color: var(--color-primary);">How to Score Well</h3>
            <ul class="tips-list">
              <li class="tips-item"><span class="tip-number">1</span><div><strong>Opening mood:</strong> Explain Antonio's melancholy and why it remains unexplained — a common exam focus.</div></li>
              <li class="tips-item"><span class="tip-number">2</span><div><strong>Friendship:</strong> Quote Antonio's offer to Bassanio when answering questions about their bond.</div></li>
              <li class="tips-item"><span class="tip-number">3</span><div><strong>Stage metaphor:</strong> Analyse "the world as a stage" as a literary device and philosophical idea.</div></li>
              <li class="tips-item"><span class="tip-number">4</span><div><strong>Golden Fleece:</strong> Identify the mythological allusion in Bassanio's Portia speech.</div></li>
              <li class="tips-item"><span class="tip-number">5</span><div><strong>Plot link:</strong> Connect Scene 1 to Scene 3 — Antonio's promise leads to the Shylock bond.</div></li>
            </ul>
          </div>
          <div class="tips-box">
            <h3 style="font-family: var(--font-serif); font-size: 1.25rem; margin-bottom: 16px; color: var(--color-primary);">Revision Checklist</h3>
            <div class="revision-progress-container">
              <div class="progress-header"><span>Revision Completed</span><span id="progress-percent">0%</span></div>
              <div class="progress-bar-bg"><div class="progress-bar-fill" id="progress-fill"></div></div>
            </div>
            <div class="checklist-container" id="revision-list">
              <label class="checklist-item"><input type="checkbox" class="checklist-checkbox" id="rev-melancholy"><span class="checklist-label">Understand Antonio's unexplained sadness</span></label>
              <label class="checklist-item"><input type="checkbox" class="checklist-checkbox" id="rev-ships"><span class="checklist-label">Explain Salarino's ship imagery and Antonio's response</span></label>
              <label class="checklist-item"><input type="checkbox" class="checklist-checkbox" id="rev-gratiano"><span class="checklist-label">Summarise Gratiano's philosophy of life</span></label>
              <label class="checklist-item"><input type="checkbox" class="checklist-checkbox" id="rev-stage"><span class="checklist-label">Analyse the "world as a stage" metaphor</span></label>
              <label class="checklist-item"><input type="checkbox" class="checklist-checkbox" id="rev-arrow"><span class="checklist-label">Explain Bassanio's arrow analogy</span></label>
              <label class="checklist-item"><input type="checkbox" class="checklist-checkbox" id="rev-portia"><span class="checklist-label">Describe how Portia is introduced (Golden Fleece)</span></label>
              <label class="checklist-item"><input type="checkbox" class="checklist-checkbox" id="rev-promise"><span class="checklist-label">Link Antonio's promise to the Shylock bond in Scene 3</span></label>
            </div>
          </div>
        </div>
      </section>
    </main>

    <footer>
      <p>Act 1 Scene 1 • Line-by-line study guide for ICSE • <a href="drama.html" style="color:var(--color-primary);text-decoration:none;">Back to all scenes</a></p>
    </footer>
  </div>

  <script src="app.js"></script>
</body>
</html>"""

out = r"C:\Projects\myprojects\debismita\act1-scene1.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(page)

print(f"Generated {out}")
print(f"Sections: {len(sections)}, Lines: {sum(len(s['lines']) for s in sections)}")