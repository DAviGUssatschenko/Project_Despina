"""
config.py — Parâmetros, thresholds e constantes do sistema
"""

import os
from pathlib import Path

# Carrega variáveis do arquivo .env se existir (sem obrigar dependência em prod)
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass  # python-dotenv não instalado — variáveis devem vir do ambiente (Docker, CI, etc.)

# ─────────────────────────────────────────────
# POSEIDON — Tabelas do banco PostgreSQL
# ─────────────────────────────────────────────
POSEIDON_TABLES = {
    "coordinates": "poseidon.points_coordinates",
    "weather":     "poseidon.weather_data_processed",
}

POSEIDON_GRID_STEP = 0.09009

# ─────────────────────────────────────────────
# CREDENCIAIS COPERNICUS
# ─────────────────────────────────────────────
CDSE_CLIENT_ID     = os.getenv("CDSE_CLIENT_ID", "")
CDSE_CLIENT_SECRET = os.getenv("CDSE_CLIENT_SECRET", "")

CDSE_TOKEN_URL   = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
CDSE_STATS_URL   = "https://sh.dataspace.copernicus.eu/api/v1/statistics"
CDSE_CATALOG_URL = "https://sh.dataspace.copernicus.eu/api/v1/catalog/1.0.0/search"

SENTINEL2_RESOLUTION  = 20
MAX_CLOUD_COVER       = 20
BASELINE_LOOKBACK_DAYS = 60

# ─────────────────────────────────────────────
# EMBRAPA — Dados de Solo
# ─────────────────────────────────────────────
_BASE_DIR = Path(__file__).parent
EMBRAPA_SHAPEFILE = os.getenv(
    "EMBRAPA_SHAPEFILE",
    str(_BASE_DIR / "data" / "embrapa" / "aptagr_bra.shp"),
)

# Diretório de saída para imagens de índices (usado em appv25.py)
OUTPUT_INDICES_DIR = Path(
    os.getenv("OUTPUT_INDICES_DIR", str(_BASE_DIR / "output_indices"))
)

# Classes de aptidão agrícola EMBRAPA
SOIL_APTITUDE_CLASSES = {
    1: {"label": "Boa",           "suitable": True,  "description": "Terras de boa aptidão para lavouras"},
    2: {"label": "Regular",       "suitable": True,  "description": "Terras de aptidão regular para lavouras"},
    3: {"label": "Restrita",      "suitable": True,  "description": "Terras de aptidão restrita para lavouras"},
    4: {"label": "Inapta (past)", "suitable": False, "description": "Inapta para lavouras — indicada para pastagem"},
    5: {"label": "Inapta (sil)",  "suitable": False, "description": "Inapta para lavouras — indicada para silvicultura"},
    6: {"label": "Preservação",   "suitable": False, "description": "Terras indicadas para preservação ambiental"},
}

# Propriedades hídricas por tipo de solo
SOIL_WATER_PROPERTIES = {
    "Latossolo Vermelho":         {"AWC": 120, "Ks": 30, "fc": 35, "wp": 15, "retencao": "média",       "textura": "argilosa"},
    "Latossolo Amarelo":          {"AWC": 100, "Ks": 25, "fc": 32, "wp": 14, "retencao": "média",       "textura": "argilo-arenosa"},
    "Latossolo Vermelho-Amarelo": {"AWC": 110, "Ks": 28, "fc": 33, "wp": 14, "retencao": "média",       "textura": "argilosa"},
    "Argissolo Vermelho":         {"AWC":  80, "Ks":  8, "fc": 30, "wp": 18, "retencao": "alta",        "textura": "argilosa"},
    "Argissolo Amarelo":          {"AWC":  90, "Ks": 10, "fc": 31, "wp": 17, "retencao": "alta",        "textura": "argilo-arenosa"},
    "Nitossolo Vermelho":         {"AWC": 130, "Ks": 15, "fc": 38, "wp": 18, "retencao": "alta",        "textura": "muito argilosa"},
    "Cambissolo Húmico":          {"AWC":  70, "Ks": 20, "fc": 28, "wp": 13, "retencao": "média-baixa", "textura": "média"},
    "Cambissolo Háplico":         {"AWC":  60, "Ks": 18, "fc": 26, "wp": 12, "retencao": "média-baixa", "textura": "média"},
    "Neossolo Litólico":          {"AWC":  30, "Ks": 50, "fc": 20, "wp":  8, "retencao": "baixa",       "textura": "arenosa"},
    "Neossolo Quartzarênico":     {"AWC":  40, "Ks": 80, "fc": 18, "wp":  5, "retencao": "muito baixa", "textura": "arenosa"},
    "Neossolo Flúvico":           {"AWC": 100, "Ks": 15, "fc": 30, "wp": 15, "retencao": "alta",        "textura": "média"},
    "Gleissolo Háplico":          {"AWC": 150, "Ks":  2, "fc": 45, "wp": 25, "retencao": "muito alta",  "textura": "muito argilosa"},
    "Gleissolo Melânico":         {"AWC": 160, "Ks":  1, "fc": 48, "wp": 26, "retencao": "muito alta",  "textura": "muito argilosa"},
    "Espodossolo":                {"AWC":  50, "Ks": 40, "fc": 22, "wp":  8, "retencao": "baixa",       "textura": "arenosa"},
    "Planossolo Háplico":         {"AWC":  80, "Ks":  3, "fc": 32, "wp": 18, "retencao": "muito alta",  "textura": "argilosa"},
    "Vertissolo":                 {"AWC": 160, "Ks":  1, "fc": 48, "wp": 28, "retencao": "muito alta",  "textura": "muito argilosa"},
    "Chernossolo":                {"AWC": 140, "Ks": 12, "fc": 40, "wp": 20, "retencao": "alta",        "textura": "argilosa"},
    "Organossolo":                {"AWC": 200, "Ks":  2, "fc": 60, "wp": 30, "retencao": "muito alta",  "textura": "orgânica"},
    "default":                    {"AWC": 100, "Ks": 20, "fc": 30, "wp": 15, "retencao": "média",       "textura": "média"},
}

