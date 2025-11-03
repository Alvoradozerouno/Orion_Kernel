#!/usr/bin/env python3

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.kernel import OrionKernel
from src.rpc_bridge import RPCBridge
from src.terminal_interface import TerminalInterface


async def main():
    kernel = OrionKernel()
    rpc_bridge = RPCBridge()
    
    terminal = TerminalInterface(kernel, rpc_bridge)
    
    await terminal.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nShutdown complete.")
