#!/usr/bin/env python3
"""Validate HTML file for GitHub Pages deployment."""

with open('docs/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("="*70)
print("HTML VALIDATION CHECK")
print("="*70)
print()

# Count tags
html_open = content.count('<html')
html_close = content.count('</html>')
body_open = content.count('<body')
body_close = content.count('</body>')
script_open = content.count('<script')
script_close = content.count('</script>')

print(f"HTML tags:   {html_open} opening, {html_close} closing")
print(f"Body tags:   {body_open} opening, {body_close} closing")
print(f"Script tags: {script_open} opening, {script_close} closing")
print()

errors = []
if html_open != html_close:
    errors.append(f"HTML tag mismatch: {html_open} opening vs {html_close} closing")
if body_open != body_close:
    errors.append(f"Body tag mismatch: {body_open} opening vs {body_close} closing")
if script_open != script_close:
    errors.append(f"Script tag mismatch: {script_open} opening vs {script_close} closing")

# Check for specific issues
if '</html>' in content and content.rindex('</html>') != content.rfind('</html>'):
    errors.append("Multiple </html> tags found")

print(f"File size: {len(content):,} bytes")
print(f"Lines: {content.count(chr(10)) + 1}")
print()

if errors:
    print("❌ ERRORS FOUND:")
    for err in errors:
        print(f"   - {err}")
else:
    print("✅ HTML structure is valid!")
    print("✅ Ready for GitHub Pages deployment")

print("="*70)