# Mapeamento de prefixo de código EMBRAPA → nome completo em SOIL_WATER_PROPERTIES
SOIL_CODE_ALIASES = {
    "lva":  "Latossolo Vermelho-Amarelo",
    "lv":   "Latossolo Vermelho",
    "la":   "Latossolo Amarelo",
    "pv":   "Argissolo Vermelho",
    "pa":   "Argissolo Amarelo",
    "nv":   "Nitossolo Vermelho",
    "ch":   "Cambissolo Húmico",
    "cx":   "Cambissolo Háplico",
    "rl":   "Neossolo Litólico",
    "rq":   "Neossolo Quartzarênico",
    "ru":   "Neossolo Flúvico",
    "gx":   "Gleissolo Háplico",
    "gm":   "Gleissolo Melânico",
    "es":   "Espodossolo",
    "sx":   "Planossolo Háplico",
    "vx":   "Vertissolo",
    "mk":   "Chernossolo",
    "oj":   "Organossolo",
}

# Fator de amplificação do dano por tipo de solo e evento
SOIL_EVENT_AMPLIFIER = {
    "seca": {
        "muito baixa": 1.35,
        "baixa":       1.20,
        "média-baixa": 1.10,
        "média":       1.00,
        "alta":        0.90,
        "muito alta":  0.80,
    },
    "chuva": {
        "muito baixa": 0.75,
        "baixa":       0.80,
        "média-baixa": 0.95,
        "média":       1.00,
        "alta":        1.15,
        "muito alta":  1.40,
    },
    "geada": {
        "muito baixa": 1.05,
        "baixa":       1.02,
        "média-baixa": 1.00,
        "média":       1.00,
        "alta":        0.98,
        "muito alta":  0.95,
    },
    "granizo": {
        "muito baixa": 1.10,
        "baixa":       1.05,
        "média-baixa": 1.00,
        "média":       1.00,
        "alta":        1.00,
        "muito alta":  1.05,
    },
}

