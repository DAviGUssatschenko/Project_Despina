"""
split_tifs.py
-------------
Separa cada GeoTIFF multi-banda (6 índices empilhados) em 6 arquivos
individuais — um por índice — preservando CRS, transform e metadados.

Uso:
    python src/seca/features/split_tifs.py

Saída:
    data/processed/output_indices/case_*/tifs/
        NBR/    NBR_{data}.tif
        NDRE/   NDRE_{data}.tif
        MSI/    MSI_{data}.tif
        GNDVI/  GNDVI_{data}.tif
        SAVI/   SAVI_{data}.tif
        NDDI/   NDDI_{data}.tif
"""

import numpy as np
import rasterio
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

# =============================================================================
# CONFIGURAÇÃO
# =============================================================================

OUTPUT_DIR   = Path("data/processed/output_indices")
ONLY_CASE    = None          # None = todos; ex: "case_114_Seca" = só esse
INDEX_NAMES  = ["NBR", "NDRE", "MSI", "GNDVI", "SAVI", "NDDI"]
NODATA_VALUE = -9999.0

# =============================================================================

def split_tif(tif_path: Path, out_base_dir: Path):
    parts    = tif_path.stem.split("_")
    date_str = next((p for p in parts if len(p) == 10 and p[4] == "-"), tif_path.stem)
    print(f"    Abrindo: {tif_path.name}")

    with rasterio.open(tif_path) as src:
        n_bands     = src.count
        profile     = src.profile.copy()
        nodata_orig = src.nodata
        print(f"    Bandas: {n_bands} | CRS: {src.crs} | Shape: {src.shape}")

        for band_idx, idx_name in enumerate(INDEX_NAMES[:n_bands], start=1):
            out_dir  = out_base_dir / idx_name
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / f"{idx_name}_{date_str}.tif"

            data = src.read(band_idx).astype(np.float32)
            if nodata_orig is not None:
                data[data == nodata_orig] = NODATA_VALUE
            data[~np.isfinite(data)] = NODATA_VALUE

            out_profile = profile.copy()
            out_profile.update({"count": 1, "dtype": "float32",
                                 "nodata": NODATA_VALUE,
                                 "compress": "deflate", "predictor": 3})

            with rasterio.open(out_path, "w", **out_profile) as dst:
                dst.write(data, 1)
                dst.update_tags(index=idx_name, source=tif_path.name, date=date_str)

            size_kb = out_path.stat().st_size / 1024
            print(f"      -> {idx_name}/{out_path.name}  ({size_kb:.1f} KB)")


def process_case(case_dir: Path):
    tif_files = sorted(f for f in case_dir.glob("*.tif"))
    if not tif_files:
        print(f"  [AVISO] Nenhum .tif na raiz de {case_dir.name}"); return

    out_base = case_dir / "tifs"
    out_base.mkdir(exist_ok=True)
    print(f"\n{'='*55}\nCaso: {case_dir.name}")
    print(f"TIFs encontrados: {[f.name for f in tif_files]}")

    for tif_path in tif_files:
        split_tif(tif_path, out_base)

    print(f"\n  Resultado:")
    for idx_name in INDEX_NAMES:
        idx_dir = out_base / idx_name
        n = len(list(idx_dir.glob("*.tif"))) if idx_dir.exists() else 0
        print(f"    {idx_name}/  → {n} arquivo(s)")


def main():
    print("=" * 55)
    print("Separador de TIFs multi-banda → 1 banda por arquivo")
    print("=" * 55)

    if not OUTPUT_DIR.exists():
        print(f"[ERRO] Pasta não encontrada: {OUTPUT_DIR}"); return

    cases = ([OUTPUT_DIR / ONLY_CASE] if ONLY_CASE
             else sorted(d for d in OUTPUT_DIR.iterdir()
                         if d.is_dir() and d.name.startswith("case_")))

    print(f"Casos encontrados: {len(cases)}")
    for case_dir in cases:
        try: process_case(case_dir)
        except Exception as e:
            import traceback
            print(f"[ERRO] {case_dir.name}: {e}"); traceback.print_exc()

    print("\nConcluído.")


if __name__ == "__main__":
    main()
