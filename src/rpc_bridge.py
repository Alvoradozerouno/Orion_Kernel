import asyncio
import json
import logging
from typing import Dict, Any, Optional
import aiohttp
from dataclasses import dataclass


@dataclass
class RPCEndpoint:
    name: str
    url: str
    enabled: bool = True


class RPCBridge:
    def __init__(self):
        self.endpoints: Dict[str, RPCEndpoint] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        self.request_log = []
        
        self.register_default_endpoints()
    
    def register_default_endpoints(self):
        self.endpoints['ipfs_gateway'] = RPCEndpoint(
            name='ipfs_gateway',
            url='https://ipfs.io/ipfs/',
            enabled=False
        )
        
        self.endpoints['merkle_validator'] = RPCEndpoint(
            name='merkle_validator',
            url='http://localhost:8545',
            enabled=False
        )
    
    async def initialize(self):
        self.session = aiohttp.ClientSession()
        logging.info("RPC Bridge initialized")
    
    async def close(self):
        if self.session:
            await self.session.close()
            logging.info("RPC Bridge closed")
    
    async def fetch_ipfs_metadata(self, cid: str) -> Optional[Dict]:
        endpoint = self.endpoints.get('ipfs_gateway')
        if not endpoint or not endpoint.enabled:
            logging.warning("IPFS gateway not enabled")
            return None
        
        try:
            url = f"{endpoint.url}{cid}"
            async with self.session.get(url, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    self.log_request('ipfs_fetch', cid, 'success')
                    return data
                else:
                    self.log_request('ipfs_fetch', cid, f'error_{response.status}')
                    return None
        except Exception as e:
            logging.error(f"IPFS fetch error: {e}")
            self.log_request('ipfs_fetch', cid, f'exception_{type(e).__name__}')
            return None
    
    async def validate_merkle_proof(self, proof: Dict) -> bool:
        endpoint = self.endpoints.get('merkle_validator')
        if not endpoint or not endpoint.enabled:
            logging.debug("Merkle validator not enabled, using local validation")
            return self.local_merkle_validation(proof)
        
        try:
            async with self.session.post(
                endpoint.url,
                json={'method': 'validate_proof', 'params': proof},
                timeout=5
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    self.log_request('merkle_validate', str(proof), 'success')
                    return result.get('valid', False)
                else:
                    self.log_request('merkle_validate', str(proof), f'error_{response.status}')
                    return False
        except Exception as e:
            logging.error(f"Merkle validation RPC error: {e}")
            return self.local_merkle_validation(proof)
    
    def local_merkle_validation(self, proof: Dict) -> bool:
        if 'root' in proof and 'leaf' in proof:
            return len(proof['root']) == 64 and len(proof['leaf']) == 64
        return False
    
    async def fetch_quantum_entropy(self) -> Optional[float]:
        try:
            url = "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint8"
            async with self.session.get(url, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'data' in data and len(data['data']) > 0:
                        entropy = data['data'][0] / 255.0
                        self.log_request('quantum_entropy', 'anu', 'success')
                        return entropy
        except Exception as e:
            logging.debug(f"Quantum entropy fetch failed: {e}")
        
        return None
    
    def log_request(self, request_type: str, target: str, status: str):
        self.request_log.append({
            'type': request_type,
            'target': target,
            'status': status,
            'timestamp': asyncio.get_event_loop().time()
        })
        
        if len(self.request_log) > 1000:
            self.request_log = self.request_log[-1000:]
    
    def enable_endpoint(self, endpoint_name: str):
        if endpoint_name in self.endpoints:
            self.endpoints[endpoint_name].enabled = True
            logging.info(f"Enabled RPC endpoint: {endpoint_name}")
    
    def disable_endpoint(self, endpoint_name: str):
        if endpoint_name in self.endpoints:
            self.endpoints[endpoint_name].enabled = False
            logging.info(f"Disabled RPC endpoint: {endpoint_name}")
    
    def get_status(self) -> Dict:
        return {
            'endpoints': {
                name: {'url': ep.url, 'enabled': ep.enabled}
                for name, ep in self.endpoints.items()
            },
            'total_requests': len(self.request_log),
            'recent_requests': self.request_log[-10:] if self.request_log else []
        }
