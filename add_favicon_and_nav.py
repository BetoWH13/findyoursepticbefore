#!/usr/bin/env python3
"""
Script to add favicon link and improve navigation across all HTML pages.
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

# Favicon link to add
FAVICON_LINK = '<link rel="icon" type="image/svg+xml" href="/favicon.svg" />'

# Improved navigation HTML
IMPROVED_NAV = '''      <nav class="site-nav" aria-label="Primary navigation">
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/septic-records-by-state/">Records Search</a></li>
          <li><a href="/#what-are-you-finding">Guides</a></li>
          <li><a href="/#faq">FAQ</a></li>
        </ul>
      </nav>'''

def add_favicon(file_path, dry_run=False):
    """Add favicon link to HTML file if missing."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if favicon already exists
        if 'favicon.svg' in content or 'rel="icon"' in content:
            return False, "Already has favicon"
        
        # Add favicon before </head>
        if '</head>' in content:
            updated_content = content.replace('</head>', f'  {FAVICON_LINK}\n</head>')
            
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
            
            return True, "Added favicon"
        else:
            return False, "No </head> tag found"
    
    except Exception as e:
        return False, f"Error: {e}"

def improve_nav(file_path, dry_run=False):
    """Improve navigation to include useful links."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if nav exists
        if 'class="site-nav"' not in content:
            return False, "No site-nav found"
        
        # Check if nav already has improved links
        if 'Records Search' in content and 'site-nav' in content:
            return False, "Nav already improved"
        
        # Replace old nav with improved nav
        # Pattern to match the entire nav block
        old_nav_pattern = r'<nav class="site-nav"[^>]*>.*?</nav>'
        
        if re.search(old_nav_pattern, content, re.DOTALL):
            updated_content = re.sub(
                old_nav_pattern,
                IMPROVED_NAV,
                content,
                count=1,
                flags=re.DOTALL
            )
            
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
            
            return True, "Updated navigation"
        else:
            return False, "Could not match nav pattern"
    
    except Exception as e:
        return False, f"Error: {e}"

def add_nav_to_pages_without_it(file_path, dry_run=False):
    """Add navigation to pages that don't have it."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if nav already exists
        if 'class="site-nav"' in content:
            return False, "Already has nav"
        
        # Find the header closing tag and add nav before it
        header_pattern = r'(</a>\s*)(</div>\s*</header>)'
        
        if re.search(header_pattern, content):
            nav_to_add = f'\n\n{IMPROVED_NAV}\n    '
            updated_content = re.sub(
                header_pattern,
                f'\\1{nav_to_add}\\2',
                content,
                count=1
            )
            
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
            
            return True, "Added navigation"
        else:
            return False, "Could not find header pattern"
    
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Run all updates."""
    print("="*70)
    print("Favicon and Navigation Updater")
    print("="*70)
    print()
    
    # Find all HTML files
    html_files = list(PROJECT_ROOT.rglob("*.html"))
    html_files = [f for f in html_files if ".git" not in f.parts]
    
    print(f"Found {len(html_files)} HTML files\n")
    
    response = input("Run in DRY RUN mode first? (y/n): ").strip().lower()
    dry_run = response == 'y'
    
    if dry_run:
        print("\n--- DRY RUN MODE ---\n")
    else:
        print("\n--- LIVE MODE ---\n")
    
    print("FAVICON UPDATES:")
    print("-" * 70)
    favicon_count = 0
    for html_file in sorted(html_files):
        changed, msg = add_favicon(html_file, dry_run)
        if changed:
            favicon_count += 1
            print(f"{'[DRY] ' if dry_run else ''}✓ {html_file.relative_to(PROJECT_ROOT)} - {msg}")
        elif "Already has" not in msg:
            print(f"⚠ {html_file.relative_to(PROJECT_ROOT)} - {msg}")
    
    print(f"\nFavicon: {favicon_count} file(s) {'would be' if dry_run else 'were'} updated\n")
    
    print("NAVIGATION UPDATES:")
    print("-" * 70)
    nav_count = 0
    for html_file in sorted(html_files):
        # Try to improve existing nav
        changed, msg = improve_nav(html_file, dry_run)
        if changed:
            nav_count += 1
            print(f"{'[DRY] ' if dry_run else ''}✓ {html_file.relative_to(PROJECT_ROOT)} - {msg}")
        elif "No site-nav" in msg:
            # Try to add nav if missing
            changed, msg = add_nav_to_pages_without_it(html_file, dry_run)
            if changed:
                nav_count += 1
                print(f"{'[DRY] ' if dry_run else ''}✓ {html_file.relative_to(PROJECT_ROOT)} - {msg}")
    
    print(f"\nNavigation: {nav_count} file(s) {'would be' if dry_run else 'were'} updated\n")
    
    print("="*70)
    print(f"Total: {favicon_count + nav_count} updates")
    print("="*70)
    
    if dry_run:
        print("\nTo apply changes, run again and choose 'n' for dry run.")

if __name__ == "__main__":
    main()
