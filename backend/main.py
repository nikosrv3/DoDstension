import json
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from web_scrape import extract_company_from_html, identify_url_type
from grading import calculate_grade
import os

# Load company data at startup
data_path = os.path.join(os.path.dirname(__file__), 'data', 'company_data.json')
with open(data_path, 'r') as f:
    company_data = json.load(f)

app = FastAPI()

class GradeRequest(BaseModel):
    url: str
    companyName: Optional[str] = None

class GradeResponse(BaseModel):
    company: Optional[str]
    total_awards: Optional[int]
    grade: Optional[int]
    error: Optional[str] = None

@app.post("/grades", response_model=GradeResponse)

def compute_grade(req: GradeRequest):
    """
    compute the grade based on the either the company name from the frontend, or further logic from html extraction
    """

    try:
        if req.companyName:
            match = next((k for k in company_data if k.lower() == req.companyName.lower()), None)
            if match:
                total_awards = company_data[match]["total_awards"]
                grade = calculate_grade(total_awards)
                return GradeResponse(company=match, total_awards=total_awards, grade=grade)
        
        url_type = identify_url_type(req.url)
        extracted = extract_company_from_html(req.url, url_type)
        if extracted:
            match = next((k for k in company_data if k.lower() == extracted.lower()), None)
            if match:
                total_awards = company_data[match]["total_awards"]
                grade = calculate_grade(total_awards)
                return GradeResponse(company=match, total_awards=total_awards, grade=grade)
            else:
                return GradeResponse(company=extracted, total_awards=None, grade=None, error="Company not found in data.")

        return GradeResponse(company=None, total_awards=None, grade=None, error="Company name could not be extracted.")
    except Exception as e:
        return GradeResponse(company=None, total_awards=None, grade=None, error=str(e))
    
"""
def get_grade(url: str = Query(..., description="URL of the company website")):
    try:
        
        url_type = identify_url_type(url)
        company_name = extract_company_from_html(url, url_type)
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
"""