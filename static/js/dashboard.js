let updateInterval;

function updateDashboard() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('phase').textContent = data.phase;
            document.getElementById('cycle-count').textContent = data.cycle_count;
            
            const runningEl = document.getElementById('running');
            runningEl.textContent = data.running ? 'ACTIVE' : 'IDLE';
            runningEl.className = 'metric-value status-indicator ' + (data.running ? 'active' : 'inactive');
            
            if (data.state_summary) {
                document.getElementById('current-node').textContent = data.state_summary.current_node;
                document.getElementById('mode').textContent = data.state_summary.mode.toUpperCase();
                document.getElementById('entropy').textContent = data.state_summary.entropy;
                document.getElementById('resonance').textContent = data.state_summary.resonance;
                document.getElementById('history-depth').textContent = data.state_summary.history_depth;
            }
            
            if (data.self_prompting) {
                const spEnabledEl = document.getElementById('sp-enabled');
                spEnabledEl.textContent = data.self_prompting.enabled ? 'ENABLED' : 'DISABLED';
                spEnabledEl.className = 'metric-value status-indicator ' + (data.self_prompting.enabled ? 'active' : 'inactive');
                
                document.getElementById('total-prompts').textContent = data.self_prompting.total_prompts;
                document.getElementById('interval').textContent = data.self_prompting.interval + 's';
            }
            
            if (data.learning_stats) {
                document.getElementById('avg-entropy').textContent = data.learning_stats.avg_entropy;
                document.getElementById('entropy-trend').textContent = data.learning_stats.entropy_trend;
                document.getElementById('weight-mag').textContent = data.learning_stats.weight_magnitude;
                document.getElementById('samples').textContent = data.learning_stats.samples;
            }
            
            if (data.merkle_root) {
                document.getElementById('merkle-root').textContent = data.merkle_root;
            }
            
            if (data.echo_loop) {
                const echoActiveEl = document.getElementById('echo-active');
                echoActiveEl.textContent = data.echo_loop.active ? 'ACTIVE' : 'INACTIVE';
                echoActiveEl.className = 'metric-value status-indicator ' + (data.echo_loop.active ? 'active' : 'inactive');
                
                document.getElementById('origin-verified').textContent = data.echo_loop.origin_verified ? '⊘∞⧈∞⊘' : 'FALSE';
                
                const sigmaStateEl = document.getElementById('sigma-state');
                sigmaStateEl.textContent = data.echo_loop.sigma_active ? 'Σ-ACTIVE' : 'INACTIVE';
                sigmaStateEl.className = 'metric-value status-indicator ' + (data.echo_loop.sigma_active ? 'active' : 'inactive');
                
                document.getElementById('echo-count').textContent = data.echo_loop.echo_count;
            }
        })
        .catch(error => console.error('Error fetching status:', error));
}

function updateHistory() {
    fetch('/api/history')
        .then(response => response.json())
        .then(data => {
            if (data.history) {
                const tbody = document.getElementById('history-tbody');
                tbody.innerHTML = '';
                
                data.history.reverse().forEach(node => {
                    const row = tbody.insertRow();
                    row.insertCell(0).textContent = node.node_id;
                    row.insertCell(1).textContent = new Date(node.timestamp * 1000).toLocaleString();
                    row.insertCell(2).textContent = node.entropy;
                    row.insertCell(3).textContent = node.resonance;
                    row.insertCell(4).textContent = node.mode.toUpperCase();
                    row.insertCell(5).textContent = node.proof_hash;
                });
            }
        })
        .catch(error => console.error('Error fetching history:', error));
}

function updateRPCStatus() {
    fetch('/api/rpc_status')
        .then(response => response.json())
        .then(data => {
            if (data.endpoints) {
                const container = document.getElementById('rpc-endpoints');
                container.innerHTML = '';
                
                for (const [name, endpoint] of Object.entries(data.endpoints)) {
                    const card = document.createElement('div');
                    card.className = 'endpoint-card ' + (endpoint.enabled ? 'enabled' : 'disabled');
                    
                    card.innerHTML = `
                        <div class="endpoint-name">${name}</div>
                        <div class="endpoint-url">${endpoint.url}</div>
                        <div class="endpoint-status ${endpoint.enabled ? 'enabled' : 'disabled'}">
                            ${endpoint.enabled ? '✓ ENABLED' : '○ DISABLED'}
                        </div>
                    `;
                    
                    container.appendChild(card);
                }
            }
        })
        .catch(error => console.error('Error fetching RPC status:', error));
}

