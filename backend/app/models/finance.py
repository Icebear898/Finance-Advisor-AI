from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class InvestmentType(str, Enum):
    STOCKS = "stocks"
    MUTUAL_FUNDS = "mutual_funds"
    GOLD = "gold"
    FIXED_DEPOSITS = "fixed_deposits"
    PPF = "ppf"
    ELSS = "elss"


class StockData(BaseModel):
    symbol: str
    name: str
    current_price: float
    change: float
    change_percent: float
    volume: int
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class CryptoData(BaseModel):
    symbol: str
    name: str
    current_price: float
    change_24h: float
    change_percent_24h: float
    market_cap: float
    volume_24h: float
    timestamp: datetime = Field(default_factory=datetime.now)


class RBIRates(BaseModel):
    repo_rate: float
    reverse_repo_rate: float
    bank_rate: float
    mclr: float
    base_rate: float
    effective_date: datetime
    timestamp: datetime = Field(default_factory=datetime.now)


class EMICalculation(BaseModel):
    principal: float = Field(..., gt=0)
    rate: float = Field(..., gt=0)
    tenure_years: int = Field(..., gt=0)
    emi_amount: float
    total_interest: float
    total_amount: float
    monthly_breakdown: List[Dict[str, float]]


class InvestmentSuggestion(BaseModel):
    type: InvestmentType
    name: str
    description: str
    expected_return: float
    risk_level: str
    investment_horizon: str
    minimum_amount: float
    tax_benefits: Optional[str] = None
    pros: List[str]
    cons: List[str]


class TaxSavingOption(BaseModel):
    section: str
    name: str
    description: str
    maximum_deduction: float
    lock_in_period: str
    expected_return: float
    risk_level: str
    eligibility: str


class FinancialAdvice(BaseModel):
    category: str
    advice: str
    reasoning: str
    actionable_steps: List[str]
    expected_impact: str
    timeline: str
