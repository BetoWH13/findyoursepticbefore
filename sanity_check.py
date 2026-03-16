#!/usr/bin/env python3
"""
Comprehensive sanity check for the Find Your Septic Before project.
Validates HTML structure, links, canonicals, assets, and more.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent
BASE_DOMAIN = "https://findyoursepticbefore.com"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_section(title):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")

def print_success(msg):
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")

def print_error(msg):
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {msg}")

def check_html_files():
    """Check all HTML files exist and are readable."""
    print_section("1. HTML Files Check")
    
    html_files = list(PROJECT_ROOT.rglob("*.html"))
    html_files = [f for f in html_files if ".git" not in f.parts]
    
    print(f"Found {len(html_files)} HTML files")
    
    errors = []
    for html_file in sorted(html_files):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) < 100:
                    errors.append(f"{html_file.relative_to(PROJECT_ROOT)} - File too small")
                else:
                    print_success(f"{html_file.relative_to(PROJECT_ROOT)}")
        except Exception as e:
            errors.append(f"{html_file.relative_to(PROJECT_ROOT)} - {e}")
    
    if errors:
        for error in errors:
            print_error(error)
        return False
    return True

def check_canonicals():
    """Check all HTML files have correct canonical URLs."""
    print_section("2. Canonical URLs Check")
    
    html_files = list(PROJECT_ROOT.rglob("*.html"))
    html_files = [f for f in html_files if ".git" not in f.parts]
    
    issues = []
    for html_file in sorted(html_files):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for canonical tag
            canonical_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', content, re.IGNORECASE)
            
            if not canonical_match:
                issues.append(f"{html_file.relative_to(PROJECT_ROOT)} - Missing canonical tag")
            else:
                canonical_url = canonical_match.group(1)
                if BASE_DOMAIN not in canonical_url:
                    issues.append(f"{html_file.relative_to(PROJECT_ROOT)} - Wrong domain: {canonical_url}")
                else:
                    print_success(f"{html_file.relative_to(PROJECT_ROOT)} → {canonical_url}")
        except Exception as e:
            issues.append(f"{html_file.relative_to(PROJECT_ROOT)} - Error: {e}")
    
    if issues:
        for issue in issues:
            print_error(issue)
        return False
    return True

def check_assets():
    """Check CSS and JS assets exist."""
    print_section("3. Assets Check")
    
    required_assets = [
        "assets/styles.css",
        "assets/septic-records.js"
    ]
    
    all_good = True
    for asset in required_assets:
        asset_path = PROJECT_ROOT / asset
        if asset_path.exists():
            size = asset_path.stat().st_size
            print_success(f"{asset} ({size:,} bytes)")
        else:
            print_error(f"{asset} - NOT FOUND")
            all_good = False
    
    return all_good

def check_footer_legal_nav():
    """Check all pages have legal footer navigation."""
    print_section("4. Legal Footer Navigation Check")
    
    html_files = list(PROJECT_ROOT.rglob("*.html"))
    html_files = [f for f in html_files if ".git" not in f.parts]
    
    missing = []
    for html_file in sorted(html_files):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for legal footer nav
            has_legal_nav = bool(re.search(r'<nav[^>]*class=["\']footer-links["\'][^>]*aria-label=["\']Footer["\']', content, re.IGNORECASE))
            
            if has_legal_nav:
                # Check for all three links
                has_disclaimer = '/legal/disclaimer.html' in content
                has_privacy = '/legal/privacy.html' in content
                has_terms = '/legal/terms.html' in content
                
                if has_disclaimer and has_privacy and has_terms:
                    print_success(f"{html_file.relative_to(PROJECT_ROOT)}")
                else:
                    missing_links = []
                    if not has_disclaimer: missing_links.append("Disclaimer")
                    if not has_privacy: missing_links.append("Privacy")
                    if not has_terms: missing_links.append("Terms")
                    print_warning(f"{html_file.relative_to(PROJECT_ROOT)} - Missing: {', '.join(missing_links)}")
            else:
                missing.append(html_file.relative_to(PROJECT_ROOT))
        except Exception as e:
            print_error(f"{html_file.relative_to(PROJECT_ROOT)} - Error: {e}")
    
    if missing:
        for file in missing:
            print_error(f"{file} - No legal footer nav")
        return False
    return True

def check_internal_links():
    """Check for broken internal links."""
    print_section("5. Internal Links Check")
    
    html_files = list(PROJECT_ROOT.rglob("*.html"))
    html_files = [f for f in html_files if ".git" not in f.parts]
    
    # Build list of valid paths
    valid_paths = set()
    for html_file in html_files:
        rel_path = html_file.relative_to(PROJECT_ROOT)
        valid_paths.add(f"/{rel_path.as_posix()}")
        
        # Add directory path for index.html files
        if html_file.name == "index.html":
            dir_path = html_file.parent.relative_to(PROJECT_ROOT)
            if str(dir_path) != ".":
                valid_paths.add(f"/{dir_path.as_posix()}/")
            else:
                valid_paths.add("/")
    
    broken_links = []
    for html_file in sorted(html_files):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all internal links
            links = re.findall(r'href=["\'](/[^"\'#]*)["\']', content)
            
            for link in links:
                # Skip external links, anchors, and assets
                if link.startswith('http') or link.startswith('#') or link.startswith('/assets'):
                    continue
                
                # Normalize link
                normalized = link.rstrip('/')
                if not normalized:
                    normalized = "/"
                
                # Check if path exists
                link_exists = False
                for valid_path in valid_paths:
                    if normalized == valid_path.rstrip('/') or normalized + '/' == valid_path:
                        link_exists = True
                        break
                
                if not link_exists:
                    broken_links.append(f"{html_file.relative_to(PROJECT_ROOT)} → {link}")
        except Exception as e:
            print_error(f"{html_file.relative_to(PROJECT_ROOT)} - Error: {e}")
    
    if broken_links:
        print_warning(f"Found {len(broken_links)} potentially broken internal links:")
        for link in broken_links[:10]:  # Show first 10
            print_warning(f"  {link}")
        if len(broken_links) > 10:
            print_warning(f"  ... and {len(broken_links) - 10} more")
        return False
    else:
        print_success("All internal links appear valid")
        return True

def check_homepage_links():
    """Check homepage links to all major pages."""
    print_section("6. Homepage Navigation Check")
    
    index_path = PROJECT_ROOT / "index.html"
    
    required_links = [
        ("/how-to-find-your-septic-tank/", "Septic Tank Guide"),
        ("/how-to-locate-septic-lines/", "Septic Lines Guide"),
        ("/how-to-find-your-drain-field/", "Drain Field Guide"),
        ("/how-to-find-a-distribution-box/", "Distribution Box Guide"),
        ("/using-property-records-to-locate-a-septic-system/", "Records Guide"),
        ("/septic-records-by-state/", "State Records Database"),
        ("/before-you-dig/", "Before You Dig"),
        ("/how-deep-is-my-septic-tank-buried/", "Burial Depth"),
        ("/electronic-septic-locator/", "Electronic Locator"),
        ("/septic-records-finder/", "Records Finder"),
    ]
    
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        missing = []
        for link, name in required_links:
            if link in content:
                print_success(f"{name} - Linked")
            else:
                missing.append(name)
                print_error(f"{name} - NOT LINKED")
        
        return len(missing) == 0
    except Exception as e:
        print_error(f"Error reading homepage: {e}")
        return False

def check_html_structure():
    """Check basic HTML structure."""
    print_section("7. HTML Structure Check")
    
    html_files = list(PROJECT_ROOT.rglob("*.html"))
    html_files = [f for f in html_files if ".git" not in f.parts]
    
    issues = []
    for html_file in sorted(html_files):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for required elements
            checks = [
                (r'<!DOCTYPE html>', "DOCTYPE"),
                (r'<html[^>]*lang=', "lang attribute"),
                (r'<head>', "head tag"),
                (r'<title>', "title tag"),
                (r'<meta[^>]*charset=', "charset meta"),
                (r'<meta[^>]*viewport', "viewport meta"),
                (r'<body>', "body tag"),
            ]
            
            file_issues = []
            for pattern, name in checks:
                if not re.search(pattern, content, re.IGNORECASE):
                    file_issues.append(name)
            
            if file_issues:
                issues.append(f"{html_file.relative_to(PROJECT_ROOT)} - Missing: {', '.join(file_issues)}")
            else:
                print_success(f"{html_file.relative_to(PROJECT_ROOT)}")
        except Exception as e:
            issues.append(f"{html_file.relative_to(PROJECT_ROOT)} - Error: {e}")
    
    if issues:
        for issue in issues:
            print_error(issue)
        return False
    return True

def main():
    """Run all sanity checks."""
    print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}SANITY CHECK - Find Your Septic Before{Colors.RESET}")
    print(f"{Colors.BOLD}Domain: {BASE_DOMAIN}{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}")
    
    results = {
        "HTML Files": check_html_files(),
        "Canonical URLs": check_canonicals(),
        "Assets": check_assets(),
        "Legal Footer Nav": check_footer_legal_nav(),
        "Internal Links": check_internal_links(),
        "Homepage Navigation": check_homepage_links(),
        "HTML Structure": check_html_structure(),
    }
    
    # Summary
    print_section("SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check, result in results.items():
        if result:
            print_success(f"{check}")
        else:
            print_error(f"{check}")
    
    print(f"\n{Colors.BOLD}Result: {passed}/{total} checks passed{Colors.RESET}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL CHECKS PASSED! Project is ready.{Colors.RESET}\n")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ Some issues found. Review above.{Colors.RESET}\n")
        return 1

if __name__ == "__main__":
    exit(main())
