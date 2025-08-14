from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
import logging
from app.services.finance_api import FinanceAPIService
from app.models.finance import EMICalculation
from app.models.auth import User
from app.utils.helpers import format_currency, format_percentage
from app.dependencies.auth import get_current_active_user
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/finance", tags=["finance"])

# Initialize service
finance_service = FinanceAPIService()


@router.get("/stocks/{symbol}")
async def get_stock_data(symbol: str):
    """Get stock market data for a given symbol"""
    try:
        if not symbol.strip():
            raise HTTPException(status_code=400, detail="Stock symbol cannot be empty")
        
        stock_data = await finance_service.get_stock_data(symbol.upper())
        
        if not stock_data:
            raise HTTPException(status_code=404, detail=f"Stock data not found for symbol: {symbol}")
        
        return {
            "stock": stock_data,
            "formatted": {
                "current_price": format_currency(stock_data.current_price, "USD"),
                "change": format_currency(stock_data.change, "USD"),
                "change_percent": format_percentage(stock_data.change_percent),
                "volume": f"{stock_data.volume:,}",
                "market_cap": format_currency(stock_data.market_cap, "USD") if stock_data.market_cap else "N/A",
                "pe_ratio": f"{stock_data.pe_ratio:.2f}" if stock_data.pe_ratio else "N/A",
                "dividend_yield": f"{stock_data.dividend_yield:.2f}%" if stock_data.dividend_yield else "N/A"
            },
            "retrieved_at": stock_data.timestamp.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching stock data for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching stock data")


@router.get("/crypto/{coin_id}")
async def get_crypto_data(coin_id: str):
    """Get cryptocurrency data for a given coin"""
    try:
        if not coin_id.strip():
            raise HTTPException(status_code=400, detail="Coin ID cannot be empty")
        
        crypto_data = await finance_service.get_crypto_data(coin_id.lower())
        
        if not crypto_data:
            raise HTTPException(status_code=404, detail=f"Crypto data not found for coin: {coin_id}")
        
        return {
            "crypto": crypto_data,
            "formatted": {
                "current_price": format_currency(crypto_data.current_price, "USD"),
                "change_24h": format_currency(crypto_data.change_24h, "USD"),
                "change_percent_24h": format_percentage(crypto_data.change_percent_24h),
                "market_cap": format_currency(crypto_data.market_cap, "USD"),
                "volume_24h": format_currency(crypto_data.volume_24h, "USD")
            },
            "retrieved_at": crypto_data.timestamp.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching crypto data for {coin_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching crypto data")


@router.get("/rbi-rates")
async def get_rbi_rates():
    """Get RBI interest rates"""
    try:
        rbi_rates = await finance_service.get_rbi_rates()
        
        if not rbi_rates:
            raise HTTPException(status_code=500, detail="Unable to fetch RBI rates")
        
        return {
            "rbi_rates": rbi_rates,
            "formatted": {
                "repo_rate": f"{rbi_rates.repo_rate:.2f}%",
                "reverse_repo_rate": f"{rbi_rates.reverse_repo_rate:.2f}%",
                "bank_rate": f"{rbi_rates.bank_rate:.2f}%",
                "mclr": f"{rbi_rates.mclr:.2f}%",
                "base_rate": f"{rbi_rates.base_rate:.2f}%"
            },
            "effective_date": rbi_rates.effective_date.isoformat(),
            "retrieved_at": rbi_rates.timestamp.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching RBI rates: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching RBI rates")


@router.post("/calculate-emi")
async def calculate_emi(
    principal: float = Query(..., gt=0, description="Loan principal amount"),
    rate: float = Query(..., gt=0, description="Annual interest rate (%)"),
    tenure_years: int = Query(..., gt=0, description="Loan tenure in years")
):
    """Calculate EMI for a loan"""
    try:
        emi_calculation = finance_service.calculate_emi(principal, rate, tenure_years)
        
        return {
            "emi_calculation": emi_calculation,
            "formatted": {
                "principal": format_currency(emi_calculation.principal),
                "rate": f"{emi_calculation.rate:.2f}%",
                "tenure_years": emi_calculation.tenure_years,
                "emi_amount": format_currency(emi_calculation.emi_amount),
                "total_interest": format_currency(emi_calculation.total_interest),
                "total_amount": format_currency(emi_calculation.total_amount)
            },
            "monthly_breakdown": emi_calculation.monthly_breakdown,
            "calculated_at": datetime.now().isoformat()
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error calculating EMI: {str(e)}")
        raise HTTPException(status_code=500, detail="Error calculating EMI")


@router.get("/market-summary")
async def get_market_summary():
    """Get a summary of market data"""
    try:
        market_data = await finance_service.get_market_summary()
        
        return {
            "market_summary": market_data,
            "summary": {
                "total_stocks": len(market_data["stocks"]),
                "total_cryptos": len(market_data["cryptocurrencies"]),
                "rbi_rates_available": market_data["rbi_rates"] is not None
            },
            "retrieved_at": market_data["timestamp"].isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching market summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching market summary")


@router.get("/popular-stocks")
async def get_popular_stocks():
    """Get data for popular stocks"""
    try:
        popular_symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META", "NVDA", "NFLX"]
        
        stocks_data = []
        for symbol in popular_symbols:
            try:
                stock_data = await finance_service.get_stock_data(symbol)
                if stock_data:
                    stocks_data.append({
                        "symbol": stock_data.symbol,
                        "name": stock_data.name,
                        "current_price": stock_data.current_price,
                        "change_percent": stock_data.change_percent,
                        "formatted_price": format_currency(stock_data.current_price, "USD"),
                        "formatted_change": format_percentage(stock_data.change_percent)
                    })
            except Exception as e:
                logger.warning(f"Error fetching data for {symbol}: {str(e)}")
                continue
        
        return {
            "popular_stocks": stocks_data,
            "total_available": len(stocks_data),
            "retrieved_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching popular stocks: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching popular stocks")


@router.get("/popular-cryptos")
async def get_popular_cryptos():
    """Get data for popular cryptocurrencies"""
    try:
        popular_coins = ["bitcoin", "ethereum", "cardano", "solana", "polkadot", "ripple"]
        
        cryptos_data = []
        for coin in popular_coins:
            try:
                crypto_data = await finance_service.get_crypto_data(coin)
                if crypto_data:
                    cryptos_data.append({
                        "symbol": crypto_data.symbol,
                        "name": crypto_data.name,
                        "current_price": crypto_data.current_price,
                        "change_percent_24h": crypto_data.change_percent_24h,
                        "formatted_price": format_currency(crypto_data.current_price, "USD"),
                        "formatted_change": format_percentage(crypto_data.change_percent_24h)
                    })
            except Exception as e:
                logger.warning(f"Error fetching data for {coin}: {str(e)}")
                continue
        
        return {
            "popular_cryptos": cryptos_data,
            "total_available": len(cryptos_data),
            "retrieved_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error fetching popular cryptos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching popular cryptos")


@router.get("/currency-converter")
async def convert_currency(
    amount: float = Query(..., gt=0, description="Amount to convert"),
    from_currency: str = Query(..., description="Source currency (e.g., USD, INR)"),
    to_currency: str = Query(..., description="Target currency (e.g., USD, INR)")
):
    """Convert currency (simplified implementation)"""
    try:
        # This is a simplified implementation
        # In production, you'd use a real currency conversion API
        
        # Mock conversion rates (for demonstration)
        conversion_rates = {
            "USD": {"INR": 83.0, "EUR": 0.92, "GBP": 0.79},
            "INR": {"USD": 0.012, "EUR": 0.011, "GBP": 0.0095},
            "EUR": {"USD": 1.09, "INR": 90.0, "GBP": 0.86},
            "GBP": {"USD": 1.27, "INR": 105.0, "EUR": 1.16}
        }
        
        if from_currency.upper() not in conversion_rates:
            raise HTTPException(status_code=400, detail=f"Unsupported source currency: {from_currency}")
        
        if to_currency.upper() not in conversion_rates[from_currency.upper()]:
            raise HTTPException(status_code=400, detail=f"Unsupported target currency: {to_currency}")
        
        rate = conversion_rates[from_currency.upper()][to_currency.upper()]
        converted_amount = amount * rate
        
        return {
            "conversion": {
                "from_amount": amount,
                "from_currency": from_currency.upper(),
                "to_amount": converted_amount,
                "to_currency": to_currency.upper(),
                "exchange_rate": rate
            },
            "formatted": {
                "from_amount": format_currency(amount, from_currency.upper()),
                "to_amount": format_currency(converted_amount, to_currency.upper()),
                "rate": f"1 {from_currency.upper()} = {rate:.4f} {to_currency.upper()}"
            },
            "converted_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error converting currency: {str(e)}")
        raise HTTPException(status_code=500, detail="Error converting currency")


@router.get("/financial-calculators/sip")
async def calculate_sip(
    monthly_amount: float = Query(..., gt=0, description="Monthly SIP amount"),
    rate: float = Query(..., gt=0, description="Expected annual return (%)"),
    years: int = Query(..., gt=0, description="Investment period in years")
):
    """Calculate SIP returns"""
    try:
        monthly_rate = rate / (12 * 100)
        total_months = years * 12
        
        # SIP formula: FV = P * ((1 + r)^n - 1) / r
        if monthly_rate == 0:
            future_value = monthly_amount * total_months
        else:
            future_value = monthly_amount * ((1 + monthly_rate) ** total_months - 1) / monthly_rate
        
        total_investment = monthly_amount * total_months
        total_returns = future_value - total_investment
        
        return {
            "sip_calculation": {
                "monthly_amount": monthly_amount,
                "rate": rate,
                "years": years,
                "future_value": future_value,
                "total_investment": total_investment,
                "total_returns": total_returns
            },
            "formatted": {
                "monthly_amount": format_currency(monthly_amount),
                "rate": f"{rate:.2f}%",
                "future_value": format_currency(future_value),
                "total_investment": format_currency(total_investment),
                "total_returns": format_currency(total_returns)
            },
            "calculated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error calculating SIP: {str(e)}")
        raise HTTPException(status_code=500, detail="Error calculating SIP")


@router.get("/financial-calculators/compound-interest")
async def calculate_compound_interest(
    principal: float = Query(..., gt=0, description="Principal amount"),
    rate: float = Query(..., gt=0, description="Annual interest rate (%)"),
    years: int = Query(..., gt=0, description="Time period in years"),
    compound_frequency: str = Query("annually", description="Compound frequency (annually, semi-annually, quarterly, monthly)")
):
    """Calculate compound interest"""
    try:
        # Convert compound frequency to number of times per year
        frequency_map = {
            "annually": 1,
            "semi-annually": 2,
            "quarterly": 4,
            "monthly": 12
        }
        
        if compound_frequency.lower() not in frequency_map:
            raise HTTPException(status_code=400, detail="Invalid compound frequency")
        
        n = frequency_map[compound_frequency.lower()]
        r = rate / 100
        
        # Compound interest formula: A = P(1 + r/n)^(nt)
        amount = principal * (1 + r/n) ** (n * years)
        interest_earned = amount - principal
        
        return {
            "compound_interest": {
                "principal": principal,
                "rate": rate,
                "years": years,
                "compound_frequency": compound_frequency,
                "final_amount": amount,
                "interest_earned": interest_earned
            },
            "formatted": {
                "principal": format_currency(principal),
                "rate": f"{rate:.2f}%",
                "final_amount": format_currency(amount),
                "interest_earned": format_currency(interest_earned)
            },
            "calculated_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating compound interest: {str(e)}")
        raise HTTPException(status_code=500, detail="Error calculating compound interest")
