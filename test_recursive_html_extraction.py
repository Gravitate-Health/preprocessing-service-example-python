#!/usr/bin/env python3
"""
Test script for recursive HTML extraction from FHIR Composition sections
"""

import json
from pathlib import Path
from preprocessor.models.html_content_manager import get_all_html_content


def test_recursive_extraction():
    """Test recursive HTML extraction from a real ePI bundle"""
    
    # Load a test bundle
    test_file = Path(__file__).parent / "preprocessor" / "test" / "testing ePIs" / "Bundle-processedbundledovato-en.json"
    
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return False
    
    print(f"📖 Loading test file: {test_file.name}")
    
    with open(test_file, 'r', encoding='utf-8') as f:
        bundle = json.load(f)
    
    # Extract composition
    composition = None
    for entry in bundle.get('entry', []):
        resource = entry.get('resource', {})
        if resource.get('resourceType') == 'Composition':
            composition = resource
            break
    
    if not composition:
        print("❌ No Composition found in bundle")
        return False
    
    print(f"✅ Found Composition: {composition.get('id', 'unknown')}")
    
    # Extract all HTML content recursively
    print("\n🔍 Extracting all HTML content recursively...")
    all_html = get_all_html_content(composition)
    
    # Display results
    print(f"\n📊 Extraction Results:")
    print(f"   • Composition HTML length: {len(all_html['composition_html'])} chars")
    print(f"   • Total sections found: {all_html['total_sections']}")
    print(f"   • Maximum nesting level: {all_html['max_nesting_level']}")
    
    print(f"\n📑 Section Details:")
    for i, section in enumerate(all_html['sections'], 1):
        indent = "  " * section['level']
        subsection_marker = " [has subsections]" if section['has_subsections'] else ""
        html_length = len(section['html'])
        print(f"   {i}. {indent}Level {section['level']}: {section['title']}{subsection_marker}")
        print(f"      {indent}HTML length: {html_length} chars")
        
        # Show a preview of the HTML content
        if html_length > 0:
            preview = section['html'][:100].replace('\n', ' ').strip()
            if len(section['html']) > 100:
                preview += "..."
            print(f"      {indent}Preview: {preview}")
    
    # Verify all sections have HTML content
    sections_with_html = sum(1 for s in all_html['sections'] if len(s['html']) > 0)
    sections_without_html = all_html['total_sections'] - sections_with_html
    
    print(f"\n📈 HTML Content Summary:")
    print(f"   • Sections with HTML: {sections_with_html}")
    print(f"   • Sections without HTML: {sections_without_html}")
    
    if sections_without_html > 0:
        print(f"\n⚠️  Warning: {sections_without_html} sections have no HTML content")
    else:
        print(f"\n✅ All sections contain HTML content!")
    
    # Calculate total HTML across all sections
    total_html_chars = len(all_html['composition_html']) + sum(
        len(s['html']) for s in all_html['sections']
    )
    print(f"\n💾 Total HTML characters extracted: {total_html_chars:,}")
    
    return True


if __name__ == '__main__':
    print("=" * 70)
    print("Testing Recursive HTML Extraction from FHIR Composition")
    print("=" * 70)
    
    try:
        success = test_recursive_extraction()
        print("\n" + "=" * 70)
        if success:
            print("✅ Test completed successfully!")
        else:
            print("❌ Test failed!")
        print("=" * 70)
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