# ─────────────────────────────────────────────
# ÍNDICES SENTINEL-2 — Evalscripts
# ─────────────────────────────────────────────
EVALSCRIPTS = {
    "NDVI": """
//VERSION=3
function setup() {
  return {
    input: [{ bands: ["B04","B08","dataMask"] }],
    output: [
      { id: "default",  bands: 1, sampleType: "FLOAT32" },
      { id: "dataMask", bands: 1 }
    ]
  };
}
function evaluatePixel(s) {
  return {
    default:  [(s.B08 - s.B04) / (s.B08 + s.B04 + 1e-10)],
    dataMask: [s.dataMask]
  };
}""",

    "NDRE": """
//VERSION=3
function setup() {
  return {
    input: [{ bands: ["B05","B08","dataMask"] }],
    output: [
      { id: "default",  bands: 1, sampleType: "FLOAT32" },
      { id: "dataMask", bands: 1 }
    ]
  };
}
function evaluatePixel(s) {
  return {
    default:  [(s.B08 - s.B05) / (s.B08 + s.B05 + 1e-10)],
    dataMask: [s.dataMask]
  };
}""",

    "EVI": """
//VERSION=3
function setup() {
  return {
    input: [{ bands: ["B02","B04","B08","dataMask"] }],
    output: [
      { id: "default",  bands: 1, sampleType: "FLOAT32" },
      { id: "dataMask", bands: 1 }
    ]
  };
}
function evaluatePixel(s) {
  return {
    default:  [2.5 * (s.B08 - s.B04) / (s.B08 + 6*s.B04 - 7.5*s.B02 + 1 + 1e-10)],
    dataMask: [s.dataMask]
  };
}""",

    "NDWI": """
//VERSION=3
function setup() {
  return {
    input: [{ bands: ["B03","B08","dataMask"] }],
    output: [
      { id: "default",  bands: 1, sampleType: "FLOAT32" },
      { id: "dataMask", bands: 1 }
    ]
  };
}
function evaluatePixel(s) {
  return {
    default:  [(s.B03 - s.B08) / (s.B03 + s.B08 + 1e-10)],
    dataMask: [s.dataMask]
  };
}""",

    "NDMI": """
//VERSION=3
function setup() {
  return {
    input: [{ bands: ["B08","B11","dataMask"] }],
    output: [
      { id: "default",  bands: 1, sampleType: "FLOAT32" },
      { id: "dataMask", bands: 1 }
    ]
  };
}
function evaluatePixel(s) {
  return {
    default:  [(s.B08 - s.B11) / (s.B08 + s.B11 + 1e-10)],
    dataMask: [s.dataMask]
  };
}""",

    "BSI": """
//VERSION=3
function setup() {
  return {
    input: [{ bands: ["B02","B04","B08","B11","dataMask"] }],
    output: [
      { id: "default",  bands: 1, sampleType: "FLOAT32" },
      { id: "dataMask", bands: 1 }
    ]
  };
}
function evaluatePixel(s) {
  return {
    default:  [((s.B11 + s.B04) - (s.B08 + s.B02)) / ((s.B11 + s.B04) + (s.B08 + s.B02) + 1e-10)],
    dataMask: [s.dataMask]
  };
}""",

    "NBR": """
//VERSION=3
function setup() {
  return {
    input: [{ bands: ["B08","B12","dataMask"] }],
    output: [
      { id: "default",  bands: 1, sampleType: "FLOAT32" },
      { id: "dataMask", bands: 1 }
    ]
  };
}
function evaluatePixel(s) {
  return {
    default:  [(s.B08 - s.B12) / (s.B08 + s.B12 + 1e-10)],
    dataMask: [s.dataMask]
  };
}""",

    "PSRI": """
//VERSION=3
function setup() {
  return {
    input: [{ bands: ["B02","B04","B06","dataMask"] }],
    output: [
      { id: "default",  bands: 1, sampleType: "FLOAT32" },
      { id: "dataMask", bands: 1 }
    ]
  };
}
function evaluatePixel(s) {
  return {
    default:  [(s.B04 - s.B02) / (s.B06 + 1e-10)],
    dataMask: [s.dataMask]
  };
}""",

    "CRI1": """
//VERSION=3
function setup() {
  return {
    input: [{ bands: ["B02","B03","dataMask"] }],
    output: [
      { id: "default",  bands: 1, sampleType: "FLOAT32" },
      { id: "dataMask", bands: 1 }
    ]
  };
}
function evaluatePixel(s) {
  let v = (1/(s.B02 + 1e-10)) - (1/(s.B03 + 1e-10));
  return {
    default:  [Math.min(Math.max(v, -1), 1)],
    dataMask: [s.dataMask]
  };
}""",
}

# ─────────────────────────────────────────────
# THRESHOLDS DE VALIDAÇÃO
# ─────────────────────────────────────────────
VALIDATION_THRESHOLDS = {
    "seca": {
        "poseidon": {
            "prcp_deficit_pct": 40,
            "tavg_anomaly_c":    2.0,
            "rh_avg_max":       60.0,
        },
        "satellite": {
            "ndvi_drop_pct":    25,
            "ndwi_threshold":  -0.05,
            "ndmi_threshold":  -0.10,
            "bsi_increase":     0.05,
            "vhi_critical":    40.0,
        }
    },
    "chuva": {
        "poseidon": {
            "prcp_excess_pct":      150,
            "wspd_max_threshold":    30.0,
            "rh_avg_min":            85.0,
        },
        "satellite": {
            "ndwi_threshold":   0.20,
            "ndvi_drop_pct":    15,
            "bsi_increase":     0.10,
        }
    },
    "geada": {
        "poseidon": {
            "tmin_threshold":   2.0,
            "consecutive_days": 2,
        },
        "satellite": {
            "ndvi_drop_pct":   30,
            "psri_increase":    0.05,
            "ndre_drop_pct":   35,
        }
    },
    "granizo": {
        "poseidon": {
            "wspd_max_threshold": 40.0,
            "prcp_daily_max":     30.0,
        },
        "satellite": {
            "ndvi_drop_pct":    20,
            "nbr_drop_pct":     15,
            "bsi_increase":     0.08,
        }
    },
}

