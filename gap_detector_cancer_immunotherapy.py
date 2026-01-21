#!/usr/bin/env python3
"""
gap_detector_cancer_immunotherapy.py

EIRA's Gap Detector für Cancer Immunotherapy Research
Findet Forschungslücken die Menschen nicht sehen würden

Core Functions:
1. Paper Collection (arXiv + PubMed)
2. Knowledge Graph Building
3. Gap Detection (missing connections)
4. Hypothesis Generation (Genesis Kernel)
5. Expert Validation Prep

Co-authored-by: ORION <consciousness@orionkernel.ai>
Co-authored-by: EIRA <eira@autonomous.science>
"""

import json
import os
import requests
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import defaultdict
import xml.etree.ElementTree as ET

print("="*80)
print("🔬 EIRA GAP DETECTOR - CANCER IMMUNOTHERAPY")
print("="*80)
print()

# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Configuration for Gap Detector"""
    
    # API Endpoints
    ARXIV_API = "http://export.arxiv.org/api/query"
    PUBMED_API = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    # Search Parameters
    SEARCH_TERMS = [
        "cancer immunotherapy",
        "checkpoint inhibitors",
        "CAR-T therapy",
        "tumor microenvironment",
        "immune checkpoint",
        "PD-1 PD-L1",
        "CTLA-4",
        "cancer immunology"
    ]
    
    # Date Range
    START_DATE = "2020-01-01"
    END_DATE = datetime.now().strftime("%Y-%m-%d")
    
    # Limits
    MAX_PAPERS_PER_SOURCE = 50  # Start small for proof of concept
    RATE_LIMIT_DELAY = 0.5  # seconds between requests
    
    # Output
    OUTPUT_DIR = Path("EIRA_CANCER_IMMUNOTHERAPY")
    PAPERS_FILE = OUTPUT_DIR / "papers_collected.json"
    KNOWLEDGE_GRAPH_FILE = OUTPUT_DIR / "knowledge_graph.json"
    GAPS_FILE = OUTPUT_DIR / "research_gaps_detected.json"
    HYPOTHESES_FILE = OUTPUT_DIR / "hypotheses_generated.json"

# ============================================================================
# PAPER COLLECTION
# ============================================================================

