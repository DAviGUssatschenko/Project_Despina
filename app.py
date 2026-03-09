"""
app.py — Entry point.
Delegates entirely to climate_dashboard.py (Poseidon IDW + Sentinel-2 STAC).
"""

from climate_dashboard import main

if __name__ == "__main__":
    main()
