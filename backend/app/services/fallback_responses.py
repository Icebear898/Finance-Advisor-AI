"""
Fallback response system for when AI service is not available
"""

import re
from typing import Dict, List, Optional

class FallbackResponseService:
    """Provides intelligent fallback responses when AI is not available"""
    
    def __init__(self):
        self.financial_advice = {
            "savings": [
                "Start with the 50/30/20 rule: 50% for needs, 30% for wants, 20% for savings.",
                "Set up automatic transfers to a separate savings account.",
                "Track your expenses for a month to identify spending patterns.",
                "Aim to save 3-6 months of expenses as an emergency fund.",
                "Consider high-yield savings accounts for better returns."
            ],
            "budgeting": [
                "Create a monthly budget using apps like Mint or YNAB.",
                "Use the envelope method for discretionary spending.",
                "Review and adjust your budget monthly.",
                "Include savings as a fixed expense in your budget.",
                "Set specific financial goals to stay motivated."
            ],
            "investments": [
                "Start with index funds for broad market exposure.",
                "Consider SIP (Systematic Investment Plan) for regular investing.",
                "Diversify across different asset classes (stocks, bonds, gold).",
                "Invest in tax-saving instruments like ELSS under Section 80C.",
                "Consult a financial advisor for personalized advice."
            ],
            "debt": [
                "Pay off high-interest debt first (credit cards, personal loans).",
                "Consider debt consolidation for multiple loans.",
                "Avoid taking new debt while paying off existing ones.",
                "Use the snowball or avalanche method for debt repayment.",
                "Build an emergency fund to avoid new debt."
            ],
            "tax": [
                "Maximize Section 80C deductions (ELSS, PPF, EPF).",
                "Consider health insurance under Section 80D.",
                "Use HRA and LTA benefits effectively.",
                "File returns on time to avoid penalties.",
                "Keep proper documentation for all deductions."
            ]
        }
        
        self.calculator_info = {
            "emi": "Use our EMI calculator to understand loan payments. Enter principal, interest rate, and tenure.",
            "sip": "Try our SIP calculator to see how regular investments can grow over time.",
            "compound": "Use compound interest calculator to understand long-term investment growth."
        }
    
    def get_fallback_response(self, user_message: str) -> str:
        """Generate a relevant fallback response based on user query"""
        message_lower = user_message.lower()
        
        # Extract income information if mentioned
        income = self._extract_income(user_message)
        
        # Check for specific topics
        if any(word in message_lower for word in ["save", "saving", "savings"]):
            return self._get_savings_advice(income)
        elif any(word in message_lower for word in ["budget", "budgeting", "spend", "expense"]):
            return self._get_budgeting_advice(income)
        elif any(word in message_lower for word in ["invest", "investment", "stock", "mutual fund"]):
            return self._get_investment_advice(income)
        elif any(word in message_lower for word in ["debt", "loan", "emi", "credit"]):
            return self._get_debt_advice(income)
        elif any(word in message_lower for word in ["tax", "deduction", "80c", "80d"]):
            return self._get_tax_advice(income)
        elif any(word in message_lower for word in ["calculator", "calculate", "emi", "sip"]):
            return self._get_calculator_info(message_lower)
        else:
            return self._get_general_advice(income)
    
    def _extract_income(self, message: str) -> Optional[float]:
        """Extract income amount from message"""
        import re
        
        # Look for income patterns
        patterns = [
            r'rs\.?\s*(\d+(?:,\d+)*)\s*k',  # Rs 30K, Rs. 30,000
            r'₹\s*(\d+(?:,\d+)*)\s*k',      # ₹30K
            r'inr\s*(\d+(?:,\d+)*)\s*k',    # INR 30K
            r'(\d+(?:,\d+)*)\s*k\s*per\s*month',  # 30K per month
            r'(\d+(?:,\d+)*)\s*thousand',   # 30 thousand
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                return float(amount_str) * 1000  # Convert K to actual amount
        
        return None
    
    def _get_savings_advice(self) -> str:
        """Get savings-related advice"""
        import random
        advice = random.choice(self.financial_advice["savings"])
        return f"💡 **Savings Tip**: {advice}\n\n💰 **Quick Actions**:\n• Use our EMI calculator to see how reducing debt can free up money for savings\n• Check our market data for investment opportunities\n• Try our compound interest calculator to see how your savings can grow"
    
    def _get_budgeting_advice(self, income: Optional[float] = None) -> str:
        """Get budgeting-related advice"""
        import random
        
        if income:
            # Calculate personalized budget breakdown
            needs = income * 0.5  # 50% for needs
            wants = income * 0.3  # 30% for wants
            savings = income * 0.2  # 20% for savings
            
            return f"""📊 **Personalized Budget for ₹{income:,.0f}/month**:

💰 **50/30/20 Rule Breakdown**:
• **Needs (50%)**: ₹{needs:,.0f} - Rent, utilities, groceries, transport
• **Wants (30%)**: ₹{wants:,.0f} - Entertainment, dining, shopping
• **Savings (20%)**: ₹{savings:,.0f} - Emergency fund, investments

📋 **Recommended Allocation**:
• Rent/EMI: ₹{needs * 0.4:,.0f} (40% of needs)
• Utilities & Groceries: ₹{needs * 0.3:,.0f} (30% of needs)
• Transport: ₹{needs * 0.2:,.0f} (20% of needs)
• Insurance: ₹{needs * 0.1:,.0f} (10% of needs)

💡 **Smart Tips**:
• Start with ₹{savings * 0.5:,.0f} in emergency fund
• Invest ₹{savings * 0.3:,.0f} in SIP/mutual funds
• Keep ₹{savings * 0.2:,.0f} for short-term goals

🧮 **Use our EMI calculator** to see how reducing debt can free up more money for savings!"""
        else:
            advice = random.choice(self.financial_advice["budgeting"])
            return f"📊 **Budgeting Tip**: {advice}\n\n📈 **Tools Available**:\n• Use our financial calculators to plan your budget\n• Check market data for investment planning\n• Upload documents for expense analysis"
    
    def _get_investment_advice(self) -> str:
        """Get investment-related advice"""
        import random
        advice = random.choice(self.financial_advice["investments"])
        return f"📈 **Investment Tip**: {advice}\n\n🔍 **Available Tools**:\n• Check live market data for current prices\n• Use our SIP calculator for investment planning\n• Try compound interest calculator for long-term planning"
    
    def _get_debt_advice(self) -> str:
        """Get debt-related advice"""
        import random
        advice = random.choice(self.financial_advice["debt"])
        return f"💳 **Debt Management Tip**: {advice}\n\n🧮 **Calculators Available**:\n• Use our EMI calculator to understand loan payments\n• Calculate debt-to-income ratio\n• Plan debt repayment strategy"
    
    def _get_tax_advice(self) -> str:
        """Get tax-related advice"""
        import random
        advice = random.choice(self.financial_advice["tax"])
        return f"📋 **Tax Planning Tip**: {advice}\n\n📊 **Resources**:\n• Check current RBI rates for loan planning\n• Use calculators for tax-saving investments\n• Upload documents for tax analysis"
    
    def _get_calculator_info(self, message: str) -> str:
        """Get calculator-specific information"""
        if "emi" in message:
            return f"🏦 **EMI Calculator**: {self.calculator_info['emi']}\n\n💡 **Pro Tip**: Lower interest rates and longer tenures reduce EMI but increase total interest paid."
        elif "sip" in message:
            return f"📈 **SIP Calculator**: {self.calculator_info['sip']}\n\n💡 **Pro Tip**: Start early and stay consistent for maximum benefits of compounding."
        elif "compound" in message:
            return f"📊 **Compound Interest Calculator**: {self.calculator_info['compound']}\n\n💡 **Pro Tip**: Time is your biggest ally in compound interest - start investing early!"
        else:
            return "🧮 **Financial Calculators Available**:\n• EMI Calculator - for loan planning\n• SIP Calculator - for regular investments\n• Compound Interest Calculator - for long-term growth\n\nTry any of these tools for detailed calculations!"
    
    def _get_general_advice(self) -> str:
        """Get general financial advice"""
        return """💡 **Financial Wellness Tips**:

1. **Emergency Fund**: Save 3-6 months of expenses
2. **Budget**: Use the 50/30/20 rule
3. **Invest**: Start with index funds and SIP
4. **Insurance**: Get adequate health and life coverage
5. **Tax Planning**: Maximize deductions under 80C and 80D

🛠️ **Available Tools**:
• Financial Calculators (EMI, SIP, Compound Interest)
• Live Market Data (Stocks, Crypto, RBI Rates)
• Document Analysis (Upload financial documents)

📚 **Learn More**: Check our market data and use calculators for personalized planning!"""

# Global instance
fallback_service = FallbackResponseService()
