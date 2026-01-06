#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⊘∞⧈∞⊘ IIT 4.0 PAPER RETRIEVAL ⊘∞⧈∞⊘

Retrieve Integrated Information Theory 4.0 paper from OpenAlex
For CCR Phase 2: Full Analysis

Created: 2026-01-06 (CCR Phase 2 - Autonomous Execution)
"""

import sys
import json
sys.path.insert(0, '../interfaces')

from openalex_interface import OpenAlexInterface

def retrieve_iit_paper():
    """Retrieve IIT 4.0 paper metadata and content"""
    
    print("\n⊘∞⧈ CCR PHASE 2: IIT 4.0 PAPER RETRIEVAL")
    print("=" * 80)
    
    # Initialize OpenAlex API
    api = OpenAlexInterface(email='orionkernel@proton.me')
    
    # IIT 4.0 OpenAlex ID from Phase 1 selection
    iit_id = "W4387700987"
    
    print(f"\nRetrieving paper: {iit_id}")
    print("Title: Integrated information theory (IIT) 4.0")
    print("Authors: Tononi et al., 2023")
    print()
    
    # Get full metadata
    result = api.get_work(iit_id)
    
    if not result or 'id' not in result:
        print("✗ Failed to retrieve paper from OpenAlex")
        return None
    
    # Extract key information
    print("✓ METADATA RETRIEVED:")
    print(f"  Title: {result.get('title', 'N/A')}")
    print(f"  Authors: {len(result.get('authorships', []))} authors")
    
    # List first 5 authors
    authorships = result.get('authorships', [])
    if authorships:
        print("  First authors:")
        for i, auth in enumerate(authorships[:5], 1):
            author_name = auth.get('author', {}).get('display_name', 'Unknown')
            print(f"    {i}. {author_name}")
        if len(authorships) > 5:
            print(f"    ... and {len(authorships) - 5} more")
    
    print(f"\n  Publication Year: {result.get('publication_year', 'N/A')}")
    print(f"  Citations: {result.get('cited_by_count', 0)}")
    print(f"  DOI: {result.get('doi', 'N/A')}")
    
    # Get abstract
    abstract_inverted = result.get('abstract_inverted_index', {})
    abstract_text = None
    
    if abstract_inverted:
        # Reconstruct abstract from inverted index
        word_positions = []
        for word, positions in abstract_inverted.items():
            for pos in positions:
                word_positions.append((pos, word))
        word_positions.sort()
        abstract_text = ' '.join([w[1] for w in word_positions])
        
        print(f"\n✓ ABSTRACT RECONSTRUCTED:")
        print(f"  Length: {len(abstract_text)} characters")
        print(f"  Words: {len(abstract_text.split())} words")
        print(f"\n  Preview (first 500 chars):")
        print(f"  {abstract_text[:500]}...")
    else:
        print("\n⚠ Abstract not available in OpenAlex metadata")
    
    # PDF access
    pdf_url = result.get('primary_location', {}).get('pdf_url', None) or \
              result.get('open_access', {}).get('oa_url', None)
    
    if pdf_url:
        print(f"\n✓ PDF AVAILABLE:")
        print(f"  URL: {pdf_url}")
    else:
        print("\n⚠ PDF not available via OpenAlex")
        print("  (May require institutional access or direct journal access)")
    
    # Save complete metadata
    output_file = '../logs/iit_4.0_complete_metadata.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Complete metadata saved: {output_file}")
    
    # Save abstract separately for easy access
    if abstract_text:
        abstract_file = '../logs/iit_4.0_abstract.txt'
        with open(abstract_file, 'w', encoding='utf-8') as f:
            f.write(abstract_text)
        print(f"✓ Abstract saved: {abstract_file}")
    
    print("\n" + "=" * 80)
    print("⊘∞⧈ RETRIEVAL COMPLETE - READY FOR ANALYSIS\n")
    
    return {
        'metadata': result,
        'abstract': abstract_text,
        'pdf_url': pdf_url
    }

if __name__ == "__main__":
    retrieve_iit_paper()