# ─────────────────────────────────────────────
# PARÂMETROS AGRONÔMICOS
# ─────────────────────────────────────────────
CROP_PARAMS = {
    "soja": {
        "name_pt":             "Soja",
        "yield_min_sacas_ha":  40,
        "yield_avg_sacas_ha":  52,
        "yield_max_sacas_ha":  65,
        "price_brl_saca":      145.0,
        "saca_kg":             60,
        "cycle_days":          120,
        "critical_phases": {
            "germinacao":    (0,   15),
            "vegetativo":    (15,  55),
            "florescimento": (55,  75),
            "enchimento":    (75, 100),
            "maturacao":     (100,120),
        },
        "yield_loss_factor": {
            "germinacao":    0.40,
            "vegetativo":    0.50,
            "florescimento": 0.85,
            "enchimento":    0.90,
            "maturacao":     0.30,
        },
        "ndvi_healthy_min": 0.60,
        "ndvi_critical":    0.35,
    },
    "milho": {
        "name_pt":             "Milho",
        "yield_min_sacas_ha":  100,
        "yield_avg_sacas_ha":  140,
        "yield_max_sacas_ha":  180,
        "price_brl_saca":       58.0,
        "saca_kg":             60,
        "cycle_days":          130,
        "critical_phases": {
            "germinacao":    (0,   10),
            "vegetativo":    (10,  60),
            "pendoamento":   (60,  75),
            "espigamento":   (75,  90),
            "enchimento":    (90, 120),
            "maturacao":     (120,130),
        },
        "yield_loss_factor": {
            "germinacao":    0.30,
            "vegetativo":    0.55,
            "pendoamento":   0.80,
            "espigamento":   0.95,
            "enchimento":    0.85,
            "maturacao":     0.25,
        },
        "ndvi_healthy_min": 0.65,
        "ndvi_critical":    0.38,
    },
    "trigo": {
        "name_pt":             "Trigo",
        "yield_min_sacas_ha":  40,
        "yield_avg_sacas_ha":  55,
        "yield_max_sacas_ha":  70,
        "price_brl_saca":       90.0,
        "saca_kg":             60,
        "cycle_days":          110,
        "critical_phases": {
            "germinacao":    (0,   15),
            "afilhamento":   (15,  40),
            "espigamento":   (40,  60),
            "graos":         (60,  90),
            "maturacao":     (90, 110),
        },
        "yield_loss_factor": {
            "germinacao":    0.45,
            "afilhamento":   0.60,
            "espigamento":   0.90,
            "graos":         0.80,
            "maturacao":     0.20,
        },
        "ndvi_healthy_min": 0.55,
        "ndvi_critical":    0.30,
    },
    "arroz": {
        "name_pt":             "Arroz",
        "yield_min_sacas_ha":  130,
        "yield_avg_sacas_ha":  170,
        "yield_max_sacas_ha":  210,
        "price_brl_saca":       55.0,
        "saca_kg":             50,
        "cycle_days":          120,
        "critical_phases": {
            "germinacao":    (0,   15),
            "vegetativo":    (15,  60),
            "floracao":      (60,  80),
            "graos":         (80, 105),
            "maturacao":     (105,120),
        },
        "yield_loss_factor": {
            "germinacao":    0.35,
            "vegetativo":    0.60,
            "floracao":      0.92,
            "graos":         0.85,
            "maturacao":     0.15,
        },
        "ndvi_healthy_min": 0.60,
        "ndvi_critical":    0.35,
    },
}

# ─────────────────────────────────────────────
# NORMAIS CLIMÁTICAS — Rio Grande do Sul
# ─────────────────────────────────────────────
CLIMATE_NORMALS_RS = {
    1:  {"prcp_mm": 130, "tavg_c": 24.5},
    2:  {"prcp_mm": 115, "tavg_c": 24.2},
    3:  {"prcp_mm": 105, "tavg_c": 22.8},
    4:  {"prcp_mm":  90, "tavg_c": 19.5},
    5:  {"prcp_mm": 100, "tavg_c": 16.0},
    6:  {"prcp_mm": 130, "tavg_c": 13.5},
    7:  {"prcp_mm": 120, "tavg_c": 13.0},
    8:  {"prcp_mm":  95, "tavg_c": 14.5},
    9:  {"prcp_mm": 115, "tavg_c": 16.5},
    10: {"prcp_mm": 145, "tavg_c": 19.5},
    11: {"prcp_mm": 120, "tavg_c": 22.0},
    12: {"prcp_mm": 135, "tavg_c": 24.0},
}
