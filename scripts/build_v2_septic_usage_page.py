#!/usr/bin/env python3
"""Build the production V2 septic usage page from the prepared state payload."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "docs" / "usgs-septic-density-analysis" / "v2-state-payload.json"
OUT = ROOT / "septic-system-usage-by-state" / "index.html"


def load_states() -> list[dict]:
    data = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    return data["states"]


def js_string(value: str) -> str:
    return json.dumps(value)


def build_state_options(states: list[dict]) -> str:
    options = ['              <option value="">-- Select a State --</option>']
    for state in states:
        options.append(f'              <option value="{state["abbr"]}">{state["state"]}</option>')
    options.append('              <option value="AK">Alaska</option>')
    options.append('              <option value="HI">Hawaii</option>')
    options.append('              <option value="OTHER">Other / National Context</option>')
    return "\n".join(options)


def build_state_data(states: list[dict]) -> str:
    items = []
    for state in states:
        metrics = state["metrics"]
        items.append(
            f'''      {json.dumps(state["abbr"])}: {{
        name: {js_string(state["state"])},
        modernSignal: {js_string(state["modern_signal"])},
        exposure: {js_string(f"Modeled medium-estimate exposure rank #{metrics['count_rank']} by count and #{metrics['density_rank']} by statewide density.")},
        blockGroupSignal: {js_string(f"{metrics['predicted_septic_block_group_pct']}% of block groups show a medium-estimate septic-supported signal.")},
        confidence: {js_string(state["confidence_note"])},
        urbanCaution: {js_string(state["urban_suburban_caution"])},
        nextStep: {js_string(state["best_next_step"])},
        metrics: {{
          countRank: {metrics["count_rank"]},
          densityRank: {metrics["density_rank"]},
          septicBlockGroupPct: {metrics["predicted_septic_block_group_pct"]},
          parcelGapPct: {metrics["parcel_gap_pct"]}
        }}
      }}'''
        )
    for abbr, name in (("AK", "Alaska"), ("HI", "Hawaii")):
        items.append(
            f'''      {json.dumps(abbr)}: {{
        name: {js_string(name)},
        modernSignal: "Not summarized in the conterminous-U.S. USGS rollup",
        exposure: "The USGS septic-density files used for this V2 analysis summarize the conterminous United States, so this page does not assign a modeled density rank for {name}.",
        blockGroupSignal: "Use local wastewater, health department, and property records for this state.",
        confidence: "Do not infer low risk from missing USGS rollup data. The right answer is still property-specific.",
        urbanCaution: "A developed-looking property can still need wastewater verification before digging.",
        nextStep: "Confirm sewer connection records or local onsite wastewater records, call 811 before digging, and use septic-specific locating when the system layout is unclear.",
        metrics: {{
          countRank: null,
          densityRank: null,
          septicBlockGroupPct: null,
          parcelGapPct: null
        }}
      }}'''
        )
    items.append(
        '''      OTHER: {
        name: "National Context",
        modernSignal: "Property-specific verification needed",
        exposure: "National averages are useful context, but they do not answer whether one address has septic.",
        blockGroupSignal: "Use state and local records when the property status is unclear.",
        confidence: "The safest answer comes from sewer billing, local records, 811, and septic-specific locating when needed.",
        urbanCaution: "A developed-looking neighborhood does not prove a home is connected to municipal sewer.",
        nextStep: "Confirm whether the home has a sewer account or local sewer connection record. If not clear, check health department records and consider septic-specific locating before digging.",
        metrics: {
          countRank: null,
          densityRank: null,
          septicBlockGroupPct: null,
          parcelGapPct: null
        }
      }'''
    )
    return ",\n".join(items)


def main() -> int:
    states = load_states()
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Septic System Usage by State | Historical Reliance and Modern Density Signals</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta
    name="description"
    content="Use historical Census data, EPA context, and USGS modeled septic-density signals to understand when septic records or private locating may matter before digging, fencing, landscaping, or yard work."
  />
  <meta name="robots" content="index,follow" />
  <link rel="canonical" href="https://findyoursepticbefore.com/septic-system-usage-by-state/" />
  <link rel="stylesheet" href="/assets/styles.css" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <style>
    .signal-panel {{
      background: linear-gradient(135deg, #fffdf9 0%, #f1ebe1 100%);
      border: 1px solid rgba(214, 203, 187, 0.95);
      border-left: 6px solid var(--grass);
      border-radius: 0 var(--radius-xl) var(--radius-xl) 0;
      padding: 1.35rem;
      box-shadow: var(--shadow-sm);
    }}

    .signal-panel h2,
    .signal-panel h3 {{
      margin-top: 0;
    }}

    .pill-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.7rem;
      margin-top: 1.2rem;
    }}

    .info-pill {{
      display: inline-flex;
      align-items: center;
      min-height: 34px;
      padding: 0.4rem 0.75rem;
      border: 1px solid rgba(214, 203, 187, 0.95);
      border-radius: 999px;
      background: var(--surface);
      color: var(--text-soft);
      font-size: 0.85rem;
      font-weight: 800;
    }}

    .state-tool {{
      display: grid;
      grid-template-columns: minmax(240px, 0.72fr) minmax(0, 1.28fr);
      gap: 22px;
      align-items: start;
    }}

    .state-select-card,
    .result-card,
    .rank-card,
    .attribution-box {{
      background: var(--surface);
      border: 1px solid rgba(214, 203, 187, 0.95);
      border-radius: var(--radius-xl);
      padding: 1.25rem;
      box-shadow: var(--shadow-sm);
    }}

    .state-select-card label {{
      display: block;
      margin-bottom: 0.55rem;
      color: var(--heading);
      font-weight: 850;
    }}

    .state-select-card select {{
      width: 100%;
      min-height: 52px;
      padding: 0.8rem 0.9rem;
      border: 2px solid var(--line);
      border-radius: var(--radius-md);
      background: #fff;
      color: var(--text);
      font: inherit;
      cursor: pointer;
    }}

    .state-select-card select:focus {{
      border-color: var(--grass);
      outline: 3px solid rgba(79, 115, 55, 0.14);
      outline-offset: 0;
    }}

    .result-card {{
      display: none;
      gap: 0.85rem;
    }}

    .result-card.is-visible {{
      display: grid;
      animation: fadeUp 0.25s ease;
    }}

    .result-card h3 {{
      margin: 0;
      font-family: var(--font-display);
      font-size: clamp(1.8rem, 3vw, 2.35rem);
      line-height: 1.1;
    }}

    .result-row {{
      padding: 0.9rem;
      border-radius: var(--radius-md);
      background: var(--surface-2);
    }}

    .result-row strong {{
      display: block;
      color: var(--heading);
      line-height: 1.35;
    }}

    .rank-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 18px;
    }}

    .rank-card {{
      border-radius: var(--radius-lg);
    }}

    .rank-card ol {{
      margin: 0;
      padding-left: 1.35rem;
    }}

    .rank-card li {{
      margin: 0.2rem 0;
      color: var(--text-soft);
    }}

    .subtle-link-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 18px;
    }}

    .subtle-link-grid p {{
      margin: 0;
      padding: 1rem;
      background: var(--surface);
      border: 1px solid rgba(214, 203, 187, 0.95);
      border-radius: var(--radius-lg);
      color: var(--text-soft);
    }}

    .method-note {{
      color: var(--text-faint);
      font-size: 0.92rem;
    }}

    @keyframes fadeUp {{
      from {{
        opacity: 0;
        transform: translateY(8px);
      }}
      to {{
        opacity: 1;
        transform: translateY(0);
      }}
    }}

    @media (max-width: 860px) {{
      .state-tool,
      .rank-grid,
      .subtle-link-grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>

  <header class="site-header" id="top">
    <div class="container header-shell">
      <a class="site-brand" href="/" aria-label="Septic System Locator Guide home">
        <span class="brand-mark" aria-hidden="true">v</span>
        <span class="brand-text">Septic System Locator Guide</span>
      </a>

      <nav class="site-nav" aria-label="Primary navigation">
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/septic-records-by-state/">Records Search</a></li>
          <li><a href="/before-you-dig/">Before You Dig</a></li>
          <li><a href="/does-811-mark-septic-tanks/">811 Limits</a></li>
        </ul>
      </nav>

      <details class="mobile-menu">
        <summary>Menu</summary>
        <nav aria-label="Mobile navigation">
          <a href="/">Home</a>
          <a href="/septic-records-by-state/">Records Search</a>
          <a href="/before-you-dig/">Before You Dig</a>
          <a href="/does-811-mark-septic-tanks/">811 Limits</a>
        </nav>
      </details>
    </div>
  </header>

  <main id="main-content">
    <section class="hero hero-inner">
      <div class="container hero-grid">
        <div class="hero-copy">
          <p class="eyebrow">Homeowner septic risk map</p>
          <h1>Septic System Usage by State: Historical Reliance and Modern Density Signals</h1>
          <p class="hero-lead">
            Septic systems are not only a rural concern. Rural properties are easier to recognize, but septic risk can be easier to overlook in older suburbs, coastal communities, lake neighborhoods, large-lot subdivisions, and streets near the edge of municipal sewer service. This guide combines historical Census sewage-disposal data, EPA national context, and a homeowner-friendly interpretation of USGS modeled septic-density data to help you know when to check records or locate private septic components before digging.
          </p>

          <div class="hero-actions">
            <a class="button button-primary" href="#state-check">Check your state</a>
            <a class="button button-secondary" href="/does-811-mark-septic-tanks/">What 811 does not mark</a>
          </div>

          <div class="pill-row" aria-label="Page data layers">
            <span class="info-pill">Historical Census baseline</span>
            <span class="info-pill">Modern USGS density signal</span>
            <span class="info-pill">Urban/suburban caution</span>
            <span class="info-pill">Before-digging next steps</span>
          </div>
        </div>

        <aside class="signal-panel">
          <p class="section-eyebrow">Short Answer</p>
          <h2>Do not judge by neighborhood appearance.</h2>
          <p>
            If you live in a clearly rural area, septic should already be on your checklist. The bigger blind spot is the developed-looking property where the owner assumes sewer because the neighborhood has sidewalks, nearby utilities, or a city mailing address. A sewer line nearby does not prove your house is connected. Before digging, confirm the property itself.
          </p>
        </aside>
      </div>
    </section>

    <section class="summary-strip">
      <div class="container summary-grid">
        <div class="summary-item">
          <h2>Historical signal</h2>
          <p>Where septic systems were officially common in historical Census sewage-disposal data.</p>
        </div>
        <div class="summary-item">
          <h2>Modern signal</h2>
          <p>Where USGS modeled septic-density data suggests present-day septic concentration.</p>
        </div>
        <div class="summary-item">
          <h2>Practical action</h2>
          <p>What homeowners should check before posts, trenches, landscaping, pools, sheds, or additions.</p>
        </div>
      </div>
    </section>

    <section class="section" id="state-check">
      <div class="container">
        <div class="section-heading">
          <p class="section-eyebrow">State Lookup</p>
          <h2>Choose a state for a homeowner-facing septic signal.</h2>
          <p class="section-lead">
            This tool does not claim exact current septic usage by state. It turns historical and modeled data into practical before-digging guidance.
          </p>
        </div>

        <div class="state-tool">
          <div class="state-select-card">
            <label for="stateSelect">Step 1: Select your state</label>
            <select id="stateSelect">
{build_state_options(states)}
            </select>
            <p class="method-note">
              Data-informed planning signal only. Local health department files, sewer billing, permit records, 811, and septic-specific locating may still be needed.
            </p>
          </div>

          <article id="resultCard" class="result-card" aria-live="polite">
            <h3 id="resStateName">State</h3>
            <div class="result-row">
              <strong>Modern USGS signal</strong>
              <span id="resModernSignal">--</span>
            </div>
            <div class="result-row">
              <strong>Modeled exposure</strong>
              <span id="resExposure">--</span>
            </div>
            <div class="result-row">
              <strong>Block group signal</strong>
              <span id="resBlockGroupSignal">--</span>
            </div>
            <div class="result-row">
              <strong>Urban/suburban caution</strong>
              <span id="resUrbanCaution">--</span>
            </div>
            <div class="result-row">
              <strong>Data confidence</strong>
              <span id="resConfidence">--</span>
            </div>
            <div class="result-row">
              <strong>Best next step</strong>
              <span id="resNextStep">--</span>
            </div>
            <div class="hero-actions">
              <a class="button button-primary" href="tel:877-735-2796">Call 877-735-2796</a>
              <a class="button button-secondary" href="/septic-records-by-state/">Search state records</a>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="section section-tinted" id="urban-trap">
      <div class="container records-layout">
        <div class="records-copy">
          <div class="section-heading section-heading-left">
            <p class="section-eyebrow">Urban/Suburban Septic Trap</p>
            <h2>Why septic can still matter in developed-looking neighborhoods</h2>
            <p class="section-lead">
              Some properties remain on septic even after nearby sewer expansion. Some neighborhoods are partially connected. Some homes have city mailing addresses but county-level wastewater records.
            </p>
          </div>

          <p>
            Older homes, private wells, lake communities, coastal areas, large-lot suburbs, and unincorporated pockets can all create septic uncertainty even when the area does not look rural.
          </p>

          <p>
            The practical rule is simple: do not judge by neighborhood appearance. Verify the property before fence posts, landscaping, trenching, patios, pools, sheds, additions, grading, drainage work, or driveway changes.
          </p>
        </div>

        <aside class="records-panel">
          <h3>Urban/suburban checklist</h3>
          <ul>
            <li>Confirm whether the home has a municipal sewer account or wastewater bill.</li>
            <li>Check disclosures, inspection reports, closing documents, and old permit files.</li>
            <li>Search local health department or county septic records.</li>
            <li>Call 811 before digging.</li>
            <li>Do not assume 811 marks private septic tanks, lines, distribution boxes, or drain fields.</li>
            <li>Use septic-specific locating if records are missing and the work area is near a likely septic path.</li>
          </ul>
        </aside>
      </div>
    </section>

    <section class="section" id="rankings">
      <div class="container">
        <div class="section-heading">
          <p class="section-eyebrow">Modern USGS Findings</p>
          <h2>Three ways to read septic risk.</h2>
          <p class="section-lead">
            A single statewide percentage can mislead. Total exposure, density, and local septic-supported patterns answer different homeowner questions.
          </p>
        </div>

        <div class="rank-grid">
          <article class="rank-card">
            <h3>High total estimated exposure</h3>
            <p>Large states can contain many modeled septic systems even when statewide density does not look extreme.</p>
            <ol>
              <li>Texas</li>
              <li>North Carolina</li>
              <li>Pennsylvania</li>
              <li>Ohio</li>
              <li>Michigan</li>
              <li>Georgia</li>
              <li>New York</li>
              <li>Tennessee</li>
              <li>Florida</li>
              <li>Alabama</li>
            </ol>
          </article>

          <article class="rank-card">
            <h3>High statewide density signal</h3>
            <p>This supports the urban/suburban blind spot because developed-looking states can still contain septic pockets.</p>
            <ol>
              <li>Connecticut</li>
              <li>Rhode Island</li>
              <li>Massachusetts</li>
              <li>Delaware</li>
              <li>Maryland</li>
              <li>New Jersey</li>
              <li>North Carolina</li>
              <li>Ohio</li>
              <li>Pennsylvania</li>
              <li>New Hampshire</li>
            </ol>
          </article>

          <article class="rank-card">
            <h3>High septic-supported block group share</h3>
            <p>This is the rural and historical signal: broad local patterns should make homeowners records-first.</p>
            <ol>
              <li>Vermont</li>
              <li>Maine</li>
              <li>West Virginia</li>
              <li>Mississippi</li>
              <li>Arkansas</li>
              <li>South Dakota</li>
              <li>Alabama</li>
              <li>New Hampshire</li>
              <li>Kentucky</li>
              <li>Montana</li>
            </ol>
          </article>
        </div>
      </div>
    </section>

    <section class="section section-tinted">
      <div class="container">
        <div class="section-heading">
          <p class="section-eyebrow">What Homeowners Should Do</p>
          <h2>Turn uncertainty into a safer next step.</h2>
          <p class="section-lead">
            The point of the data is not to prove that a specific address has septic. The point is to know when guessing is a bad plan.
          </p>
        </div>

        <div class="target-grid">
          <article class="target-card">
            <h3>Before fence installation</h3>
            <p>Posts and gate footings can hit lines or block future tank access when the layout is unknown.</p>
            <a href="/locate-septic-before-fence-installation/">Read the fence guide</a>
          </article>
          <article class="target-card">
            <h3>Before landscaping</h3>
            <p>Tree planting, grading, drainage work, and hardscape can disturb septic components that are not visible.</p>
            <a href="/find-septic-before-landscaping/">Read the landscaping guide</a>
          </article>
          <article class="target-card">
            <h3>811 is not the whole answer</h3>
            <p>811 is still the first call before digging, but private septic components may need separate locating.</p>
            <a href="/does-811-mark-septic-tanks/">Compare 811 and septic locating</a>
          </article>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-heading">
          <p class="section-eyebrow">Local Context</p>
          <h2>State signals still need local follow-up.</h2>
          <p class="section-lead">
            These state resources are included where they naturally support local records and service context. They do not replace property-specific verification.
          </p>
        </div>

        <div class="subtle-link-grid">
          <p>In New England, older homes, private wells, lake communities, and town-level records make local context important in <a href="https://vermontsepticconnect.com" target="_blank" rel="noopener">Vermont</a>, <a href="https://mainesepticconnect.com" target="_blank" rel="noopener">Maine</a>, and <a href="https://newhampshiresepticconnect.com" target="_blank" rel="noopener">New Hampshire</a>.</p>
          <p>In the South and Appalachia, county-level records and rural/suburban growth patterns matter in <a href="https://alabamasepticconnect.com" target="_blank" rel="noopener">Alabama</a>, <a href="https://mississippisepticconnect.com" target="_blank" rel="noopener">Mississippi</a>, <a href="https://tennesseesepticconnect.com" target="_blank" rel="noopener">Tennessee</a>, and <a href="https://kentuckysepticconnect.com" target="_blank" rel="noopener">Kentucky</a>.</p>
          <p>Western states can look low by statewide density while still having rural, private-well, and unincorporated septic pockets. That is the safer way to read <a href="https://newmexicosepticconnect.com" target="_blank" rel="noopener">New Mexico septic context</a>.</p>
          <p>For any state, start with local records before digging: health department files, permit records, sewer billing, disclosures, and septic-specific locating when the layout is unclear.</p>
        </div>
      </div>
    </section>

    <section class="section section-tinted" id="attribution">
      <div class="container records-layout">
        <div class="records-copy">
          <div class="section-heading section-heading-left">
            <p class="section-eyebrow">Data Attribution</p>
            <h2>Credit and limitations</h2>
          </div>

          <div class="attribution-box">
            <p>
              This page uses and interprets public data from the U.S. Geological Survey dataset <a href="https://doi.org/10.5066/P1WCYDPB" target="_blank" rel="noopener">Estimated Densities of Residential Septic Tanks across the Conterminous United States for 12-digit Hydrologic Unit Code 12 (HUC12), National Hydrography Dataset Plus Version 2 (NHDPlusV2) Catchment, and Block Group Scales</a>.
            </p>
            <p>
              Dataset authors: Brennon K. Peterson, Stephanie E. Gordon, Brianna M. Williams, Rachel M. Atkins, Labeeb Ahmed, and Serena M. Seawolf. Publisher: U.S. Geological Survey.
            </p>
            <p>
              FindYourSepticBefore.com interpreted the public dataset for homeowner education. This page is not an official USGS ranking, USGS endorsement, or property-level septic determination. Local records, sewer billing, health department files, 811, and professional locating may still be needed.
            </p>
            <p class="method-note">
              This V2 interpretation uses the prepared state rollup from <code>docs/usgs-septic-density-analysis/state-summary.csv</code> and homeowner-facing labels from <code>docs/usgs-septic-density-analysis/v2-state-payload.json</code>. Historical context comes from Census sewage-disposal tables and EPA national septic context.
            </p>
          </div>
        </div>

        <aside class="records-panel">
          <h3>Still not sure before digging?</h3>
          <p>
            If records do not clearly show the tank, lines, distribution box, or drain field, septic-specific locating may be the practical next step before digging.
          </p>
          <a class="button button-primary" href="tel:877-735-2796">Call 877-735-2796</a>
        </aside>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container footer-shell">
      <div>
        <p class="footer-brand">Septic System Locator Guide</p>
        <p class="footer-copy">
          Practical homeowner guidance for locating septic tanks, lines, lids, and drain fields before digging, maintenance, or planning yard work.
        </p>

        <p class="footer-help">
          Need local septic help? Call <a href="tel:877-735-2796" style="color: var(--text-soft); text-decoration: none; border-bottom: 1px solid var(--line-strong);">877-735-2796</a>
        </p>
      </div>

      <aside class="footer-cta">
        <h2>Still cannot confirm the septic location?</h2>
        <p>
          If records, yard clues, and 811 markings still leave the tank, lines, or drain field unclear, local septic help may be the next practical step.
        </p>
        <a class="button" href="tel:877-735-2796">Call 877-735-2796</a>
      </aside>

      <div class="footer-links">
        <a href="/">Home</a>
        <a href="/septic-records-by-state/">Records Search</a>
        <a href="/before-you-dig/">Before You Dig</a>
      </div>
    </div>
    <nav class="footer-links" aria-label="Footer">
      <a href="/legal/disclaimer.html">Disclaimer</a>
      <a href="/legal/privacy.html">Privacy</a>
      <a href="/legal/terms.html">Terms</a>
    </nav>

    <div class="container footer-legal">
      <p>
        This site provides general educational information only. Septic system layouts vary by property, installation history, and local requirements.
      </p>
      <p>&copy; 2026 Septic System Locator Guide</p>
    </div>
  </footer>

  <script>
    const stateData = {{
{build_state_data(states)}
    }};

    const selector = document.getElementById("stateSelect");
    const card = document.getElementById("resultCard");

    selector.addEventListener("change", function () {{
      const data = stateData[this.value];
      if (!data) {{
        card.classList.remove("is-visible");
        return;
      }}

      document.getElementById("resStateName").innerText = data.name;
      document.getElementById("resModernSignal").innerText = data.modernSignal;
      document.getElementById("resExposure").innerText = data.exposure;
      document.getElementById("resBlockGroupSignal").innerText = data.blockGroupSignal;
      document.getElementById("resUrbanCaution").innerText = data.urbanCaution;
      document.getElementById("resConfidence").innerText = data.confidence;
      document.getElementById("resNextStep").innerText = data.nextStep;
      card.classList.add("is-visible");
    }});
  </script>
</body>
</html>
'''
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
