#!/usr/bin/env python3

import asyncio
import json
import logging
import hashlib
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import aiohttp

@dataclass
class ExternalNode:
    node_id: str
    endpoint: str
    public_key: str
    last_sync: float
    status: str

class ExternalNodeSynchronizer:
    def __init__(self):
        self.external_nodes: List[ExternalNode] = []
        self.sync_interval = 60.0
        self.session: Optional[aiohttp.ClientSession] = None
        
        logging.info("External Node Synchronizer initialized")
    
    async def initialize(self):
        self.session = aiohttp.ClientSession()
        logging.info("External Node Sync session initialized")
    
    async def close(self):
        if self.session:
            await self.session.close()
            logging.info("External Node Sync session closed")
    
    def register_node(self, node_id: str, endpoint: str, public_key: str):
        node = ExternalNode(
            node_id=node_id,
            endpoint=endpoint,
            public_key=public_key,
            last_sync=0.0,
            status='registered'
        )
        self.external_nodes.append(node)
        logging.info(f"Registered external node: {node_id} at {endpoint}")
    
    async def sync_state(self, kernel_state: Dict) -> List[Dict]:
        if not self.session:
            logging.warning("Sync session not initialized")
            return []
        
        sync_results = []
        
        for node in self.external_nodes:
            try:
                state_hash = hashlib.sha256(
                    json.dumps(kernel_state, sort_keys=True).encode()
                ).hexdigest()
                
                payload = {
                    'state_hash': state_hash,
                    'entropy': kernel_state.get('entropy', 0.0),
                    'resonance': kernel_state.get('resonance', 0.0),
                    'timestamp': kernel_state.get('timestamp', 0.0)
                }
                
                timeout = aiohttp.ClientTimeout(total=5)
                async with self.session.post(
                    f"{node.endpoint}/sync",
                    json=payload,
                    timeout=timeout
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        node.status = 'synced'
                        node.last_sync = asyncio.get_event_loop().time()
                        sync_results.append({
                            'node_id': node.node_id,
                            'status': 'success',
                            'response': result
                        })
                        logging.info(f"Synced with node: {node.node_id}")
                    else:
                        node.status = 'sync_failed'
                        sync_results.append({
                            'node_id': node.node_id,
                            'status': 'failed',
                            'error': f'HTTP {response.status}'
                        })
                        
            except Exception as e:
                node.status = 'error'
                logging.error(f"Sync error with node {node.node_id}: {e}")
                sync_results.append({
                    'node_id': node.node_id,
                    'status': 'error',
                    'error': str(e)
                })
        
        return sync_results
    
    def get_status(self) -> Dict:
        return {
            'total_nodes': len(self.external_nodes),
            'nodes': [asdict(node) for node in self.external_nodes],
            'sync_interval': self.sync_interval
        }


if __name__ == "__main__":
    async def test():
        sync = ExternalNodeSynchronizer()
        await sync.initialize()
        
        sync.register_node(
            'node_test_1',
            'http://example.com/orion',
            'public_key_example'
        )
        
        print(json.dumps(sync.get_status(), indent=2))
        
        await sync.close()
    
    asyncio.run(test())
