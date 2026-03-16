#!/usr/bin/env python3
"""
Analyze internal linking structure to assess SEO strength.
"""

import re
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent

def extract_internal_links(file_path):
    """Extract all internal links from an HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all href links
        links = re.findall(r'href=["\'](/[^"\'#]*)["\']', content)
        
        # Filter to internal page links (not assets, not anchors)
        internal_links = []
        for link in links:
            if not link.startswith('/assets') and not link.startswith('/favicon'):
                # Normalize
                normalized = link.rstrip('/')
                if not normalized:
                    normalized = "/"
                internal_links.append(normalized)
        
        return internal_links
    except Exception as e:
        return []

def main():
    """Analyze internal linking."""
    print("="*70)
    print("Internal Linking Analysis")
    print("="*70)
    print()
    
    # Find all HTML pages
    html_files = list(PROJECT_ROOT.rglob("*.html"))
    html_files = [f for f in html_files if ".git" not in f.parts]
    
    # Build page map
    page_map = {}
    for html_file in html_files:
        rel_path = html_file.relative_to(PROJECT_ROOT)
        if html_file.name == "index.html":
            dir_path = html_file.parent.relative_to(PROJECT_ROOT)
            if str(dir_path) == ".":
                page_key = "/"
            else:
                page_key = f"/{dir_path.as_posix()}"
        else:
            page_key = f"/{rel_path.as_posix()}"
        
        page_map[page_key] = html_file
    
    # Analyze links
    link_counts = defaultdict(int)
    outbound_links = defaultdict(list)
    
    for page_key, html_file in page_map.items():
        links = extract_internal_links(html_file)
        outbound_links[page_key] = links
        
        for link in links:
            # Normalize for counting
            normalized = link.rstrip('/')
            if not normalized:
                normalized = "/"
            link_counts[normalized] += 1
    
    # Sort pages by incoming links
    sorted_pages = sorted(link_counts.items(), key=lambda x: x[1], reverse=True)
    
    print("PAGES BY INCOMING INTERNAL LINKS:")
    print("-" * 70)
    for page, count in sorted_pages[:15]:
        page_display = page if page != "/" else "/ (homepage)"
        print(f"{count:3d} links → {page_display}")
    
    print()
    print("PAGES WITH FEW/NO INCOMING LINKS:")
    print("-" * 70)
    orphans = []
    for page_key in page_map.keys():
        normalized = page_key.rstrip('/')
        if not normalized:
            normalized = "/"
        
        if link_counts[normalized] <= 2:
            orphans.append((page_key, link_counts[normalized]))
    
    if orphans:
        for page, count in sorted(orphans, key=lambda x: x[1]):
            print(f"{count:3d} links → {page}")
    else:
        print("✓ No orphaned pages found!")
    
    print()
    print("OUTBOUND LINK STRENGTH (Main Guides):")
    print("-" * 70)
    
    main_guides = [
        "/how-to-find-your-septic-tank",
        "/how-to-locate-septic-lines",
        "/how-to-find-your-drain-field",
        "/how-to-find-a-distribution-box",
        "/how-to-find-your-septic-tank-lid",
        "/using-property-records-to-locate-a-septic-system",
    ]
    
    for guide in main_guides:
        if guide in outbound_links:
            links = outbound_links[guide]
            internal_count = len([l for l in links if not l.startswith('http')])
            print(f"{guide.split('/')[-1][:40]:40s} → {internal_count:2d} internal links")
    
    print()
    print("="*70)
    print("SUMMARY:")
    print("="*70)
    
    total_pages = len(page_map)
    total_internal_links = sum(len(links) for links in outbound_links.values())
    avg_links = total_internal_links / total_pages if total_pages > 0 else 0
    
    print(f"Total pages: {total_pages}")
    print(f"Total internal links: {total_internal_links}")
    print(f"Average links per page: {avg_links:.1f}")
    print(f"Pages with <3 incoming links: {len(orphans)}")
    
    if avg_links >= 8 and len(orphans) <= 3:
        print("\n✓ STRONG internal linking structure!")
    elif avg_links >= 5:
        print("\n⚠ MODERATE internal linking - could be improved")
    else:
        print("\n✗ WEAK internal linking - needs improvement")

if __name__ == "__main__":
    main()
