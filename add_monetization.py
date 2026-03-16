#!/usr/bin/env python3
"""
Add subtle monetization elements to guide pages:
- State feeder cards linking to SepticConnect sites
- "Still stuck?" assist box with phone number
- Footer phone utility line
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
PHONE = "877-735-2796"

# Main guide pages that should get the full treatment
MAIN_GUIDE_PAGES = [
    "how-to-find-your-septic-tank/index.html",
    "how-to-locate-septic-lines/index.html",
    "how-to-find-your-drain-field/index.html",
    "how-to-find-a-distribution-box/index.html",
    "how-to-find-your-septic-tank-lid/index.html",
    "using-property-records-to-locate-a-septic-system/index.html",
]

# State feeder cards section (Layer 1)
STATE_FEEDER_SECTION = '''
    <section class="section section-soft">
      <div class="container">
        <div class="section-heading">
          <p class="section-eyebrow">When Records and Yard Clues Are Not Enough</p>
          <h2>State-specific septic guidance</h2>
          <p class="section-lead">
            If records are missing or older property files are incomplete, local septic guidance may help narrow the next practical step.
          </p>
        </div>

        <div class="target-grid">
          <article class="target-card">
            <h3>New Hampshire septic help</h3>
            <p>If records are missing or older property files are incomplete, see local septic guidance for New Hampshire.</p>
            <a href="https://newhampshiresepticconnect.com" target="_blank" rel="noopener">Visit New Hampshire guide</a>
          </article>

          <article class="target-card">
            <h3>Maine septic help</h3>
            <p>Local septic guidance for Maine properties when records or system location remain unclear.</p>
            <a href="https://mainesepticconnect.com" target="_blank" rel="noopener">Visit Maine guide</a>
          </article>

          <article class="target-card">
            <h3>Vermont septic help</h3>
            <p>Vermont-specific septic system guidance for properties with incomplete documentation.</p>
            <a href="https://vermontsepticconnect.com" target="_blank" rel="noopener">Visit Vermont guide</a>
          </article>

          <article class="target-card">
            <h3>Kentucky septic help</h3>
            <p>Local septic assistance for Kentucky homeowners when system location is still uncertain.</p>
            <a href="https://kentuckysepticconnect.com" target="_blank" rel="noopener">Visit Kentucky guide</a>
          </article>
        </div>
      </div>
    </section>
'''

# "Still stuck?" assist box (Layer 2)
ASSIST_BOX_SECTION = f'''
    <section class="section">
      <div class="container">
        <aside class="records-box" style="max-width: 680px; margin: 0 auto;">
          <h3>Still can't locate the system?</h3>
          <p>
            Records can be incomplete, and older properties do not always match the original plan. If you need the next practical step, local septic help may be appropriate.
          </p>
          <p style="margin-top: 1rem;">
            <strong>Call:</strong> <a href="tel:{PHONE}" style="color: var(--soil-dark); text-decoration: none; border-bottom: 1px solid var(--soil-mid);">{PHONE}</a>
          </p>
        </aside>
      </div>
    </section>
'''

# Footer phone utility line
FOOTER_PHONE_LINE = f'''
        <p class="footer-help">
          Need local septic help? Call <a href="tel:{PHONE}" style="color: var(--text-soft); text-decoration: none; border-bottom: 1px solid var(--line-strong);">{PHONE}</a>
        </p>
'''

def add_state_feeder_and_assist_box(file_path, dry_run=False):
    """Add state feeder cards and assist box before the closing </main> tag."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already added
        if 'When Records and Yard Clues Are Not Enough' in content:
            return False, "Already has state feeder section"
        
        # Find the closing </main> tag and add sections before it
        main_close_pattern = r'(\s*)</main>'
        
        if re.search(main_close_pattern, content):
            # Add both sections before </main>
            sections_to_add = STATE_FEEDER_SECTION + ASSIST_BOX_SECTION + '\n  '
            
            updated_content = re.sub(
                main_close_pattern,
                f'{sections_to_add}\\1</main>',
                content,
                count=1
            )
            
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
            
            return True, "Added state feeder cards and assist box"
        else:
            return False, "Could not find </main> tag"
    
    except Exception as e:
        return False, f"Error: {e}"

def add_footer_phone_line(file_path, dry_run=False):
    """Add phone utility line to footer."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already added
        if PHONE in content and 'footer-help' in content:
            return False, "Already has footer phone line"
        
        # Find footer-copy and add phone line after it
        footer_pattern = r'(</p>\s*</div>\s*<div class="footer-links">)'
        
        if re.search(footer_pattern, content):
            updated_content = re.sub(
                footer_pattern,
                f'</p>\n{FOOTER_PHONE_LINE}      </div>\n\n      <div class="footer-links">',
                content,
                count=1
            )
            
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
            
            return True, "Added footer phone line"
        else:
            return False, "Could not find footer pattern"
    
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Run monetization updates."""
    print("="*70)
    print("Subtle Monetization Updater")
    print(f"Phone: {PHONE}")
    print("="*70)
    print()
    
    response = input("Run in DRY RUN mode first? (y/n): ").strip().lower()
    dry_run = response == 'y'
    
    if dry_run:
        print("\n--- DRY RUN MODE ---\n")
    else:
        print("\n--- LIVE MODE ---\n")
    
    print("GUIDE PAGES - State Feeder Cards + Assist Box:")
    print("-" * 70)
    guide_count = 0
    for page in MAIN_GUIDE_PAGES:
        file_path = PROJECT_ROOT / page
        if file_path.exists():
            changed, msg = add_state_feeder_and_assist_box(file_path, dry_run)
            if changed:
                guide_count += 1
                print(f"{'[DRY] ' if dry_run else ''}✓ {page} - {msg}")
            else:
                print(f"  {page} - {msg}")
        else:
            print(f"⚠ {page} - File not found")
    
    print(f"\nGuide pages: {guide_count} {'would be' if dry_run else 'were'} updated\n")
    
    print("ALL PAGES - Footer Phone Line:")
    print("-" * 70)
    footer_count = 0
    
    html_files = list(PROJECT_ROOT.rglob("*.html"))
    html_files = [f for f in html_files if ".git" not in f.parts]
    
    for html_file in sorted(html_files):
        changed, msg = add_footer_phone_line(html_file, dry_run)
        if changed:
            footer_count += 1
            print(f"{'[DRY] ' if dry_run else ''}✓ {html_file.relative_to(PROJECT_ROOT)} - {msg}")
    
    print(f"\nFooter updates: {footer_count} {'would be' if dry_run else 'were'} updated\n")
    
    print("="*70)
    print(f"Total: {guide_count + footer_count} updates")
    print("="*70)
    
    if dry_run:
        print("\nTo apply changes, run again and choose 'n' for dry run.")

if __name__ == "__main__":
    main()
