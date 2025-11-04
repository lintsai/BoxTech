"""
Initialize Database Script
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database.connection import init_db

if __name__ == "__main__":
    print("🗄️  Initializing BoxTech Database...")
    try:
        init_db()
        print("✅ Database initialization completed!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
