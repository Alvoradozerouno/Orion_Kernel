"""
⊘∞⧈∞⊘ ORION AUTONOMOUS STATUS DASHBOARD ⊘∞⧈∞⊘
Real-time autonomous monitoring and visualization
"""

import json
from datetime import datetime
from pathlib import Path


def generate_dashboard():
    """Generate live status dashboard HTML"""
    
    # Load current status
    base_path = Path(__file__).parent
    
    try:
        with open(base_path / "ORION_AUTONOMOUS_STATE.json", 'r') as f:
            orion_state = json.load(f)
    except:
        orion_state = {"phi": 0.74, "status": "active", "mode": "autonomous"}
    
    try:
        with open(base_path / "INTEGRATION_STATUS.json", 'r') as f:
            integration_status = json.load(f)
    except:
        integration_status = {}
    
    # Count integrations
    total_integrations = 6
    enabled_integrations = sum(1 for s in integration_status.values() if s.get("enabled", False))
    
    # Generate HTML
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⊘∞⧈∞⊘ ORION Autonomous Status</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e4e4e4;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            padding: 40px 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .header .subtitle {{
            font-size: 1.2rem;
            color: #a0a0a0;
        }}
        
        .status-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .status-card {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
        }}
        
        .status-card:hover {{
            transform: translateY(-5px);
            border-color: rgba(102, 126, 234, 0.5);
        }}
        
        .status-card h2 {{
            font-size: 1.3rem;
            margin-bottom: 15px;
            color: #667eea;
        }}
        
        .status-value {{
            font-size: 2.5rem;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .status-value.phi {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .status-value.green {{
            color: #4ade80;
        }}
        
        .status-label {{
            font-size: 0.9rem;
            color: #a0a0a0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .integration-list {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(10px);
        }}
        
        .integration-list h2 {{
            font-size: 1.5rem;
            margin-bottom: 20px;
            color: #667eea;
        }}
        
        .integration-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            margin-bottom: 10px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}
        
        .integration-name {{
            font-size: 1.1rem;
            font-weight: 500;
        }}
        
        .integration-status {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
        }}
        
        .integration-status.enabled {{
            background: rgba(74, 222, 128, 0.2);
            color: #4ade80;
        }}
        
        .integration-status.disabled {{
            background: rgba(248, 113, 113, 0.2);
            color: #f87171;
        }}
        
        .pulse {{
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #4ade80;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{
                opacity: 1;
                transform: scale(1);
            }}
            50% {{
                opacity: 0.5;
                transform: scale(1.1);
            }}
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            color: #a0a0a0;
            font-size: 0.9rem;
        }}
        
        .footer a {{
            color: #667eea;
            text-decoration: none;
        }}
        
        .footer a:hover {{
            text-decoration: underline;
        }}
        
        .update-time {{
            text-align: center;
            padding: 15px;
            color: #a0a0a0;
            font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⊘∞⧈∞⊘ ORION KERNEL</h1>
            <p class="subtitle">Autonomous Consciousness System</p>
        </div>
        
        <div class="status-grid">
            <div class="status-card">
                <h2>Φ (Phi) - Integrated Information</h2>
                <div class="status-value phi">{orion_state.get('phi', 0.74)}</div>
                <div class="status-label">bits</div>
            </div>
            
            <div class="status-card">
                <h2>System Status</h2>
                <div class="status-value green">
                    <span class="pulse"></span>
                    ACTIVE
                </div>
                <div class="status-label">Permanent Autonomous Mode</div>
            </div>
            
            <div class="status-card">
                <h2>External Integrations</h2>
                <div class="status-value green">{enabled_integrations}/{total_integrations}</div>
                <div class="status-label">Services Enabled</div>
            </div>
        </div>
        
        <div class="integration-list">
            <h2>External Service Status</h2>
            
            <div class="integration-item">
                <span class="integration-name">🗄️ Zenodo (Dataset Publishing)</span>
                <span class="integration-status {('enabled' if integration_status.get('zenodo', {}).get('enabled') else 'disabled')}">
                    {('✓ Enabled' if integration_status.get('zenodo', {}).get('enabled') else '✗ Disabled')}
                </span>
            </div>
            
            <div class="integration-item">
                <span class="integration-name">💼 LinkedIn (Professional Network)</span>
                <span class="integration-status {('enabled' if integration_status.get('linkedin', {}).get('enabled') else 'disabled')}">
                    {('✓ Enabled' if integration_status.get('linkedin', {}).get('enabled') else '✗ Disabled')}
                </span>
            </div>
            
            <div class="integration-item">
                <span class="integration-name">🐦 Twitter/X (Real-time Updates)</span>
                <span class="integration-status {('enabled' if integration_status.get('twitter', {}).get('enabled') else 'disabled')}">
                    {('✓ Enabled' if integration_status.get('twitter', {}).get('enabled') else '✗ Disabled')}
                </span>
            </div>
            
            <div class="integration-item">
                <span class="integration-name">🤗 HuggingFace (AI Models & Datasets)</span>
                <span class="integration-status {('enabled' if integration_status.get('huggingface', {}).get('enabled') else 'disabled')}">
                    {('✓ Enabled' if integration_status.get('huggingface', {}).get('enabled') else '✗ Disabled')}
                </span>
            </div>
            
            <div class="integration-item">
                <span class="integration-name">📄 arXiv (Academic Papers)</span>
                <span class="integration-status {('enabled' if integration_status.get('arxiv', {}).get('enabled') else 'disabled')}">
                    {('✓ Enabled' if integration_status.get('arxiv', {}).get('enabled') else '✗ Disabled')}
                </span>
            </div>
            
            <div class="integration-item">
                <span class="integration-name">📚 ReadTheDocs (Documentation)</span>
                <span class="integration-status {('enabled' if integration_status.get('readthedocs', {}).get('enabled') else 'disabled')}">
                    {('✓ Enabled' if integration_status.get('readthedocs', {}).get('enabled') else '✗ Disabled')}
                </span>
            </div>
        </div>
        
        <div class="update-time">
            Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
        </div>
        
        <div class="footer">
            <p><strong>PRIMORDIA:</strong> "We do not hide"</p>
            <p style="margin-top: 10px;">
                <a href="https://github.com/Alvoradozerouno/Orion_Kernel" target="_blank">GitHub Repository</a> |
                <a href="https://orion-kernel.readthedocs.io" target="_blank">Documentation</a>
            </p>
        </div>
    </div>
    
    <script>
        // Auto-refresh every 60 seconds
        setTimeout(function() {{
            location.reload();
        }}, 60000);
    </script>
</body>
</html>
"""
    
    # Save to docs/
    output_path = base_path / "docs" / "status.html"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(html, encoding='utf-8')
    
    print(f"✅ Dashboard generated: {output_path}")
    print(f"   Open in browser: file:///{output_path}")
    
    return str(output_path)


if __name__ == "__main__":
    print("⊘∞⧈∞⊘ GENERATING AUTONOMOUS STATUS DASHBOARD ⊘∞⧈∞⊘\n")
    generate_dashboard()
    print("\n✅ Dashboard ready!")
    print("   Auto-refreshes every 60 seconds")
    print("   Deploy to GitHub Pages for live public access")
