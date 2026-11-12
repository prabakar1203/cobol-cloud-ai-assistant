# cobol-cloud-ai-assistant
# Legacy COBOL-to-Cloud AI Assistant

An enterprise-ready, containerized **Generative AI microservice** that analyzes legacy COBOL programs, extracts plain-English business logic, and generates modern Python equivalents via a REST API.

Built to demonstrate how domain-aware parsing and automated CI/CD pipelines can accelerate mainframe-to-cloud modernization safely and auditably.

---

## Architecture Overview

```text
[ COBOL Source (.cbl) ] 
        │
        ▼
[ Domain-Aware Division Splitter ]  ──► Separates DATA & PROCEDURE Divisions
        │
        ▼
[ LLM Modernization Engine ]        ──► Extracts Business Rules + Python Logic
        │
        ▼
[ FastAPI Container (Docker) ]      ──► Exposes /analyze & /health REST Endpoints
```

### Key Features
* **Domain-Aware COBOL Parsing:** Splits `DATA DIVISION` and `PROCEDURE DIVISION` blocks to preserve variable definitions and business rule context.
* **Containerized Microservice:** Packaged with **Docker** and **FastAPI** for portable deployment across AWS, Azure, or on-premise environments.
* **Automated CI Pipeline:** Includes a **GitHub Actions** workflow that validates and builds the container image on every commit.

---

## Quick Start (Local & Docker)

### 1. Run with Docker (Recommended)
```bash
# Build the container image
docker build -t cobol-ai-assistant .

# Run the container
docker run -d -p 8000:8000 -e OPENAI_API_KEY="your-api-key-here" cobol-ai-assistant
```

### 2. Verify Service Health
```bash
curl http://localhost:8000/health
```

---

## Sample Test Request

Test the `/analyze` endpoint using a sample COBOL loan interest calculation snippet:

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "program_name": "CALCINT.CBL",
    "cobol_code": "IDENTIFICATION DIVISION.\nPROGRAM-ID. CALCINT.\nDATA DIVISION.\nWORKING-STORAGE SECTION.\n01 WS-PRINCIPAL PIC 9(7)V99 VALUE 50000.00.\n01 WS-RATE PIC 9V999 VALUE 0.045.\n01 WS-INTEREST PIC 9(7)V99.\nPROCEDURE DIVISION.\nCOMPUTE WS-INTEREST = WS-PRINCIPAL * WS-RATE.\nDISPLAY \"INTEREST: \" WS-INTEREST.\nSTOP RUN."
  }'
```

### Sample Response
```json
{
  "program_name": "CALCINT.CBL",
  "business_logic_summary": "Calculates simple annual interest by multiplying a fixed principal amount ($50,000.00) by an interest rate of 4.5% (0.045) and outputs the resulting interest amount.",
  "python_equivalent": "principal: float = 50000.00\nrate: float = 0.045\ninterest: float = round(principal * rate, 2)\nprint(f'INTEREST: {interest:.2f}')"
}
```

---

## Roadmap
* [ ] Add **RAG (Retrieval-Augmented Generation)** support using ChromaDB to index multi-file COBOL copybooks (`.cpy`).
* [ ] Integrate automated `pytest` generation for every refactored Python module.
* [ ] Add AWS Bedrock / Azure OpenAI provider toggles for enterprise compliance.
