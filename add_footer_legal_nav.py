#!/usr/bin/env python3
"""
Script to add legal footer navigation to all HTML files.
Adds: Disclaimer, Privacy, Terms links in a <nav> element.
"""

import os
import re
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent

# The legal footer nav to add
LEGAL_FOOTER_NAV = '''    <nav class="footer-links" aria-label="Footer">
      <a href="/legal/disclaimer.html">Disclaimer</a>
      <a href="/legal/privacy.html">Privacy</a>
      <a href="/legal/terms.html">Terms</a>
    </nav>'''

def has_legal_footer_nav(content):
    """Check if content already has the legal footer nav."""
    return bool(re.search(r'<nav[^>]*class=["\']footer-links["\'][^>]*aria-label=["\']Footer["\']', content, re.IGNORECASE))

def add_legal_footer_nav(file_path, dry_run=False):
    """Add legal footer navigation to an HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has legal footer nav
        if has_legal_footer_nav(content):
            print(f"✓ {file_path.relative_to(PROJECT_ROOT)} - Already has legal footer nav")
            return False
        
        # Find the footer-legal section or the closing </footer> tag
        # We want to add the legal nav AFTER the existing footer-links (if any)
        # and BEFORE the footer-legal section
        
        # Pattern 1: Look for footer-legal div
        footer_legal_pattern = r'(\s*)<div class=["\']container footer-legal["\']>'
        
        if re.search(footer_legal_pattern, content):
            # Add before footer-legal
            updated_content = re.sub(
                footer_legal_pattern,
                f'\n{LEGAL_FOOTER_NAV}\n\n\\1<div class="container footer-legal">',
                content,
                count=1
            )
            action = "Added before footer-legal"
        else:
            # Pattern 2: Look for closing </footer> tag
            footer_close_pattern = r'(\s*)</footer>'
            
            if re.search(footer_close_pattern, content):
                updated_content = re.sub(
                    footer_close_pattern,
                    f'\n{LEGAL_FOOTER_NAV}\n\\1</footer>',
                    content,
                    count=1
                )
                action = "Added before </footer>"
            else:
                print(f"⚠ {file_path.relative_to(PROJECT_ROOT)} - No suitable footer location found")
                return False
        
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
        
        print(f"{'[DRY RUN] ' if dry_run else ''}✓ {action}: {file_path.relative_to(PROJECT_ROOT)}")
        return True
    
    except Exception as e:
        print(f"✗ Error processing {file_path.relative_to(PROJECT_ROOT)}: {e}")
        return False

def find_html_files():
    """Find all HTML files in the project."""
    html_files = []
    
    # Find all .html files recursively
    for html_file in PROJECT_ROOT.rglob("*.html"):
        # Skip files in certain directories if needed
        if ".git" in html_file.parts:
            continue
        html_files.append(html_file)
    
    return sorted(html_files)

def main():
    """Main execution function."""
    print("=" * 70)
    print("Legal Footer Navigation Updater")
    print("Adding: Disclaimer | Privacy | Terms")
    print("=" * 70)
    print()
    
    # Find all HTML files
    html_files = find_html_files()
    print(f"Found {len(html_files)} HTML files\n")
    
    # Ask for confirmation
    response = input("Run in DRY RUN mode first? (y/n): ").strip().lower()
    dry_run = response == 'y'
    
    if dry_run:
        print("\n--- DRY RUN MODE (no files will be modified) ---\n")
    else:
        print("\n--- LIVE MODE (files will be modified) ---\n")
    
    # Process each file
    updated_count = 0
    for html_file in html_files:
        if add_legal_footer_nav(html_file, dry_run=dry_run):
            updated_count += 1
    
    # Summary
    print()
    print("=" * 70)
    print(f"Summary: {updated_count} file(s) {'would be' if dry_run else 'were'} modified")
    print("=" * 70)
    
    if dry_run:
        print("\nTo apply changes, run the script again and choose 'n' for dry run.")

if __name__ == "__main__":
    main()
