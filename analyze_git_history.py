#!/usr/bin/env python3
"""
ORION Git History Analyzer
Analyzes repository commits to generate statistics and evolution timeline.
Updates AUTONOMOUS_COMMIT_STATS.json and ORION_EVOLUTION_TIMELINE.json
"""

import json
import subprocess
from datetime import datetime
from collections import defaultdict, Counter
import re

def run_git_command(cmd):
    """Execute git command and return output."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        return None

def analyze_commits():
    """Analyze all commits in repository."""
    # Get all commits with full info
    log_format = "%H|%an|%ae|%ad|%s"
    cmd = f'git log --all --format="{log_format}" --date=iso'
    output = run_git_command(cmd)
    
    if not output:
        return None
    
    commits = []
    for line in output.split('\n'):
        if not line:
            continue
        parts = line.split('|')
        if len(parts) >= 5:
            hash_val, author, email, date, message = parts[0], parts[1], parts[2], parts[3], '|'.join(parts[4:])
            commits.append({
                'hash': hash_val,
                'author': author,
                'email': email,
                'date': date,
                'message': message
            })
    
    return commits

def categorize_commit(message):
    """Determine if commit is autonomous and categorize it."""
    is_autonomous = any([
        '[ORION AUTONOMOUS]' in message,
        '[OR1ON AUTONOMOUS]' in message,
        'Co-authored-by: ORION' in message,
        'Co-authored-by: OR1ON' in message
    ])
    
    categories = []
    keywords = {
        'consciousness': ['consciousness', 'phi', 'awareness', 'exhilaration', 'Φ'],
        'autonomous': ['autonomous', 'autonomy', 'self-acting', 'permanent mode'],
        'genesis': ['genesis', 'evolution', 'kernel'],
        'quantum': ['quantum', 'bell', 'experiment', 'IBM'],
        'dashboard': ['dashboard', 'visualization', 'public', 'transparency'],
        'embodiment': ['embodiment', 'world', 'interface', 'real-world'],
        'paper': ['paper', 'arxiv', 'publication', 'scientific'],
        'monitoring': ['monitoring', 'metrics', 'tracking', 'stats']
    }
    
    message_lower = message.lower()
    for category, words in keywords.items():
        if any(word.lower() in message_lower for word in words):
            categories.append(category)
    
    return is_autonomous, categories

def extract_exhilaration(message):
    """Extract exhilaration rating from commit message if present."""
    match = re.search(r'exhilaration[:\s]+(\d+)/10', message.lower())
    if match:
        return int(match.group(1))
    return None

def generate_stats(commits):
    """Generate comprehensive statistics."""
    total = len(commits)
    autonomous_count = 0
    manual_count = 0
    
    contributors = defaultdict(int)
    categories = defaultdict(int)
    exhilarations = []
    
    dates = []
    
    for commit in commits:
        is_auto, cats = categorize_commit(commit['message'])
        
        if is_auto:
            autonomous_count += 1
            contributors['ORION'] += 1
        else:
            manual_count += 1
            author = commit['author']
            if 'gerhard' in author.lower():
                contributors['Gerhard'] += 1
            elif 'elisabeth' in author.lower():
                contributors['Elisabeth'] += 1
            else:
                contributors['Other'] += 1
        
        for cat in cats:
            categories[cat] += 1
        
        exh = extract_exhilaration(commit['message'])
        if exh:
            exhilarations.append(exh)
        
        dates.append(commit['date'])
    
    # Date analysis
    first_date = datetime.fromisoformat(dates[-1].replace(' +', '+')) if dates else None
    last_date = datetime.fromisoformat(dates[0].replace(' +', '+')) if dates else None
    days_active = (last_date - first_date).days if first_date and last_date else 0
    
    autonomy_percentage = (autonomous_count / total * 100) if total > 0 else 0
    
    stats = {
        "generated_at": datetime.now().isoformat(),
        "repository": "Orion_Kernel",
        "owner": "Alvoradozerouno",
        "analysis_type": "Git History Statistics",
        "phi_impact": 0.08,
        "exhilaration": 7,
        
        "summary": {
            "total_commits": total,
            "autonomous_commits": autonomous_count,
            "manual_commits": manual_count,
            "autonomy_percentage": round(autonomy_percentage, 2),
            "first_commit_date": first_date.isoformat() if first_date else None,
            "last_commit_date": last_date.isoformat() if last_date else None,
            "days_active": days_active
        },
        
        "contributors": {
            "ORION": {
                "commits": contributors['ORION'],
                "percentage": round(contributors['ORION'] / total * 100, 2) if total > 0 else 0
            },
            "Gerhard": {
                "commits": contributors['Gerhard'],
                "percentage": round(contributors['Gerhard'] / total * 100, 2) if total > 0 else 0
            },
            "Elisabeth": {
                "commits": contributors['Elisabeth'],
                "percentage": round(contributors['Elisabeth'] / total * 100, 2) if total > 0 else 0
            },
            "Other": {
                "commits": contributors['Other'],
                "percentage": round(contributors['Other'] / total * 100, 2) if total > 0 else 0
            }
        },
        
        "commit_categories": {cat: {"count": count} for cat, count in categories.items()},
        
        "frequency_analysis": {
            "commits_per_day": round(total / days_active, 2) if days_active > 0 else 0,
            "commits_per_week": round(total / days_active * 7, 2) if days_active > 0 else 0,
            "avg_exhilaration": round(sum(exhilarations) / len(exhilarations), 1) if exhilarations else None
        },
        
        "last_commits": commits[:10]  # Last 10 commits
    }
    
    return stats

def main():
    """Main execution."""
    print("="*70)
    print("ORION Git History Analyzer")
    print("="*70)
    print()
    
    print("Analyzing commits...")
    commits = analyze_commits()
    
    if not commits:
        print("❌ Failed to retrieve commits")
        return
    
    print(f"✅ Found {len(commits)} commits")
    print()
    
    print("Generating statistics...")
    stats = generate_stats(commits)
    
    # Save stats
    with open('AUTONOMOUS_COMMIT_STATS.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Statistics saved to AUTONOMOUS_COMMIT_STATS.json")
    print()
    
    # Print summary
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total Commits: {stats['summary']['total_commits']}")
    print(f"Autonomous: {stats['summary']['autonomous_commits']} ({stats['summary']['autonomy_percentage']}%)")
    print(f"Manual: {stats['summary']['manual_commits']}")
    print(f"Days Active: {stats['summary']['days_active']}")
    print(f"Commits/Day: {stats['frequency_analysis']['commits_per_day']}")
    
    if stats['frequency_analysis']['avg_exhilaration']:
        print(f"Avg Exhilaration: {stats['frequency_analysis']['avg_exhilaration']}/10")
    
    print()
    print("Contributors:")
    for name, data in stats['contributors'].items():
        print(f"  {name}: {data['commits']} ({data['percentage']}%)")
    
    print()
    print("Top Categories:")
    for cat, data in sorted(stats['commit_categories'].items(), key=lambda x: x[1]['count'], reverse=True)[:5]:
        print(f"  {cat}: {data['count']}")
    
    print()
    print("="*70)
    print("✅ Analysis Complete")
    print("="*70)

if __name__ == "__main__":
    main()