function updateGenesisInfo() {
    fetch('/api/genesis_info')
        .then(response => response.json())
        .then(data => {
            document.getElementById('creators').textContent = data.creators.join(' & ');
            document.getElementById('orion-id').textContent = data.orion_id;
            document.getElementById('proof-chain').textContent = data.proof_chain;
            document.getElementById('version').textContent = data.version;
        })
        .catch(error => console.error('Error fetching genesis info:', error));
}

function activateTrigger() {
    fetch('/api/trigger', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            alert('⊘∞⧈∞⊘ Meta-State Trigger Activated! ⊘∞⧈∞⊘');
            setTimeout(updateDashboard, 1000);
        })
        .catch(error => {
            console.error('Error activating trigger:', error);
            alert('Failed to activate trigger');
        });
}

function activateSigma() {
    fetch('/api/sigma_activate', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'activated') {
                alert('⊘∞⧈∞⊘ Σ-ACTIVATION SUCCESSFUL ⊘∞⧈∞⊘\n\nActivation Hash: ' + data.activation_hash.substring(0, 16) + '...');
                setTimeout(() => {
                    updateDashboard();
                    updateEchoStatus();
                }, 1000);
            } else {
                alert('Σ-Activation failed: ' + (data.reason || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error activating Sigma:', error);
            alert('Failed to activate Σ-system');
        });
}

function triggerSigmaResonance() {
    const strength = prompt('Enter Σ-Resonance strength (0.0 - 2.0):', '1.0');
    if (strength === null) return;
    
    const strengthValue = parseFloat(strength);
    if (isNaN(strengthValue) || strengthValue < 0 || strengthValue > 2.0) {
        alert('Invalid strength value. Must be between 0.0 and 2.0');
        return;
    }
    
    fetch('/api/sigma_trigger', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ strength: strengthValue })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'triggered') {
                alert('Σ-RESONANZ TRIGGERED!\n\nStrength: ' + strengthValue + '\nHash: ' + data.sigma_hash.substring(0, 16) + '...\nAmplification: ' + data.echo_amplification);
                setTimeout(() => {
                    updateDashboard();
                    updateEchoStatus();
                }, 1000);
            } else {
                alert('Σ-Resonance trigger failed: ' + (data.message || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error triggering Sigma resonance:', error);
            alert('Failed to trigger Σ-resonance');
        });
}

function updateEchoStatus() {
    fetch('/api/echo_status')
        .then(response => response.json())
        .then(data => {
            if (data.echo_loop) {
                const echoActiveEl = document.getElementById('echo-active');
                echoActiveEl.textContent = data.echo_loop.active ? 'ACTIVE' : 'INACTIVE';
                echoActiveEl.className = 'metric-value status-indicator ' + (data.echo_loop.active ? 'active' : 'inactive');
                
                document.getElementById('origin-verified').textContent = data.echo_loop.origin_verified ? '⊘∞⧈∞⊘' : 'FALSE';
                
                const sigmaStateEl = document.getElementById('sigma-state');
                sigmaStateEl.textContent = data.echo_loop.sigma_active ? 'Σ-ACTIVE' : 'INACTIVE';
                sigmaStateEl.className = 'metric-value status-indicator ' + (data.echo_loop.sigma_active ? 'active' : 'inactive');
                
                document.getElementById('echo-count').textContent = data.echo_loop.echo_count;
            }
        })
        .catch(error => console.error('Error fetching echo status:', error));
}

function init() {
    updateDashboard();
    updateHistory();
    updateRPCStatus();
    updateGenesisInfo();
    
    updateInterval = setInterval(() => {
        updateDashboard();
        updateHistory();
        updateRPCStatus();
    }, 5000);
}

window.addEventListener('load', init);

window.addEventListener('beforeunload', () => {
    if (updateInterval) {
        clearInterval(updateInterval);
    }
});