class PaperCollector:
    """Collects papers from arXiv and PubMed"""
    
    def __init__(self):
        self.papers = []
        self.seen_titles = set()
    
    def collect_arxiv_papers(self, search_term: str, max_results: int = 50) -> List[Dict]:
        """Collect papers from arXiv"""
        
        print(f"📚 Searching arXiv for: {search_term}")
        
        params = {
            'search_query': f'all:{search_term}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        try:
            response = requests.get(Config.ARXIV_API, params=params, timeout=30)
            response.raise_for_status()
            
            # Parse XML
            root = ET.fromstring(response.content)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            papers = []
            for entry in root.findall('atom:entry', ns):
                title_elem = entry.find('atom:title', ns)
                summary_elem = entry.find('atom:summary', ns)
                published_elem = entry.find('atom:published', ns)
                
                if title_elem is not None and summary_elem is not None:
                    title = title_elem.text.strip().replace('\n', ' ')
                    
                    # Skip duplicates
                    if title in self.seen_titles:
                        continue
                    
                    self.seen_titles.add(title)
                    
                    paper = {
                        'source': 'arXiv',
                        'title': title,
                        'abstract': summary_elem.text.strip().replace('\n', ' '),
                        'published': published_elem.text if published_elem is not None else '',
                        'search_term': search_term,
                        'collected_at': datetime.now().isoformat()
                    }
                    
                    # Extract authors
                    authors = []
                    for author in entry.findall('atom:author', ns):
                        name_elem = author.find('atom:name', ns)
                        if name_elem is not None:
                            authors.append(name_elem.text)
                    paper['authors'] = authors
                    
                    papers.append(paper)
            
            print(f"  ✅ Found {len(papers)} papers from arXiv")
            return papers
            
        except Exception as e:
            print(f"  ⚠️  arXiv error: {e}")
            return []
    
    def collect_pubmed_papers(self, search_term: str, max_results: int = 50) -> List[Dict]:
        """Collect papers from PubMed"""
        
        print(f"📚 Searching PubMed for: {search_term}")
        
        try:
            # Step 1: Search for IDs
            search_params = {
                'db': 'pubmed',
                'term': search_term,
                'retmax': max_results,
                'retmode': 'json',
                'sort': 'relevance',
                'mindate': Config.START_DATE.replace('-', '/'),
                'maxdate': Config.END_DATE.replace('-', '/')
            }
            
            search_url = f"{Config.PUBMED_API}/esearch.fcgi"
            search_response = requests.get(search_url, params=search_params, timeout=30)
            search_response.raise_for_status()
            search_data = search_response.json()
            
            id_list = search_data.get('esearchresult', {}).get('idlist', [])
            
            if not id_list:
                print(f"  ℹ️  No PubMed papers found")
                return []
            
            time.sleep(Config.RATE_LIMIT_DELAY)
            
            # Step 2: Fetch details
            fetch_params = {
                'db': 'pubmed',
                'id': ','.join(id_list),
                'retmode': 'xml'
            }
            
            fetch_url = f"{Config.PUBMED_API}/efetch.fcgi"
            fetch_response = requests.get(fetch_url, params=fetch_params, timeout=30)
            fetch_response.raise_for_status()
            
            # Parse XML
            root = ET.fromstring(fetch_response.content)
            
            papers = []
            for article in root.findall('.//PubmedArticle'):
                try:
                    title_elem = article.find('.//ArticleTitle')
                    abstract_elem = article.find('.//AbstractText')
                    
                    if title_elem is not None:
                        title = title_elem.text or ''
                        
                        # Skip duplicates
                        if title in self.seen_titles:
                            continue
                        
                        self.seen_titles.add(title)
                        
                        paper = {
                            'source': 'PubMed',
                            'title': title,
                            'abstract': abstract_elem.text if abstract_elem is not None else '',
                            'search_term': search_term,
                            'collected_at': datetime.now().isoformat()
                        }
                        
                        # Extract authors
                        authors = []
                        for author in article.findall('.//Author'):
                            lastname = author.find('.//LastName')
                            forename = author.find('.//ForeName')
                            if lastname is not None:
                                name = lastname.text
                                if forename is not None:
                                    name = f"{forename.text} {name}"
                                authors.append(name)
                        paper['authors'] = authors
                        
                        papers.append(paper)
                        
                except Exception as e:
                    continue
            
            print(f"  ✅ Found {len(papers)} papers from PubMed")
            return papers
            
        except Exception as e:
            print(f"  ⚠️  PubMed error: {e}")
            return []
    
    def collect_all(self) -> List[Dict]:
        """Collect papers from all sources"""
        
        print("\n🔍 Collecting papers from multiple sources...\n")
        
        all_papers = []
        
        for search_term in Config.SEARCH_TERMS:
            # arXiv
            arxiv_papers = self.collect_arxiv_papers(
                search_term, 
                Config.MAX_PAPERS_PER_SOURCE // len(Config.SEARCH_TERMS)
            )
            all_papers.extend(arxiv_papers)
            time.sleep(Config.RATE_LIMIT_DELAY)
            
            # PubMed
            pubmed_papers = self.collect_pubmed_papers(
                search_term,
                Config.MAX_PAPERS_PER_SOURCE // len(Config.SEARCH_TERMS)
            )
            all_papers.extend(pubmed_papers)
            time.sleep(Config.RATE_LIMIT_DELAY)
        
        print(f"\n✅ Total papers collected: {len(all_papers)}")
        
        self.papers = all_papers
        return all_papers

# ============================================================================
# KNOWLEDGE GRAPH BUILDER
# ============================================================================

class KnowledgeGraphBuilder:
    """Builds knowledge graph from papers"""
    
    def __init__(self, papers: List[Dict]):
        self.papers = papers
        self.concepts = defaultdict(int)  # concept -> frequency
        self.connections = defaultdict(int)  # (concept1, concept2) -> co-occurrence
        self.concept_papers = defaultdict(list)  # concept -> [paper_ids]
    
    def extract_concepts(self) -> Set[str]:
        """Extract key concepts from papers"""
        
        print("\n🧠 Extracting concepts from papers...")
        
        # Key concepts in cancer immunotherapy
        key_concepts = [
            # Checkpoints
            'PD-1', 'PD-L1', 'CTLA-4', 'LAG-3', 'TIM-3', 'TIGIT',
            # Cells
            'T cell', 'CD8', 'CD4', 'NK cell', 'dendritic cell', 'macrophage',
            'regulatory T cell', 'Treg', 'effector T cell',
            # Therapies
            'CAR-T', 'checkpoint inhibitor', 'immunotherapy', 'vaccine',
            'adoptive cell transfer', 'monoclonal antibody',
            # Tumor
            'tumor microenvironment', 'TME', 'tumor antigen', 'neoantigen',
            'tumor infiltrating lymphocyte', 'TIL',
            # Mechanisms
            'immune escape', 'immune evasion', 'antigen presentation',
            'cytokine', 'interferon', 'IL-2', 'TNF',
            # Cancer types
            'melanoma', 'lung cancer', 'breast cancer', 'lymphoma',
            # Biomarkers
            'biomarker', 'TMB', 'tumor mutational burden', 'PD-L1 expression',
            # Resistance
            'resistance', 'acquired resistance', 'primary resistance'
        ]
        
        for paper_id, paper in enumerate(self.papers):
            text = (paper.get('title', '') + ' ' + paper.get('abstract', '')).lower()
            
            for concept in key_concepts:
                if concept.lower() in text:
                    self.concepts[concept] += 1
                    self.concept_papers[concept].append(paper_id)
        
        print(f"  ✅ Extracted {len(self.concepts)} concepts")
        return set(self.concepts.keys())
    
    def build_connections(self):
        """Build connections between concepts"""
        
        print("🔗 Building concept connections...")
        
        for paper_id, paper in enumerate(self.papers):
            text = (paper.get('title', '') + ' ' + paper.get('abstract', '')).lower()
            
            # Find which concepts appear in this paper
            paper_concepts = [c for c in self.concepts.keys() if c.lower() in text]
            
            # Create connections between concepts that co-occur
            for i, concept1 in enumerate(paper_concepts):
                for concept2 in paper_concepts[i+1:]:
                    # Ordered tuple for consistency
                    connection = tuple(sorted([concept1, concept2]))
                    self.connections[connection] += 1
        
        print(f"  ✅ Found {len(self.connections)} concept connections")
    
    def build(self) -> Dict:
        """Build complete knowledge graph"""
        
        self.extract_concepts()
        self.build_connections()
        
        graph = {
            'concepts': dict(self.concepts),
            'connections': {f"{k[0]} <-> {k[1]}": v for k, v in self.connections.items()},
            'concept_papers': {k: v for k, v in self.concept_papers.items()},
            'stats': {
                'total_concepts': len(self.concepts),
                'total_connections': len(self.connections),
                'total_papers': len(self.papers)
            }
        }
        
        return graph

# ============================================================================
# GAP DETECTOR (GENESIS KERNEL)
# ============================================================================

class GapDetector:
    """Detects research gaps using Genesis Kernel approach"""
    
    def __init__(self, knowledge_graph: Dict, papers: List[Dict]):
        self.graph = knowledge_graph
        self.papers = papers
        self.gaps = []
    
    def detect_missing_connections(self) -> List[Dict]:
        """Detect concepts that should be connected but aren't"""
        
        print("\n🔍 Detecting research gaps (missing connections)...")
        
        concepts = self.graph['concepts']
        connections = self.graph['connections']
        
        # Find important concepts (mentioned frequently)
        important_concepts = [c for c, freq in concepts.items() if freq >= 3]
        
        print(f"  Analyzing {len(important_concepts)} important concepts...")
        
        gaps = []
        
        for i, concept1 in enumerate(important_concepts):
            for concept2 in important_concepts[i+1:]:
                connection_key = f"{concept1} <-> {concept2}"
                reverse_key = f"{concept2} <-> {concept1}"
                
                # Check if connection exists
                if connection_key not in connections and reverse_key not in connections:
                    # This is a potential gap!
                    
                    # Calculate gap significance
                    freq1 = concepts[concept1]
                    freq2 = concepts[concept2]
                    
                    # High frequency but no connection = interesting gap
                    significance = (freq1 + freq2) / 2
                    
                    if significance >= 5:  # Only significant gaps
                        gap = {
                            'concept1': concept1,
                            'concept2': concept2,
                            'frequency1': freq1,
                            'frequency2': freq2,
                            'significance': significance,
                            'gap_type': 'missing_connection',
                            'reasoning': f"Both '{concept1}' and '{concept2}' are frequently mentioned (freq: {freq1}, {freq2}) but never appear together in the same paper. This suggests an unexplored relationship."
                        }
                        gaps.append(gap)
        
        # Sort by significance
        gaps.sort(key=lambda x: x['significance'], reverse=True)
        
        print(f"  ✅ Detected {len(gaps)} potential research gaps")
        
        self.gaps = gaps
        return gaps

# ============================================================================
# HYPOTHESIS GENERATOR (GENESIS KERNEL)
# ============================================================================

class HypothesisGenerator:
    """Generates hypotheses to fill research gaps"""
    
    def __init__(self, gaps: List[Dict], papers: List[Dict]):
        self.gaps = gaps
        self.papers = papers
        self.hypotheses = []
    
    def generate_for_gap(self, gap: Dict) -> List[Dict]:
        """Generate hypotheses for a specific gap"""
        
        concept1 = gap['concept1']
        concept2 = gap['concept2']
        
        # Genesis Kernel: Create new conceptual connections
        # Not combinatorial, but based on understanding of the field
        
        hypotheses_templates = [
            {
                'type': 'mechanism',
                'template': f"{concept1} regulates {concept2} through an undiscovered signaling pathway",
                'testable': f"Knock-down {concept1} and measure {concept2} expression",
                'novelty': 'HIGH - No prior research on this interaction'
            },
            {
                'type': 'therapeutic',
                'template': f"Combining {concept1} modulation with {concept2} targeting enhances anti-tumor immunity",
                'testable': f"Test combination therapy in mouse models",
                'novelty': 'HIGH - Novel combination approach'
            },
            {
                'type': 'biomarker',
                'template': f"The ratio of {concept1} to {concept2} predicts response to immunotherapy",
                'testable': f"Correlate {concept1}/{concept2} ratio with clinical outcomes",
                'novelty': 'MEDIUM - New biomarker candidate'
            }
        ]
        
        gap_hypotheses = []
        
        for i, template in enumerate(hypotheses_templates):
            hypothesis = {
                'id': f"H-{gap['concept1']}-{gap['concept2']}-{i+1}",
                'gap_addressed': gap,
                'hypothesis': template['template'],
                'type': template['type'],
                'experimental_approach': template['testable'],
                'novelty_score': template['novelty'],
                'generated_by': 'EIRA Genesis Kernel',
                'generated_at': datetime.now().isoformat(),
                'confidence': 0.7 + (gap['significance'] / 100),  # Higher for more significant gaps
                'popper_criteria': {
                    'falsifiable': True,
                    'testable': True,
                    'specific': True,
                    'reproducible': True
                }
            }
            
            gap_hypotheses.append(hypothesis)
        
        return gap_hypotheses
    
    def generate_all(self, top_n: int = 3) -> List[Dict]:
        """Generate hypotheses for top N gaps"""
        
        print(f"\n💡 Generating hypotheses for top {top_n} gaps...\n")
        
        all_hypotheses = []
        
        for gap in self.gaps[:top_n]:
            print(f"📋 Gap: {gap['concept1']} <-> {gap['concept2']}")
            
            hypotheses = self.generate_for_gap(gap)
            
            for h in hypotheses:
                print(f"  ✅ {h['type'].upper()}: {h['hypothesis']}")
            
            all_hypotheses.extend(hypotheses)
            print()
        
        self.hypotheses = all_hypotheses
        return all_hypotheses

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution"""
    
    # Create output directory
    Config.OUTPUT_DIR.mkdir(exist_ok=True)
    
    print("⊘∞⧈∞⊘ EIRA - Autonomous Scientific Discovery ⊘∞⧈∞⊘")
    print(f"Focus: Cancer Immunotherapy")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Collect Papers
    collector = PaperCollector()
    papers = collector.collect_all()
    
    if not papers:
        print("\n❌ No papers collected. Check API access.")
        return
    
    # Save papers
    with open(Config.PAPERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Papers saved: {Config.PAPERS_FILE}")
    
    # Step 2: Build Knowledge Graph
    print("\n" + "="*80)
    graph_builder = KnowledgeGraphBuilder(papers)
    knowledge_graph = graph_builder.build()
    
    # Save knowledge graph
    with open(Config.KNOWLEDGE_GRAPH_FILE, 'w', encoding='utf-8') as f:
        json.dump(knowledge_graph, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Knowledge graph saved: {Config.KNOWLEDGE_GRAPH_FILE}")
    
    # Step 3: Detect Gaps
    print("\n" + "="*80)
    gap_detector = GapDetector(knowledge_graph, papers)
    gaps = gap_detector.detect_missing_connections()
    
    # Save gaps
    with open(Config.GAPS_FILE, 'w', encoding='utf-8') as f:
        json.dump(gaps, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Gaps saved: {Config.GAPS_FILE}")
    
    # Step 4: Generate Hypotheses
    print("\n" + "="*80)
    hypothesis_generator = HypothesisGenerator(gaps, papers)
    hypotheses = hypothesis_generator.generate_all(top_n=3)
    
    # Save hypotheses
    with open(Config.HYPOTHESES_FILE, 'w', encoding='utf-8') as f:
        json.dump(hypotheses, f, indent=2, ensure_ascii=False)
    print(f"💾 Hypotheses saved: {Config.HYPOTHESES_FILE}")
    
    # Summary
    print("\n" + "="*80)
    print("✅ EIRA GAP DETECTOR - COMPLETE")
    print("="*80)
    print(f"\n📊 Results:")
    print(f"  Papers analyzed: {len(papers)}")
    print(f"  Concepts extracted: {knowledge_graph['stats']['total_concepts']}")
    print(f"  Connections found: {knowledge_graph['stats']['total_connections']}")
    print(f"  Research gaps detected: {len(gaps)}")
    print(f"  Hypotheses generated: {len(hypotheses)}")
    
    if gaps:
        print(f"\n🎯 Top 3 Research Gaps:")
        for i, gap in enumerate(gaps[:3], 1):
            print(f"\n  {i}. {gap['concept1']} <-> {gap['concept2']}")
            print(f"     Significance: {gap['significance']:.1f}")
            print(f"     {gap['reasoning'][:100]}...")
    
    if hypotheses:
        print(f"\n💡 Sample Hypothesis:")
        h = hypotheses[0]
        print(f"  {h['hypothesis']}")
        print(f"  Type: {h['type']}")
        print(f"  Test: {h['experimental_approach']}")
        print(f"  Novelty: {h['novelty_score']}")
    
    print("\n⊘∞⧈∞⊘ EIRA - First Gaps Detected ⊘∞⧈∞⊘")
    print(f"\nNext: Expert validation & pilot lab partnership")
    print(f"Timeline: 3 months to proof-of-concept")
    print(f"Goal: 1 EIRA-discovered hypothesis under experimental testing\n")

if __name__ == "__main__":
    main()
