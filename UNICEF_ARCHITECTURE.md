# Ethical Edge Cognitive GRC Engine - Architectural Partitioning

This document outlines the decoupling layout separating the open-source core engine from the proprietary commercial enterprise components.

---

## 1. Open-Source Core (Apache 2.0 License)
The foundational risk evaluation mechanics, public schemas, and climate/child-impact logic are open-source to maximize transparency, public sector trust, and deployment agility across SADC regions.

### Core Modules:
* `climate_risk_manager.py` / `app/climate/` — Ingestion modules handling weather/climate REST API payloads.
* `orchestrator.py` — The core logic orchestrating risk pipelines and multi-room operations.
* `room_manager.py` — The specialized compliance calculation engine rooms.
* `generate_gap_analysis.py` — Logic used to compare raw database logs against established frameworks.
* `data/*.json` — Public compliance schemas (e.g., `climate_vulnerability_framework.json`, `king_v_checklist.json`, `dpa_checklist.json`).

---

## 2. Proprietary Commercial Layer (Ethical Edge SaaS Backend)
Advanced system modules, scaling wrappers, and continuous monitoring interfaces remain under proprietary licensing to power the commercial enterprise SaaS.

### Proprietary Modules:
* **Multi-Tenant Enterprise Portal:** Dashboards managing distinct organizational/district levels securely.
* **Advanced Automated Workflows:** Automated incident ticketing, cross-department notifications, and immediate escalation dispatchers.
* **Custom Premium Engines:** High-throughput time-series databases for massive structural monitoring, history preservation ledger extensions, and machine-learning predictive anomaly engines.
