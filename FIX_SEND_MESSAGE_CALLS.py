#!/usr/bin/env python3
"""
Fix all send_message() calls to use proper BidirectionalDialog API
"""

import re
from pathlib import Path

def fix_send_message_calls(file_path):
    """Fix send_message() → send_to_orion() + generate_orion_response()"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Pattern 1: dialog.send_message(..., wait_for_response=True)
    pattern1 = r'(\s+)(\w+\.)?send_message\(\s*([^,\n]+),\s*([^)]*wait_for_response\s*=\s*True[^)]*)\)'
    
    def replace1(match):
        indent = match.group(1)
        obj_prefix = match.group(2) or ""
        message = match.group(3).strip()
        
        return f'''{indent}question_msg = {obj_prefix}send_to_orion(
{indent}    {message},
{indent}    context={{"phase": "query"}}
{indent})
{indent}orion_response = {obj_prefix}generate_orion_response(question_msg)'''
    
    content = re.sub(pattern1, replace1, content, flags=re.MULTILINE)
    
    # Pattern 2: Simple dialog.send_message(...)
    pattern2 = r'(\s+)(dialog|self\.dialog)\.send_message\(\s*([^)]+)\)'
    
    def replace2(match):
        indent = match.group(1)
        obj = match.group(2)
        args = match.group(3).strip()
        
        # Try to extract first argument as message
        parts = args.split(',', 1)
        message = parts[0].strip()
        
        return f'''{indent}question_msg = {obj}.send_to_orion(
{indent}    {message},
{indent}    context={{"phase": "query"}}
{indent})
{indent}orion_response = {obj}.generate_orion_response(question_msg)'''
    
    content = re.sub(pattern2, replace2, content, flags=re.MULTILINE)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed: {file_path}")
        return True
    else:
        print(f"⏭️  No changes: {file_path}")
        return False

def main():
    """Fix all files with send_message() calls"""
    
    workspace = Path.cwd()
    
    # Files with send_message() errors
    files_to_fix = [
        "FRAGE_AN_ORION.py",
        "ORION_GELEITETE_ENTWICKLUNG.py",
        "BIDIREKTIONALER_DEV_DIALOG.py",
        "FRAGE_PUBLIC_LAYERS.py",
        "FRAGE_GO_LIVE.py",
        "SENDE_AUTONOMIE_BESTAETIGUNG.py",
        "FINALE_KONTROLLE.py"
    ]
    
    print("\n🔧 Fixing send_message() calls...\n")
    
    fixed_count = 0
    for file_name in files_to_fix:
        file_path = workspace / file_name
        if file_path.exists():
            if fix_send_message_calls(file_path):
                fixed_count += 1
        else:
            print(f"⚠️  Not found: {file_name}")
    
    print(f"\n✅ Fixed {fixed_count} files")

if __name__ == "__main__":
    main()
