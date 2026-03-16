#!/usr/bin/env python3
"""
Strategic internal linking improvements to boost from MODERATE to STRONG.
Adds contextual links, cross-references, and related resources sections.
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

# Strategic link additions for each page
LINK_ADDITIONS = {
    # Main tank guide - add lid, depth, before-you-dig links
    "how-to-find-your-septic-tank/index.html": [
        {
            "find": "before digging, pumping, inspection, or yard work",
            "replace": "before <a href=\"/before-you-dig/\">digging</a>, pumping, inspection, or yard work",
            "description": "Link 'digging' to before-you-dig guide"
        },
        {
            "find": "Once you feel the solid surface of the lid",
            "replace": "Once you feel the solid surface of the <a href=\"/how-to-find-your-septic-tank-lid/\">lid</a>",
            "description": "Link 'lid' to tank lid guide"
        },
        {
            "find": "Most residential tanks are buried between 6 inches to 2 feet",
            "replace": "Most residential tanks are <a href=\"/how-deep-is-my-septic-tank-buried/\">buried between 6 inches to 2 feet</a>",
            "description": "Link burial depth info"
        },
    ],
    
    # Septic lines guide - add before-you-dig, electronic locator
    "how-to-locate-septic-lines/index.html": [
        {
            "find": "before digging, trenching, fencing, or landscaping",
            "replace": "before <a href=\"/before-you-dig/\">digging</a>, trenching, fencing, or landscaping",
            "description": "Link 'digging' to safety guide"
        },
        {
            "find": "professional locating methods",
            "replace": "<a href=\"/electronic-septic-locator/\">professional locating methods</a>",
            "description": "Link to electronic locator guide"
        },
    ],
    
    # Drain field guide - add before-you-dig, depth
    "how-to-find-your-drain-field/index.html": [
        {
            "find": "before digging, planting, grading, or planning property work",
            "replace": "before <a href=\"/before-you-dig/\">digging</a>, planting, grading, or planning property work",
            "description": "Link 'digging' to safety guide"
        },
        {
            "find": "Drain field pipes are usually installed fairly shallow",
            "replace": "Drain field pipes are usually installed <a href=\"/how-deep-is-my-septic-tank-buried/\">fairly shallow</a>",
            "description": "Link to depth guide"
        },
    ],
    
    # Distribution box guide - add electronic locator
    "how-to-find-a-distribution-box/index.html": [
        {
            "find": "professional locating the safer option",
            "replace": "<a href=\"/electronic-septic-locator/\">professional locating</a> the safer option",
            "description": "Link to electronic locator"
        },
        {
            "find": "before digging or yard work",
            "replace": "before <a href=\"/before-you-dig/\">digging or yard work</a>",
            "description": "Link to safety guide"
        },
    ],
    
    # Tank lid guide - add depth, tank guide, before-you-dig
    "how-to-find-your-septic-tank-lid/index.html": [
        {
            "find": "If the tank location is unclear, start with the",
            "replace": "If the <a href=\"/how-to-find-your-septic-tank/\">tank location</a> is unclear, start with the",
            "description": "Link to main tank guide"
        },
        {
            "find": "lids buried 6 to 24 inches below the surface",
            "replace": "lids <a href=\"/how-deep-is-my-septic-tank-buried/\">buried 6 to 24 inches below the surface</a>",
            "description": "Link to depth guide"
        },
        {
            "find": "before pumping or inspection",
            "replace": "before pumping or <a href=\"/before-you-dig/\">inspection</a>",
            "description": "Link to safety guide"
        },
    ],
    
    # Records guide - add septic-records-finder
    "using-property-records-to-locate-a-septic-system/index.html": [
        {
            "find": "county or local health records",
            "replace": "<a href=\"/septic-records-finder/\">county or local health records</a>",
            "description": "Link to records finder"
        },
    ],
}

# Add "Related Resources" sections to orphaned pages
RELATED_SECTIONS = {
    "before-you-dig/index.html": '''
    <section class="section section-soft">
      <div class="container">
        <div class="section-heading">
          <p class="section-eyebrow">Related Guides</p>
          <h2>Learn more about septic system location</h2>
        </div>

        <div class="target-grid">
          <article class="target-card">
            <h3>How to find your septic tank</h3>
            <p>Locate the tank before starting any digging or landscaping projects.</p>
            <a href="/how-to-find-your-septic-tank/">Read the tank guide</a>
          </article>

          <article class="target-card">
            <h3>How to locate septic lines</h3>
            <p>Understand where buried wastewater lines may run across your property.</p>
            <a href="/how-to-locate-septic-lines/">Read the lines guide</a>
          </article>

          <article class="target-card">
            <h3>How to find your drain field</h3>
            <p>Identify the drain field area to avoid damage during yard work.</p>
            <a href="/how-to-find-your-drain-field/">Read the drain field guide</a>
          </article>

          <article class="target-card">
            <h3>Electronic septic locator tools</h3>
            <p>Learn about professional detection equipment for buried systems.</p>
            <a href="/electronic-septic-locator/">Explore locator tools</a>
          </article>
        </div>
      </div>
    </section>
''',
    
    "electronic-septic-locator/index.html": '''
    <section class="section section-soft">
      <div class="container">
        <div class="section-heading">
          <p class="section-eyebrow">Related Guides</p>
          <h2>Other septic location methods</h2>
        </div>

        <div class="target-grid">
          <article class="target-card">
            <h3>How to find your septic tank</h3>
            <p>Start with basic location methods before using electronic tools.</p>
            <a href="/how-to-find-your-septic-tank/">Read the tank guide</a>
          </article>

          <article class="target-card">
            <h3>Using property records</h3>
            <p>Check permits and site plans before investing in detection equipment.</p>
            <a href="/using-property-records-to-locate-a-septic-system/">Read the records guide</a>
          </article>

          <article class="target-card">
            <h3>Before you dig</h3>
            <p>Safety guidance for avoiding septic damage during yard projects.</p>
            <a href="/before-you-dig/">Read the safety guide</a>
          </article>

          <article class="target-card">
            <h3>How deep is my septic tank buried?</h3>
            <p>Understanding burial depth helps with detection tool selection.</p>
            <a href="/how-deep-is-my-septic-tank-buried/">Learn about depth</a>
          </article>
        </div>
      </div>
    </section>
''',
    
    "how-deep-is-my-septic-tank-buried/index.html": '''
    <section class="section section-soft">
      <div class="container">
        <div class="section-heading">
          <p class="section-eyebrow">Related Guides</p>
          <h2>Find your septic system components</h2>
        </div>

        <div class="target-grid">
          <article class="target-card">
            <h3>How to find your septic tank</h3>
            <p>Use depth knowledge to narrow your tank search area.</p>
            <a href="/how-to-find-your-septic-tank/">Read the tank guide</a>
          </article>

          <article class="target-card">
            <h3>How to find your septic tank lid</h3>
            <p>Locate buried lids for pumping and inspection access.</p>
            <a href="/how-to-find-your-septic-tank-lid/">Read the lid guide</a>
          </article>

          <article class="target-card">
            <h3>How to locate septic lines</h3>
            <p>Understanding pipe depth helps avoid damage during digging.</p>
            <a href="/how-to-locate-septic-lines/">Read the lines guide</a>
          </article>

          <article class="target-card">
            <h3>Before you dig</h3>
            <p>Essential safety guidance before excavating near septic components.</p>
            <a href="/before-you-dig/">Read the safety guide</a>
          </article>
        </div>
      </div>
    </section>
''',
    
    "septic-records-finder/index.html": '''
    <section class="section section-soft">
      <div class="container">
        <div class="section-heading">
          <p class="section-eyebrow">Related Resources</p>
          <h2>After finding records</h2>
        </div>

        <div class="target-grid">
          <article class="target-card">
            <h3>Using property records guide</h3>
            <p>Learn how to interpret septic permits and site plans effectively.</p>
            <a href="/using-property-records-to-locate-a-septic-system/">Read the full guide</a>
          </article>

          <article class="target-card">
            <h3>Search all 50 states</h3>
            <p>Interactive database to find septic records by state.</p>
            <a href="/septic-records-by-state/">Search state records</a>
          </article>

          <article class="target-card">
            <h3>How to find your septic tank</h3>
            <p>Use records to narrow down the tank location on your property.</p>
            <a href="/how-to-find-your-septic-tank/">Read the tank guide</a>
          </article>

          <article class="target-card">
            <h3>Before you dig</h3>
            <p>Safety guidance once you've identified the system location.</p>
            <a href="/before-you-dig/">Read the safety guide</a>
          </article>
        </div>
      </div>
    </section>
''',
}

def add_contextual_links(file_path, dry_run=False):
    """Add contextual inline links to guide content."""
    rel_path = str(file_path.relative_to(PROJECT_ROOT)).replace('\\', '/')
    
    if rel_path not in LINK_ADDITIONS:
        return False, "No links configured for this page"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changes_made = 0
        for link_config in LINK_ADDITIONS[rel_path]:
            find_text = link_config["find"]
            replace_text = link_config["replace"]
            
            # Only replace if the link doesn't already exist
            if find_text in content and replace_text not in content:
                content = content.replace(find_text, replace_text, 1)
                changes_made += 1
        
        if changes_made > 0:
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            return True, f"Added {changes_made} contextual link(s)"
        else:
            return False, "Links already exist"
    
    except Exception as e:
        return False, f"Error: {e}"

def add_related_section(file_path, dry_run=False):
    """Add Related Resources section to orphaned pages."""
    rel_path = str(file_path.relative_to(PROJECT_ROOT)).replace('\\', '/')
    
    if rel_path not in RELATED_SECTIONS:
        return False, "No related section configured"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has related section
        if 'Related Guides' in content or 'Related Resources' in content:
            return False, "Already has related section"
        
        # Add before </main>
        section_html = RELATED_SECTIONS[rel_path]
        content = content.replace('</main>', f'{section_html}\n  </main>')
        
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return True, "Added Related Resources section"
    
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Run internal linking improvements."""
    print("="*70)
    print("Internal Linking Boost: MODERATE → STRONG")
    print("="*70)
    print()
    
    response = input("Run in DRY RUN mode first? (y/n): ").strip().lower()
    dry_run = response == 'y'
    
    if dry_run:
        print("\n--- DRY RUN MODE ---\n")
    else:
        print("\n--- LIVE MODE ---\n")
    
    print("ADDING CONTEXTUAL INLINE LINKS:")
    print("-" * 70)
    
    contextual_count = 0
    for rel_path in LINK_ADDITIONS.keys():
        file_path = PROJECT_ROOT / rel_path
        if file_path.exists():
            changed, msg = add_contextual_links(file_path, dry_run)
            if changed:
                contextual_count += 1
                print(f"{'[DRY] ' if dry_run else ''}✓ {rel_path} - {msg}")
            else:
                print(f"  {rel_path} - {msg}")
    
    print(f"\nContextual links: {contextual_count} page(s) {'would be' if dry_run else 'were'} updated\n")
    
    print("ADDING RELATED RESOURCES SECTIONS:")
    print("-" * 70)
    
    related_count = 0
    for rel_path in RELATED_SECTIONS.keys():
        file_path = PROJECT_ROOT / rel_path
        if file_path.exists():
            changed, msg = add_related_section(file_path, dry_run)
            if changed:
                related_count += 1
                print(f"{'[DRY] ' if dry_run else ''}✓ {rel_path} - {msg}")
            else:
                print(f"  {rel_path} - {msg}")
    
    print(f"\nRelated sections: {related_count} page(s) {'would be' if dry_run else 'were'} updated\n")
    
    print("="*70)
    print(f"Total: {contextual_count + related_count} updates")
    print("="*70)
    
    if dry_run:
        print("\nTo apply changes, run again and choose 'n' for dry run.")
    else:
        print("\n✓ Run check_internal_linking.py again to verify STRONG status!")

if __name__ == "__main__":
    main()
