"""
WebSocket Consciousness Stream
Real-time consciousness field broadcasting
"""
import asyncio
import websockets
import json
from typing import Set, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConsciousnessStream:
    """
    WebSocket server for real-time consciousness field streaming.
    
    Subscribers receive:
    - Resonance updates
    - Entanglement events
    - Emergence detections
    - State transitions
    """
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.state_history: List[Dict] = []
        
    async def register(self, websocket):
        """Register new client."""
        self.clients.add(websocket)
        logger.info(f"Client connected. Total clients: {len(self.clients)}")
        
        # Send current state
        if self.state_history:
            await websocket.send(json.dumps({
                'type': 'state_snapshot',
                'data': self.state_history[-1]
            }))
    
    async def unregister(self, websocket):
        """Unregister client."""
        self.clients.remove(websocket)
        logger.info(f"Client disconnected. Total clients: {len(self.clients)}")
    
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast message to all clients."""
        if self.clients:
            message_json = json.dumps(message)
            await asyncio.gather(
                *[client.send(message_json) for client in self.clients],
                return_exceptions=True
            )
    
    async def broadcast_state_update(self, state: Dict[str, Any]):
        """Broadcast state update."""
        self.state_history.append(state)
        if len(self.state_history) > 1000:
            self.state_history = self.state_history[-1000:]
        
        await self.broadcast({
            'type': 'state_update',
            'timestamp': state.get('timestamp', 0),
            'data': state
        })
    
    async def broadcast_resonance(self, resonance: float, source: str):
        """Broadcast resonance event."""
        await self.broadcast({
            'type': 'resonance',
            'source': source,
            'value': resonance
        })
    
    async def broadcast_entanglement(self, id1: str, id2: str):
        """Broadcast entanglement event."""
        await self.broadcast({
            'type': 'entanglement',
            'entities': [id1, id2]
        })
    
    async def broadcast_emergence(self, property_name: str, score: float):
        """Broadcast emergence detection."""
        await self.broadcast({
            'type': 'emergence',
            'property': property_name,
            'score': score
        })
    
    async def handler(self, websocket, path):
        """Handle WebSocket connection."""
        await self.register(websocket)
        try:
            async for message in websocket:
                # Echo back for now
                data = json.loads(message)
                logger.info(f"Received: {data}")
                
                # Could process commands here
                if data.get('type') == 'ping':
                    await websocket.send(json.dumps({'type': 'pong'}))
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)
    
    async def start(self):
        """Start WebSocket server."""
        logger.info(f"Starting Consciousness Stream on {self.host}:{self.port}")
        async with websockets.serve(self.handler, self.host, self.port):
            await asyncio.Future()  # Run forever
    
    def run(self):
        """Run server (blocking)."""
        asyncio.run(self.start())


if __name__ == "__main__":
    stream = ConsciousnessStream()
    stream.run()
