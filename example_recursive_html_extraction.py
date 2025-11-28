#!/usr/bin/env python3
"""
Example: Using Recursive HTML Extraction from FHIR ePI Bundles

This example demonstrates how to extract all HTML content from a FHIR ePI bundle,
including content from deeply nested sections.
"""

import json
from pathlib import Path
from preprocessor.models.fhir_epi import FhirEPI
from preprocessor.models.html_content_manager import (
    get_all_html_content,
    extract_text_content,
    update_section_html
)


def example_1_basic_extraction():
    """Example 1: Basic recursive HTML extraction"""
    print("\n" + "=" * 70)
    print("Example 1: Basic Recursive HTML Extraction")
    print("=" * 70)
    
    # Load a test bundle
    test_file = Path(__file__).parent / "preprocessor" / "test" / "testing ePIs" / "Bundle-processedbundledovato-en.json"
    
    with open(test_file, 'r', encoding='utf-8') as f:
        bundle_dict = json.load(f)
    
    # Create FhirEPI instance
    epi = FhirEPI.from_dict(bundle_dict)
    
    # Extract all HTML content using the FhirEPI method
    all_html = epi.get_all_html_content()
    
    print(f"\n📊 Summary:")
    print(f"   Total sections: {all_html['total_sections']}")
    print(f"   Max nesting level: {all_html['max_nesting_level']}")
    print(f"   Composition HTML length: {len(all_html['composition_html'])} chars")
    
    # Show section hierarchy
    print(f"\n📑 Section Hierarchy:")
    for section in all_html['sections']:
        indent = "  " * section['level']
        marker = "└─" if section['level'] > 0 else "•"
        print(f"   {indent}{marker} {section['title']}")
        print(f"   {indent}  HTML: {len(section['html'])} chars")


def example_2_extract_text():
    """Example 2: Extract plain text from all sections"""
    print("\n" + "=" * 70)
    print("Example 2: Extract Plain Text from All Sections")
    print("=" * 70)
    
    # Load bundle
    test_file = Path(__file__).parent / "preprocessor" / "test" / "testing ePIs" / "Bundle-processedbundledovato-en.json"
    
    with open(test_file, 'r', encoding='utf-8') as f:
        bundle_dict = json.load(f)
    
    epi = FhirEPI.from_dict(bundle_dict)
    all_html = epi.get_all_html_content()
    
    # Extract and display text content from each section
    print(f"\n📝 Text Content by Section:")
    for section in all_html['sections']:
        if section['html']:
            text = extract_text_content(section['html'])
            indent = "  " * section['level']
            print(f"\n{indent}[Level {section['level']}] {section['title']}")
            print(f"{indent}{'─' * 60}")
            
            # Show first 150 characters
            preview = text[:150] + "..." if len(text) > 150 else text
            print(f"{indent}{preview}")
            print(f"{indent}(Total: {len(text)} chars)")


def example_3_find_specific_sections():
    """Example 3: Find and extract specific sections by title"""
    print("\n" + "=" * 70)
    print("Example 3: Find Specific Sections")
    print("=" * 70)
    
    # Load bundle
    test_file = Path(__file__).parent / "preprocessor" / "test" / "testing ePIs" / "Bundle-processedbundledovato-en.json"
    
    with open(test_file, 'r', encoding='utf-8') as f:
        bundle_dict = json.load(f)
    
    epi = FhirEPI.from_dict(bundle_dict)
    all_html = epi.get_all_html_content()
    
    # Search for specific sections
    search_terms = ['side effects', 'Dovato', 'pregnancy']
    
    print(f"\n🔍 Searching for sections containing: {', '.join(search_terms)}")
    
    for section in all_html['sections']:
        title_lower = section['title'].lower()
        if any(term.lower() in title_lower for term in search_terms):
            text = extract_text_content(section['html'])
            print(f"\n✓ Found: {section['title']}")
            print(f"  Level: {section['level']}")
            print(f"  HTML length: {len(section['html'])} chars")
            print(f"  Text preview: {text[:100]}...")


def example_4_update_section_html():
    """Example 4: Update HTML in a specific section"""
    print("\n" + "=" * 70)
    print("Example 4: Update Section HTML")
    print("=" * 70)
    
    # Load bundle
    test_file = Path(__file__).parent / "preprocessor" / "test" / "testing ePIs" / "Bundle-processedbundledovato-en.json"
    
    with open(test_file, 'r', encoding='utf-8') as f:
        bundle_dict = json.load(f)
    
    epi = FhirEPI.from_dict(bundle_dict)
    composition = epi.get_composition()
    
    # Get original HTML
    all_html_before = get_all_html_content(composition)
    print(f"\n📊 Before update:")
    print(f"   Total sections: {all_html_before['total_sections']}")
    
    # Update a specific section
    section_title = "What is in this leaflet"
    new_html = '<div xmlns="http://www.w3.org/1999/xhtml"><p><strong>UPDATED:</strong> This section has been modified for demonstration purposes.</p></div>'
    
    success = update_section_html(
        composition.get('section', []),
        section_title,
        new_html,
        recursive=True
    )
    
    if success:
        print(f"\n✅ Successfully updated section: '{section_title}'")
        
        # Verify the update
        all_html_after = get_all_html_content(composition)
        for section in all_html_after['sections']:
            if section['title'] == section_title:
                print(f"\n   New HTML: {section['html']}")
    else:
        print(f"\n❌ Failed to find section: '{section_title}'")


def example_5_analyze_structure():
    """Example 5: Analyze HTML structure across all sections"""
    print("\n" + "=" * 70)
    print("Example 5: Analyze HTML Structure")
    print("=" * 70)
    
    # Load bundle
    test_file = Path(__file__).parent / "preprocessor" / "test" / "testing ePIs" / "Bundle-processedbundledovato-en.json"
    
    with open(test_file, 'r', encoding='utf-8') as f:
        bundle_dict = json.load(f)
    
    epi = FhirEPI.from_dict(bundle_dict)
    all_html = epi.get_all_html_content()
    
    # Analyze HTML content
    total_html_length = 0
    sections_with_lists = 0
    sections_with_tables = 0
    sections_with_links = 0
    
    print(f"\n📈 Analyzing {all_html['total_sections']} sections...")
    
    for section in all_html['sections']:
        html = section['html']
        total_html_length += len(html)
        
        if '<ul>' in html or '<ol>' in html:
            sections_with_lists += 1
        if '<table>' in html:
            sections_with_tables += 1
        if '<a ' in html:
            sections_with_links += 1
    
    print(f"\n📊 Analysis Results:")
    print(f"   Total HTML content: {total_html_length:,} chars")
    print(f"   Sections with lists: {sections_with_lists}")
    print(f"   Sections with tables: {sections_with_tables}")
    print(f"   Sections with links: {sections_with_links}")
    print(f"   Average HTML per section: {total_html_length // all_html['total_sections']:,} chars")


if __name__ == '__main__':
    print("=" * 70)
    print("FHIR ePI Recursive HTML Extraction Examples")
    print("=" * 70)
    
    try:
        example_1_basic_extraction()
        example_2_extract_text()
        example_3_find_specific_sections()
        example_4_update_section_html()
        example_5_analyze_structure()
        
        print("\n" + "=" * 70)
        print("✅ All examples completed successfully!")
        print("=" * 70)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
