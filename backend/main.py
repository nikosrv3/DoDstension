import json
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from web_scrape import extract_company_from_html
from grading import calculate_grade
import os

# Load company data at startup
data_path = os.path.join(os.path.dirname(__file__), 'data', 'company_data.json')
with open(data_path, 'r') as f:
    company_data = json.load(f)

app = FastAPI()

class GradeResponse(BaseModel):
    company: Optional[str]
    total_awards: Optional[int]
    grade: Optional[int]
    error: Optional[str] = None

@app.get("/get_grade", response_model=GradeResponse)
def get_grade(url: str = Query(..., description="URL of the company website")):
    try:
        company_name = extract_company_from_html(url)
        if not company_name:
            return GradeResponse(company=None, total_awards=None, grade=None, error="Company name could not be extracted.")
        # Try to match company name in data (case-insensitive, exact match)
        match = next((k for k in company_data if k.lower() == company_name.lower()), None)
        if not match:
            return GradeResponse(company=company_name, total_awards=None, grade=None, error="Company not found in data.")
        total_awards = company_data[match]["total_awards"]
        grade = calculate_grade(total_awards)
        return GradeResponse(company=match, total_awards=total_awards, grade=grade)
    except Exception as e:
        return GradeResponse(company=None, total_awards=None, grade=None, error=str(e))