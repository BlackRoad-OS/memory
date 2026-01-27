"""
BlackRoad Memory System - Core Module

Central shared memory and coordination layer for BlackRoad OS.
"""

__version__ = "0.1.0"
__author__ = "BlackRoad OS, Inc."
__license__ = "Proprietary"

from .memory_client import MemoryClient
from .memory_server import MemoryServer

__all__ = [
    "MemoryClient",
    "MemoryServer",
]
