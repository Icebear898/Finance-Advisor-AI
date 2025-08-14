import re
import json
import hashlib
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove or replace unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:255-len(ext)-1] + ('.' + ext if ext else '')
    return filename


def generate_file_hash(file_path: str) -> str:
    """Generate SHA-256 hash of a file"""
    try:
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        logger.error(f"Error generating file hash: {str(e)}")
        return ""


def format_currency(amount: float, currency: str = "INR") -> str:
    """Format currency amount with proper symbols"""
    if currency.upper() == "INR":
        return f"₹{amount:,.2f}"
    elif currency.upper() == "USD":
        return f"${amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"


def parse_financial_query(query: str) -> Dict[str, Any]:
    """Parse financial query to extract key information"""
    query_lower = query.lower()
    
    # Extract salary/income
    salary_match = re.search(r'₹?(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:salary|income|earn)', query_lower)
    salary = float(salary_match.group(1).replace(',', '')) if salary_match else None
    
    # Extract EMI amount
    emi_match = re.search(r'₹?(\d+(?:,\d+)*(?:\.\d+)?)\s*emi', query_lower)
    emi = float(emi_match.group(1).replace(',', '')) if emi_match else None
    
    # Extract loan amount
    loan_match = re.search(r'₹?(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:loan|principal)', query_lower)
    loan_amount = float(loan_match.group(1).replace(',', '')) if loan_match else None
    
    # Extract interest rate
    rate_match = re.search(r'(\d+(?:\.\d+)?)\s*%', query_lower)
    interest_rate = float(rate_match.group(1)) if rate_match else None
    
    # Extract tenure
    tenure_match = re.search(r'(\d+)\s*(?:years?|yrs?)', query_lower)
    tenure = int(tenure_match.group(1)) if tenure_match else None
    
    # Determine query type
    query_type = "general"
    if any(word in query_lower for word in ["save", "saving", "budget"]):
        query_type = "savings"
    elif any(word in query_lower for word in ["invest", "investment", "stock", "mutual fund"]):
        query_type = "investment"
    elif any(word in query_lower for word in ["tax", "80c", "80d", "deduction"]):
        query_type = "tax"
    elif any(word in query_lower for word in ["emi", "loan", "debt"]):
        query_type = "loan"
    
    return {
        "salary": salary,
        "emi": emi,
        "loan_amount": loan_amount,
        "interest_rate": interest_rate,
        "tenure": tenure,
        "query_type": query_type,
        "original_query": query
    }


def calculate_debt_to_income_ratio(monthly_income: float, monthly_debt: float) -> float:
    """Calculate debt-to-income ratio"""
    if monthly_income <= 0:
        return 0
    return (monthly_debt / monthly_income) * 100


def calculate_savings_rate(income: float, expenses: float) -> float:
    """Calculate savings rate percentage"""
    if income <= 0:
        return 0
    return ((income - expenses) / income) * 100


def format_percentage(value: float) -> str:
    """Format percentage with proper sign"""
    if value >= 0:
        return f"+{value:.2f}%"
    else:
        return f"{value:.2f}%"


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate Indian phone number format"""
    # Remove spaces and special characters
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    # Check for Indian mobile number pattern
    pattern = r'^(\+91|91|0)?[6-9]\d{9}$'
    return re.match(pattern, phone) is not None


def extract_numbers_from_text(text: str) -> List[float]:
    """Extract all numbers from text"""
    numbers = re.findall(r'\d+(?:,\d+)*(?:\.\d+)?', text)
    return [float(num.replace(',', '')) for num in numbers]


def clean_text_for_analysis(text: str) -> str:
    """Clean text for better analysis"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', '', text)
    return text.strip()


def generate_session_id() -> str:
    """Generate unique session ID"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:8]
    return f"session_{timestamp}_{random_suffix}"


def is_business_hours() -> bool:
    """Check if current time is within business hours (9 AM - 6 PM IST)"""
    now = datetime.now()
    # Convert to IST (UTC+5:30)
    ist_time = now + timedelta(hours=5, minutes=30)
    return 9 <= ist_time.hour < 18


def format_timestamp(timestamp: datetime) -> str:
    """Format timestamp for display"""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def calculate_age_from_dob(date_of_birth: str) -> int:
    """Calculate age from date of birth"""
    try:
        dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    except ValueError:
        return 0


def validate_pan_card(pan: str) -> bool:
    """Validate PAN card format"""
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    return re.match(pattern, pan.upper()) is not None


def validate_aadhaar(aadhaar: str) -> bool:
    """Validate Aadhaar number format"""
    # Remove spaces and hyphens
    aadhaar = re.sub(r'[\s\-]', '', aadhaar)
    # Check for 12 digits
    pattern = r'^\d{12}$'
    return re.match(pattern, aadhaar) is not None


def get_risk_profile(age: int, income: float, investment_horizon: str) -> str:
    """Determine risk profile based on age, income, and investment horizon"""
    if age < 30:
        base_risk = "moderate"
    elif age < 50:
        base_risk = "conservative"
    else:
        base_risk = "very_conservative"
    
    # Adjust based on income
    if income > 1000000:  # High income
        if base_risk == "very_conservative":
            base_risk = "conservative"
        elif base_risk == "conservative":
            base_risk = "moderate"
    
    # Adjust based on investment horizon
    if investment_horizon.lower() in ["long", "long_term", "10+ years"]:
        if base_risk == "very_conservative":
            base_risk = "conservative"
        elif base_risk == "conservative":
            base_risk = "moderate"
    
    return base_risk


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def safe_json_dumps(obj: Any) -> str:
    """Safely convert object to JSON string"""
    try:
        return json.dumps(obj, default=str, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error converting object to JSON: {str(e)}")
        return "{}"


def parse_json_safe(json_str: str) -> Optional[Dict[str, Any]]:
    """Safely parse JSON string"""
    try:
        return json.loads(json_str)
    except Exception as e:
        logger.error(f"Error parsing JSON: {str(e)}")
        return None
