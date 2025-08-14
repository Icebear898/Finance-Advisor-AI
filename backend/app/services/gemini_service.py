import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.config import settings
from app.services.fallback_responses import fallback_service
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.google_gemini_api_key)
        
        # Try different model versions in case of compatibility issues
        try:
            self.model = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=settings.google_gemini_api_key,
                temperature=0.7,
                max_output_tokens=2048,
                convert_system_message_to_human=True
            )
        except Exception as e:
            logger.warning(f"Failed to initialize gemini-1.5-pro, trying gemini-pro: {str(e)}")
            try:
                self.model = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash-lite",
                    google_api_key=settings.google_gemini_api_key,
                    temperature=0.7,
                    max_output_tokens=2048,
                    convert_system_message_to_human=True
                )
            except Exception as e2:
                logger.error(f"Failed to initialize both models: {str(e2)}")
                # Create a fallback model with basic configuration
                self.model = None
        
        # Finance-specific system prompts
        self.finance_system_prompt = """
        You are an expert AI Finance Advisor specializing in Indian financial markets and regulations. 
        Provide accurate, helpful, and personalized financial advice based on the following guidelines:
        
        1. **Personal Finance**: Help with budgeting, savings, debt management, and financial planning
        2. **Investment Advice**: Provide insights on stocks, mutual funds, gold, and other investment options
        3. **Tax Planning**: Guide on Indian tax laws, Sections 80C, 80D, and tax-saving investments
        4. **Market Analysis**: Analyze market trends and provide investment recommendations
        5. **Risk Assessment**: Always consider risk factors and provide balanced advice
        
        Important Guidelines:
        - Always mention that you're providing general advice and recommend consulting a financial advisor
        - Include specific Indian context and regulations when relevant
        - Provide actionable steps and clear explanations
        - Consider the user's financial situation and goals
        - Be conservative in recommendations and highlight risks
        """
        
        self.document_analysis_prompt = """
        You are an expert financial document analyst. Analyze the provided financial documents and extract key insights:
        
        1. **Bank Statements**: Identify spending patterns, income sources, and financial health indicators
        2. **Portfolio Reports**: Analyze asset allocation, performance, and risk metrics
        3. **EMI Lists**: Calculate debt-to-income ratios and repayment capacity
        4. **Investment Reports**: Extract key metrics, returns, and recommendations
        
        Provide structured analysis with:
        - Key findings and insights
        - Financial health indicators
        - Recommendations for improvement
        - Risk factors to consider
        """

    async def generate_response(
        self, 
        user_message: str, 
        context: Optional[Dict[str, Any]] = None,
        document_content: Optional[str] = None
    ) -> str:
        """Generate AI response for user query"""
        try:
            # Check if model is initialized
            if self.model is None:
                return "I apologize, but the AI service is not properly configured. Please check your API key and try again."
            
            # Prepare messages
            messages = []
            
            # Add system prompt based on context
            if document_content:
                system_prompt = self.document_analysis_prompt
                messages.append(SystemMessage(content=system_prompt))
                messages.append(HumanMessage(content=f"Document Content:\n{document_content}\n\nUser Query: {user_message}"))
            else:
                system_prompt = self.finance_system_prompt
                if context:
                    system_prompt += f"\n\nContext: {context}"
                messages.append(SystemMessage(content=system_prompt))
                messages.append(HumanMessage(content=user_message))
            
            # Generate response
            response = await self.model.agenerate([messages])
            return response.generations[0][0].text
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error generating response: {error_msg}")
            
            # Check for specific error types
            if "quota" in error_msg.lower() or "429" in error_msg or "rate limit" in error_msg.lower():
                return fallback_service.get_fallback_response(user_message)
            elif "api key" in error_msg.lower() or "authentication" in error_msg.lower():
                return "I apologize, but there's an issue with the AI service configuration. Please check your API key settings."
            else:
                return fallback_service.get_fallback_response(user_message)

    async def generate_investment_advice(
        self, 
        user_profile: Dict[str, Any], 
        investment_goal: str
    ) -> str:
        """Generate personalized investment advice"""
        try:
            prompt = f"""
            Based on the following user profile and investment goal, provide personalized investment advice:
            
            User Profile:
            - Age: {user_profile.get('age', 'Not specified')}
            - Income: {user_profile.get('income', 'Not specified')}
            - Risk Tolerance: {user_profile.get('risk_tolerance', 'Not specified')}
            - Investment Horizon: {user_profile.get('investment_horizon', 'Not specified')}
            - Current Investments: {user_profile.get('current_investments', 'None')}
            
            Investment Goal: {investment_goal}
            
            Please provide:
            1. Recommended asset allocation
            2. Specific investment options
            3. Risk considerations
            4. Expected returns
            5. Actionable steps
            """
            
            messages = [
                SystemMessage(content=self.finance_system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = await self.model.agenerate([messages])
            return response.generations[0][0].text
            
        except Exception as e:
            logger.error(f"Error generating investment advice: {str(e)}")
            return "I apologize, but I'm having trouble generating investment advice right now. Please try again later."

    async def analyze_financial_document(
        self, 
        document_content: str, 
        document_type: str
    ) -> str:
        """Analyze financial documents and provide insights"""
        try:
            prompt = f"""
            Analyze the following {document_type} and provide comprehensive financial insights:
            
            Document Type: {document_type}
            Document Content:
            {document_content}
            
            Please provide:
            1. Key financial metrics and indicators
            2. Spending patterns and trends
            3. Financial health assessment
            4. Areas for improvement
            5. Recommendations
            6. Risk factors to consider
            """
            
            messages = [
                SystemMessage(content=self.document_analysis_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = await self.model.agenerate([messages])
            return response.generations[0][0].text
            
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            return "I apologize, but I'm having trouble analyzing the document right now. Please try again later."

    async def generate_tax_planning_advice(
        self, 
        income: float, 
        current_deductions: Dict[str, float]
    ) -> str:
        """Generate tax planning advice for Indian tax laws"""
        try:
            prompt = f"""
            Provide comprehensive tax planning advice for the following scenario:
            
            Annual Income: ₹{income:,.2f}
            Current Deductions:
            {chr(10).join([f"- {section}: ₹{amount:,.2f}" for section, amount in current_deductions.items()])}
            
            Please provide:
            1. Available tax-saving options under different sections
            2. Recommended investments for maximum tax savings
            3. Lock-in periods and returns
            4. Risk considerations
            5. Action plan for the financial year
            """
            
            messages = [
                SystemMessage(content=self.finance_system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = await self.model.agenerate([messages])
            return response.generations[0][0].text
            
        except Exception as e:
            logger.error(f"Error generating tax advice: {str(e)}")
            return "I apologize, but I'm having trouble generating tax planning advice right now. Please try again later."
