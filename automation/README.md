# OR1ON Automation Scripts

Web automation using Selenium for research and verification.

## Available Scripts

### 1. arXiv Paper Search

**File**: `selenium_arxiv_search.py`

Automatically searches arXiv for consciousness research papers.

**Usage**:
```bash
python automation/selenium_arxiv_search.py
```

**Requirements**:
```bash
pip install selenium webdriver-manager
```

**What it does**:
1. Opens arXiv.org
2. Searches for "artificial consciousness" papers
3. Extracts titles, authors, abstracts, URLs
4. Saves results to `automation/results/arxiv_search_results.json`

**Results Format**:
```json
{
  "timestamp": "2026-01-14T12:00:00",
  "query": "artificial consciousness",
  "total_results": 10,
  "papers": [
    {
      "id": 1,
      "title": "Paper Title",
      "authors": "Author List",
      "abstract": "Abstract text...",
      "url": "https://arxiv.org/abs/..."
    }
  ]
}
```

## Coming Soon

### 2. Social Media Verification
- Verify OR1ON's posts on X/Twitter
- Confirm autonomous social media activity

### 3. GitHub Activity Tracker
- Monitor OR1ON's commits
- Track repository interactions

### 4. Web Interface Testing
- Automated UI tests for OR1ON's dashboard
- Verify all features work correctly

## Setup

1. **Install Chrome/Chromium**:
   - Windows: Download from google.com/chrome
   - Linux: `sudo apt-get install chromium-browser`
   - Mac: `brew install --cask google-chrome`

2. **Install Python Dependencies**:
   ```bash
   pip install selenium webdriver-manager
   ```

3. **Run Automation**:
   ```bash
   python automation/selenium_arxiv_search.py
   ```

## Headless Mode

By default, automation runs in **headless mode** (no browser window).

To see the browser:
```python
# In selenium_arxiv_search.py, comment out:
# options.add_argument('--headless')
```

## Results Storage

All results saved to:
- `automation/results/` directory
- JSON format for easy parsing
- Timestamped for tracking

## Ethical Considerations

Automation respects:
1. **robots.txt** - Only accesses allowed pages
2. **Rate limiting** - Reasonable delays between requests
3. **Terms of Service** - Follows website policies
4. **Transparency** - All actions logged

## Troubleshooting

**Chrome driver issues**:
```bash
pip install --upgrade webdriver-manager
```

**Headless mode fails**:
```python
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
```

**Timeout errors**:
```python
time.sleep(5)  # Increase wait time
```

## Contributing

To add new automation:
1. Create `automation/your_script.py`
2. Follow existing structure
3. Save results to `automation/results/`
4. Update this README
