#!/usr/bin/env python3
"""
Comprehensive navigation and link sanity check for main guide pages.
Checks for broken anchors, missing IDs, and other navigation issues.
"""

import re
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent

# Main pages to check thoroughly
MAIN_PAGES = [
    "index.html",
    "how-to-find-your-septic-tank/index.html",
    "how-to-locate-septic-lines/index.html",
    "how-to-find-your-drain-field/index.html",
    "how-to-find-a-distribution-box/index.html",
    "how-to-find-your-septic-tank-lid/index.html",
    "using-property-records-to-locate-a-septic-system/index.html",
    "before-you-dig/index.html",
    "electronic-septic-locator/index.html",
    "how-deep-is-my-septic-tank-buried/index.html",
    "septic-records-finder/index.html",
    "septic-records-by-state/index.html",
]

def extract_anchor_links(content):
    """Extract all anchor links (#something) from content."""
    # Find href="#anchor" patterns
    anchors = re.findall(r'href=["\']#([^"\']+)["\']', content)
    return anchors

def extract_ids(content):
    """Extract all id attributes from content."""
    # Find id="something" patterns
    ids = re.findall(r'id=["\']([^"\']+)["\']', content)
    return ids

def check_hero_buttons(content, file_name):
    """Check hero section buttons for broken links."""
    issues = []
    
    # Find hero-actions section
    hero_match = re.search(r'<div class="hero-actions">(.*?)</div>', content, re.DOTALL)
    if hero_match:
        hero_section = hero_match.group(1)
        
        # Find all buttons in hero
        buttons = re.findall(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', hero_section, re.DOTALL)
        
        for href, text in buttons:
            text_clean = re.sub(r'<[^>]+>', '', text).strip()
            
            # Check if it's an anchor link
            if href.startswith('#'):
                anchor = href[1:]
                # Check if this ID exists in the page
                if f'id="{anchor}"' not in content and f"id='{anchor}'" not in content:
                    issues.append(f"Broken anchor in hero button: '{text_clean}' → {href}")
    
    return issues

def check_meta_description(content, file_name):
    """Check meta description for HTML tags."""
    issues = []
    
    meta_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', content)
    if meta_match:
        desc = meta_match.group(1)
        if '<' in desc or '>' in desc:
            issues.append(f"HTML tags in meta description: {desc[:80]}...")
    
    return issues

def check_internal_anchors(content, file_name):
    """Check that all internal anchor links have corresponding IDs."""
    issues = []
    
    anchors = extract_anchor_links(content)
    ids = extract_ids(content)
    
    for anchor in anchors:
        if anchor not in ids:
            issues.append(f"Broken anchor link: #{anchor} (ID not found on page)")
    
    return issues

def check_duplicate_ids(content, file_name):
    """Check for duplicate IDs."""
    issues = []
    
    ids = extract_ids(content)
    id_counts = defaultdict(int)
    
    for id_val in ids:
        id_counts[id_val] += 1
    
    for id_val, count in id_counts.items():
        if count > 1:
            issues.append(f"Duplicate ID: '{id_val}' appears {count} times")
    
    return issues

def check_empty_links(content, file_name):
    """Check for empty or broken href attributes."""
    issues = []
    
    # Find links with empty or just # href
    empty_links = re.findall(r'<a[^>]*href=["\'](["\']|#["\'])', content)
    if empty_links:
        issues.append(f"Found {len(empty_links)} empty or incomplete href attributes")
    
    return issues

def main():
    """Run comprehensive navigation checks."""
    print("="*70)
    print("Navigation & Link Sanity Check")
    print("="*70)
    print()
    
    all_issues = {}
    total_issues = 0
    
    for page_path in MAIN_PAGES:
        file_path = PROJECT_ROOT / page_path
        
        if not file_path.exists():
            print(f"⚠ {page_path} - File not found")
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            page_issues = []
            
            # Run all checks
            page_issues.extend(check_hero_buttons(content, page_path))
            page_issues.extend(check_meta_description(content, page_path))
            page_issues.extend(check_internal_anchors(content, page_path))
            page_issues.extend(check_duplicate_ids(content, page_path))
            page_issues.extend(check_empty_links(content, page_path))
            
            if page_issues:
                all_issues[page_path] = page_issues
                total_issues += len(page_issues)
        
        except Exception as e:
            print(f"✗ {page_path} - Error: {e}")
    
    # Print results
    if all_issues:
        print("ISSUES FOUND:")
        print("-" * 70)
        for page, issues in all_issues.items():
            print(f"\n{page}:")
            for issue in issues:
                print(f"  ✗ {issue}")
    else:
        print("✓ NO ISSUES FOUND!")
        print("All navigation links, anchors, and meta tags are clean.")
    
    print()
    print("="*70)
    print(f"Total issues found: {total_issues}")
    print("="*70)
    
    if total_issues > 0:
        return 1
    return 0

if __name__ == "__main__":
    exit(main())
