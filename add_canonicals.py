#!/usr/bin/env python3
"""
Script to add or update canonical URLs in all HTML files.
Domain: findyoursepticbefore.com
"""

import os
import re
from pathlib import Path

# Configuration
BASE_DOMAIN = "https://findyoursepticbefore.com"
PROJECT_ROOT = Path(__file__).parent

def get_canonical_url(file_path):
    """Generate the canonical URL based on file path."""
    relative_path = file_path.relative_to(PROJECT_ROOT)
    
    # Convert file path to URL path
    if relative_path.name == "index.html":
        # Remove index.html from path
        url_path = str(relative_path.parent).replace("\\", "/")
    else:
        # Keep the filename
        url_path = str(relative_path).replace("\\", "/")
    
    # Handle root index.html
    if url_path == "." or url_path == "index.html":
        return f"{BASE_DOMAIN}/"
    
    # Ensure trailing slash for directory-based URLs
    if not url_path.endswith(".html"):
        url_path = url_path + "/"
    
    return f"{BASE_DOMAIN}/{url_path}"

def has_canonical(content):
    """Check if content already has a canonical tag."""
    return bool(re.search(r'<link\s+rel=["\']canonical["\']', content, re.IGNORECASE))

def get_canonical_tag(content):
    """Extract existing canonical tag if present."""
    match = re.search(r'<link\s+rel=["\']canonical["\'][^>]*>', content, re.IGNORECASE)
    return match.group(0) if match else None

def add_or_update_canonical(file_path, dry_run=False):
    """Add or update canonical URL in an HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        canonical_url = get_canonical_url(file_path)
        new_canonical = f'<link rel="canonical" href="{canonical_url}" />'
        
        # Check if canonical already exists
        if has_canonical(content):
            old_canonical = get_canonical_tag(content)
            
            # Check if it needs updating
            if canonical_url in old_canonical:
                print(f"✓ {file_path.relative_to(PROJECT_ROOT)} - Already correct")
                return False
            
            # Update existing canonical
            updated_content = re.sub(
                r'<link\s+rel=["\']canonical["\'][^>]*>',
                new_canonical,
                content,
                flags=re.IGNORECASE
            )
            action = "Updated"
        else:
            # Add new canonical tag before </head>
            if '</head>' in content:
                updated_content = content.replace('</head>', f'{new_canonical}\n</head>')
                action = "Added"
            else:
                print(f"⚠ {file_path.relative_to(PROJECT_ROOT)} - No </head> tag found")
                return False
        
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
        
        print(f"{'[DRY RUN] ' if dry_run else ''}✓ {action}: {file_path.relative_to(PROJECT_ROOT)}")
        print(f"  → {canonical_url}")
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
    print("Canonical URL Updater")
    print(f"Domain: {BASE_DOMAIN}")
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
        if add_or_update_canonical(html_file, dry_run=dry_run):
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
