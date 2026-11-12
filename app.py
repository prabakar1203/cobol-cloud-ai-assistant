import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(
    title="Legacy COBOL-to-Cloud AI Assistant",
    description="Analyzes legacy COBOL programs and generates business documentation and Python REST API equivalents.",
    version="1.0.0"
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CobolRequest(BaseModel):
    program_name: str
    cobol_code: str

class ModernizationResponse(BaseModel):
    program_name: str
    business_logic_summary: str
    python_equivalent: str

def split_cobol_divisions(code: str) -> dict:
    """Domain-aware parser separating Data and Procedure divisions."""
    upper_code = code.upper()
    data_idx = upper_code.find("DATA DIVISION")
    proc_idx = upper_code.find("PROCEDURE DIVISION")
    
    return {
        "header": code[:data_idx] if data_idx != -1 else "",
        "data_division": code[data_idx:proc_idx] if (data_idx != -1 and proc_idx != -1) else "",
        "procedure_division": code[proc_idx:] if proc_idx != -1 else code
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "cobol-modernization-ai"}

@app.post("/analyze", response_model=ModernizationResponse)
def analyze_cobol(request: CobolRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured.")
    
    sections = split_cobol_divisions(request.cobol_code)
    
    prompt = f"""
    You are an Enterprise Mainframe Modernization Architect. Analyze the following COBOL program ({request.program_name}).
    
    DATA DIVISION:
    {sections['data_division']}
    
    PROCEDURE DIVISION:
    {sections['procedure_division']}
    
    Provide two clearly separated outputs:
    1. A concise plain-English summary of the business rules, inputs, and edge cases.
    2. Clean, production-grade Python code replicating the exact business logic.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You specialize in refactoring legacy COBOL into modern Python microservices."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        content = response.choices[0].message.content
        parts = content.split("```python")
        summary = parts[0].strip()
        py_code = parts[1].replace("```", "").strip() if len(parts) > 1 else "See summary."
        
        return ModernizationResponse(
            program_name=request.program_name,
            business_logic_summary=summary,
            python_equivalent=py_code
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
