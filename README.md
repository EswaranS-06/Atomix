# ATOMIX

## Atomic Target Orchestration for Mapping, Intelligence & eXploitation

**ATOMIX** is a modular, profile‑driven **Web Reconnaissance Automation Engine** designed to orchestrate industry‑standard security tools in a clean, scalable, and production‑ready architecture.

The project focuses on **execution correctness, data integrity, and extensibility** rather than ad‑hoc scanning. ATOMIX is built as a backend‑first system with clear separation between execution, persistence, and future intelligence layers.

---

## 🚀 Project Status

**Current Phase:** Phase 4 – Execution & Persistence (Completed)

ATOMIX is currently capable of:

* Creating and managing scans via API
* Executing recon tools in isolated Docker containers
* Persisting raw and normalized outputs
* Managing scan lifecycle states

The intelligence and reporting layers will be introduced in upcoming phases.

---

## 🧠 Core Design Principles

* **Profile‑Driven Execution** – Tools and arguments are defined declaratively
* **Docker‑Isolated Tooling** – No tool runs directly on the host
* **State‑Driven Scans** – Strict lifecycle enforcement
* **Raw Output Preservation** – Nothing is lost or overwritten
* **Clean Output Normalization** – ANSI‑free outputs for UI and parsing
* **Future‑Proof Architecture** – Parsing and CVE logic intentionally deferred

---

## 🏗️ Architecture Overview

```bash
Client / UI
    │
    ▼
Django REST API
    │
    ├── Scan Management
    │   ├── Create Scan
    │   ├── Queue Scan
    │   └── Scan Status
    │
    ├── Executor (Python)
    │   ├── Docker SDK
    │   ├── Tool Runner
    │   └── State Transitions
    │
    └── MongoDB
        ├── scans
        └── results
```

---

## 🔧 Technology Stack

### Backend

* **Python 3.12**
* **Django** (API‑first)
* **UV** (Python runtime & dependency manager)
* **Docker SDK for Python**

### Database

* **MongoDB** (document‑based storage)

### Recon Tools (via Docker)

* WhatWeb
* Nikto
* Amass
* FFUF
* SQLMap
* XSStrike

---

## 📂 Project Structure

```bash
backend/
├── config/                 # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── db/
│       └── mongo.py         # MongoDB connection
│
├── scans/                   # Core domain
│   ├── api/                 # API views & serializers
│   ├── executor/            # Scan execution engine
│   │   ├── runner.py
│   │   └── docker_runner.py
│   ├── repository.py        # Mongo persistence layer
│   ├── results.py           # Result builder & storage
│   ├── utils/
│   │   └── output.py        # ANSI normalization
│   └── apps.py              # States & transitions
│
├── profiles/                # Recon profiles (YAML)
│   └── default.yaml
│
└── manage.py
```

---

## 🔄 Scan Lifecycle

Each scan follows a strict, enforced lifecycle:

```bash
CREATED → QUEUED → RUNNING → COMPLETED
                    └─────→ FAILED
```

Invalid state transitions are rejected by design.

---

## 📑 Recon Profiles

Profiles define **what tools run and how**.

Example: `profiles/default.yaml`

```yaml
profile: default
desc: Basic passive + light active recon
type: Both

tools:
  - name: whatweb
    info: Web technology fingerprinting
    args:
      - whatweb
      - --no-errors
      - --color=never
      - "{target}"
    regex: null

  - name: nikto
    info: Web server vulnerability scanner
    args:
      - nikto
      - -h
      - "http://{target}"
    regex: null
```

Parsing (`regex`) is intentionally deferred to future phases.

---

## 📊 Data Storage Model

### `scans` Collection

```json
{
  "scan_id": "uuid",
  "target": "example.com",
  "profile": "default",
  "state": "COMPLETED",
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

### `results` Collection

```json
{
  "scan_id": "uuid",
  "tool": "whatweb",
  "raw_output": "<original output>",
  "clean_output": "<ansi‑stripped output>",
  "created_at": "ISODate"
}
```

---

## ▶️ Running the Project (Development)

### 1. Start MongoDB

```bash
docker compose up -d mongodb
```

### 2. Run Django API

```bash
uv run python manage.py runserver
```

### 3. Create a Scan

```bash
curl -X POST http://127.0.0.1:8000/api/scans/ \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "profile": "default"}'
```

### 4. Queue the Scan

```bash
curl -X POST http://127.0.0.1:8000/api/scans/<scan_id>/queue/
```

### 5. Run Executor

```bash
uv run python manage.py shell
```

```python
from scans.executor.runner import process_queued_scans
process_queued_scans()
```

---

## 🧩 Git History (Milestones)

* **Recon engine & Mongo setup**
* **Project base & Django config**
* **Scan structure & APIs**
* **Tool execution & persistence**

Each phase is committed cleanly and incrementally.

---

## 🛣️ Roadmap

### Phase 5 (Upcoming)

* Findings domain model
* Structured issue extraction
* Severity normalization
* Result aggregation API

### Phase 6

* Reporting engine
* UI integration
* CVE enrichment

---

## ⚠️ Disclaimer

ATOMIX is intended for **authorized security testing only**.
Running recon or vulnerability tools against targets without explicit permission may be illegal.

---

## 👤 Author

**Eswaran S**
Cybersecurity Student & Builder

---

## ⭐ Acknowledgements

Inspired by real‑world recon workflows and modern security automation practices.

---

**ATOMIX** — *From raw recon to structured intelligence.*
