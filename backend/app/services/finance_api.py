import httpx
import aiohttp
import asyncio
from typing import Dict, Any, Optional, List
from app.config import settings
from app.models.finance import StockData, CryptoData, RBIRates, EMICalculation
import logging
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class FinanceAPIService:
    def __init__(self):
        self.alpha_vantage_api_key = settings.alpha_vantage_api_key
        self.coingecko_api_key = settings.coingecko_api_key
        
        # API endpoints
        self.alpha_vantage_base_url = "https://www.alphavantage.co/query"
        self.coingecko_base_url = "https://api.coingecko.com/api/v3"
        self.rbi_base_url = "https://www.rbi.org.in/Scripts/BS_NSDPDisplay.aspx"
        
        # Cache for API responses
        self.cache = {}
        self.cache_duration = timedelta(minutes=5)

    async def get_stock_data(self, symbol: str) -> Optional[StockData]:
        """Get stock data from Alpha Vantage API"""
        try:
            if not self.alpha_vantage_api_key:
                logger.warning("Alpha Vantage API key not configured")
                return self._get_mock_stock_data(symbol)
            
            # Check cache first
            cache_key = f"stock_{symbol}"
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if datetime.now() - timestamp < self.cache_duration:
                    return cached_data
            
            async with httpx.AsyncClient() as client:
                params = {
                    "function": "GLOBAL_QUOTE",
                    "symbol": symbol,
                    "apikey": self.alpha_vantage_api_key
                }
                
                response = await client.get(self.alpha_vantage_base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if "Global Quote" in data:
                    quote = data["Global Quote"]
                    stock_data = StockData(
                        symbol=symbol,
                        name=symbol,  # Alpha Vantage doesn't provide company name in this endpoint
                        current_price=float(quote.get("05. price", 0)),
                        change=float(quote.get("09. change", 0)),
                        change_percent=float(quote.get("10. change percent", "0%").replace("%", "")),
                        volume=int(quote.get("06. volume", 0)),
                        market_cap=None,  # Not available in this endpoint
                        pe_ratio=None,    # Not available in this endpoint
                        dividend_yield=None  # Not available in this endpoint
                    )
                    
                    # Cache the result
                    self.cache[cache_key] = (stock_data, datetime.now())
                    return stock_data
                else:
                    logger.error(f"No stock data found for symbol: {symbol}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching stock data for {symbol}: {str(e)}")
            return self._get_mock_stock_data(symbol)

    async def get_crypto_data(self, coin_id: str) -> Optional[CryptoData]:
        """Get cryptocurrency data from CoinGecko API"""
        try:
            # Check cache first
            cache_key = f"crypto_{coin_id}"
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if datetime.now() - timestamp < self.cache_duration:
                    return cached_data
            
            async with httpx.AsyncClient() as client:
                url = f"{self.coingecko_base_url}/simple/price"
                params = {
                    "ids": coin_id,
                    "vs_currencies": "usd",
                    "include_24hr_change": "true",
                    "include_market_cap": "true",
                    "include_24hr_vol": "true"
                }
                
                if self.coingecko_api_key:
                    params["x_cg_demo_api_key"] = self.coingecko_api_key
                
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if coin_id in data:
                    coin_data = data[coin_id]
                    crypto_data = CryptoData(
                        symbol=coin_id.upper(),
                        name=coin_id.title(),
                        current_price=coin_data.get("usd", 0),
                        change_24h=coin_data.get("usd_24h_change", 0),
                        change_percent_24h=coin_data.get("usd_24h_change", 0),
                        market_cap=coin_data.get("usd_market_cap", 0),
                        volume_24h=coin_data.get("usd_24h_vol", 0)
                    )
                    
                    # Cache the result
                    self.cache[cache_key] = (crypto_data, datetime.now())
                    return crypto_data
                else:
                    logger.error(f"No crypto data found for coin: {coin_id}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching crypto data for {coin_id}: {str(e)}")
            return self._get_mock_crypto_data(coin_id)

    async def get_rbi_rates(self) -> Optional[RBIRates]:
        """Get RBI interest rates (mock data for now)"""
        try:
            # Check cache first
            cache_key = "rbi_rates"
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if datetime.now() - timestamp < self.cache_duration:
                    return cached_data
            
            # For now, return mock data since RBI doesn't have a public API
            rbi_rates = RBIRates(
                repo_rate=6.50,
                reverse_repo_rate=3.35,
                bank_rate=6.75,
                mclr=8.50,
                base_rate=8.25,
                effective_date=datetime.now(),
                timestamp=datetime.now()
            )
            
            # Cache the result
            self.cache[cache_key] = (rbi_rates, datetime.now())
            return rbi_rates
            
        except Exception as e:
            logger.error(f"Error fetching RBI rates: {str(e)}")
            return None

    def calculate_emi(
        self, 
        principal: float, 
        rate: float, 
        tenure_years: int
    ) -> EMICalculation:
        """Calculate EMI for a loan"""
        try:
            # Convert annual rate to monthly rate
            monthly_rate = rate / (12 * 100)
            total_months = tenure_years * 12
            
            # Calculate EMI using formula: EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
            if monthly_rate == 0:
                emi_amount = principal / total_months
            else:
                emi_amount = principal * monthly_rate * (1 + monthly_rate) ** total_months
                emi_amount = emi_amount / ((1 + monthly_rate) ** total_months - 1)
            
            total_amount = emi_amount * total_months
            total_interest = total_amount - principal
            
            # Generate monthly breakdown
            monthly_breakdown = []
            remaining_principal = principal
            
            for month in range(1, min(total_months + 1, 13)):  # Show first 12 months
                interest_payment = remaining_principal * monthly_rate
                principal_payment = emi_amount - interest_payment
                remaining_principal -= principal_payment
                
                monthly_breakdown.append({
                    "month": month,
                    "emi": round(emi_amount, 2),
                    "principal": round(principal_payment, 2),
                    "interest": round(interest_payment, 2),
                    "remaining_principal": round(max(0, remaining_principal), 2)
                })
            
            return EMICalculation(
                principal=principal,
                rate=rate,
                tenure_years=tenure_years,
                emi_amount=round(emi_amount, 2),
                total_interest=round(total_interest, 2),
                total_amount=round(total_amount, 2),
                monthly_breakdown=monthly_breakdown
            )
            
        except Exception as e:
            logger.error(f"Error calculating EMI: {str(e)}")
            raise ValueError("Invalid parameters for EMI calculation")

    def _get_mock_stock_data(self, symbol: str) -> StockData:
        """Get mock stock data for testing"""
        return StockData(
            symbol=symbol,
            name=f"{symbol} Corporation",
            current_price=1500.0,
            change=25.5,
            change_percent=1.73,
            volume=1000000,
            market_cap=15000000000.0,
            pe_ratio=15.5,
            dividend_yield=2.5
        )

    def _get_mock_crypto_data(self, coin_id: str) -> CryptoData:
        """Get mock crypto data for testing"""
        return CryptoData(
            symbol=coin_id.upper(),
            name=coin_id.title(),
            current_price=45000.0,
            change_24h=1250.0,
            change_percent_24h=2.85,
            market_cap=850000000000.0,
            volume_24h=25000000000.0
        )

    async def get_market_summary(self) -> Dict[str, Any]:
        """Get a summary of market data"""
        try:
            # Get data for popular stocks and cryptos
            stocks = ["AAPL", "GOOGL", "MSFT", "TSLA"]
            cryptos = ["bitcoin", "ethereum", "cardano"]
            
            stock_data = []
            crypto_data = []
            
            # Fetch stock data
            for symbol in stocks:
                data = await self.get_stock_data(symbol)
                if data:
                    stock_data.append(data)
            
            # Fetch crypto data
            for coin in cryptos:
                data = await self.get_crypto_data(coin)
                if data:
                    crypto_data.append(data)
            
            # Get RBI rates
            rbi_rates = await self.get_rbi_rates()
            
            return {
                "stocks": stock_data,
                "cryptocurrencies": crypto_data,
                "rbi_rates": rbi_rates,
                "timestamp": datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error fetching market summary: {str(e)}")
            return {
                "stocks": [],
                "cryptocurrencies": [],
                "rbi_rates": None,
                "timestamp": datetime.now()
            }

    def clear_cache(self):
        """Clear the API cache"""
        self.cache.clear()
        logger.info("API cache cleared")
