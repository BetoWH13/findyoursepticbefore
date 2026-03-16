#!/usr/bin/env python3
"""
Replace current 'When Records...' section with cleaner feeder structure.
Keeps all 4 states, uses proper feeder-grid/card classes.
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
PHONE = "877-735-2796"

# Main guide pages to update
MAIN_GUIDE_PAGES = [
    "how-to-find-your-septic-tank/index.html",
    "how-to-locate-septic-lines/index.html",
    "how-to-find-your-drain-field/index.html",
    "how-to-find-a-distribution-box/index.html",
    "how-to-find-your-septic-tank-lid/index.html",
    "using-property-records-to-locate-a-septic-system/index.html",
]

# New cleaner feeder structure with all 4 states
NEW_FEEDER_SECTION = f'''
    <section class="section section-soft">
      <div class="container">
        <div class="section-heading">
          <p class="section-eyebrow">Next practical step</p>
          <h2>Need local septic help instead of more record searching?</h2>
          <p class="section-lead">
            If septic records are missing, the yard layout is unclear, or you still cannot confirm the tank, lines, or drain field location, the next step may be local septic help in your state.
          </p>
        </div>

        <div class="feeder-grid">
          <article class="feeder-card">
            <p class="feeder-tag">State help</p>
            <h3><a href="https://mainesepticconnect.com/" target="_blank" rel="noopener">Maine Septic Connect</a></h3>
            <p>Local septic information for Maine properties where records are incomplete or system location is still unclear.</p>
          </article>

          <article class="feeder-card">
            <p class="feeder-tag">State help</p>
            <h3><a href="https://newhampshiresepticconnect.com/" target="_blank" rel="noopener">New Hampshire Septic Connect</a></h3>
            <p>Guidance for New Hampshire homeowners who still need the next practical septic step.</p>
          </article>

          <article class="feeder-card">
            <p class="feeder-tag">State help</p>
            <h3><a href="https://vermontsepticconnect.com/" target="_blank" rel="noopener">Vermont Septic Connect</a></h3>
            <p>Useful when old permits, tank location clues, or drain field layouts are still uncertain.</p>
          </article>

          <article class="feeder-card">
            <p class="feeder-tag">State help</p>
            <h3><a href="https://kentuckysepticconnect.com/" target="_blank" rel="noopener">Kentucky Septic Connect</a></h3>
            <p>Local septic help for Kentucky properties when system location remains unclear.</p>
          </article>
        </div>

        <div class="feeder-note-box">
          <p>
            Still stuck? If you need the next practical step, local septic help may be appropriate.
            Call <a href="tel:{PHONE}">{PHONE}</a>.
          </p>
        </div>
      </div>
    </section>
'''

def replace_feeder_section(file_path, dry_run=False):
    """Replace old 'When Records...' section with new feeder structure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if old section exists
        if 'When Records and Yard Clues Are Not Enough' not in content:
            return False, "Old section not found"
        
        # Pattern to match the entire old section (both the state feeder AND assist box)
        # We need to remove both sections and replace with the new combined one
        old_section_pattern = r'<section class="section section-soft">.*?When Records and Yard Clues Are Not Enough.*?</section>\s*<section class="section">.*?Still can\'t locate the system\?.*?</section>'
        
        if re.search(old_section_pattern, content, re.DOTALL):
            updated_content = re.sub(
                old_section_pattern,
                NEW_FEEDER_SECTION.strip(),
                content,
                count=1,
                flags=re.DOTALL
            )
            
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
            
            return True, "Replaced with new feeder structure"
        else:
            return False, "Could not match old section pattern"
    
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Run replacement."""
    print("="*70)
    print("Feeder Structure Replacement")
    print("Replacing old sections with cleaner feeder structure (4 states)")
    print("="*70)
    print()
    
    response = input("Run in DRY RUN mode first? (y/n): ").strip().lower()
    dry_run = response == 'y'
    
    if dry_run:
        print("\n--- DRY RUN MODE ---\n")
    else:
        print("\n--- LIVE MODE ---\n")
    
    print("REPLACING FEEDER SECTIONS:")
    print("-" * 70)
    
    count = 0
    for page in MAIN_GUIDE_PAGES:
        file_path = PROJECT_ROOT / page
        if file_path.exists():
            changed, msg = replace_feeder_section(file_path, dry_run)
            if changed:
                count += 1
                print(f"{'[DRY] ' if dry_run else ''}✓ {page} - {msg}")
            else:
                print(f"  {page} - {msg}")
        else:
            print(f"⚠ {page} - File not found")
    
    print()
    print("="*70)
    print(f"Total: {count} page(s) {'would be' if dry_run else 'were'} updated")
    print("="*70)
    
    if dry_run:
        print("\nTo apply changes, run again and choose 'n' for dry run.")
    
    print("\nNote: Footer phone lines remain unchanged as requested.")

if __name__ == "__main__":
    main()
