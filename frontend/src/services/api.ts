import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Chat API
export const sendChatMessage = async (data: {
  message: string;
  document_ids?: string[];
}) => {
  const response = await api.post('/api/chat/', data);
  return response.data;
};

export const getChatHistory = async (sessionId: string) => {
  const response = await api.get(`/api/chat/history/${sessionId}`);
  return response.data;
};

export const clearChatHistory = async (sessionId: string) => {
  const response = await api.delete(`/api/chat/history/${sessionId}`);
  return response.data;
};

// Documents API
export const uploadDocument = async (file: File, description?: string) => {
  const formData = new FormData();
  formData.append('file', file);
  if (description) {
    formData.append('description', description);
  }
  
  const response = await api.post('/api/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getDocuments = async () => {
  const response = await api.get('/api/documents/list');
  return response.data;
};

export const deleteDocument = async (documentId: string) => {
  const response = await api.delete(`/api/documents/${documentId}`);
  return response.data;
};

export const searchDocuments = async (query: string, maxResults: number = 5) => {
  const response = await api.post('/api/documents/search', { query, max_results: maxResults });
  return response.data;
};

// Finance API
export const getStockData = async (symbol: string) => {
  const response = await api.get(`/api/finance/stocks/${symbol}`);
  return response.data;
};

export const getCryptoData = async (coinId: string) => {
  const response = await api.get(`/api/finance/crypto/${coinId}`);
  return response.data;
};

export const getRBIRates = async () => {
  const response = await api.get('/api/finance/rbi-rates');
  return response.data;
};

export const calculateEMI = async (principal: number, rate: number, tenureYears: number) => {
  const response = await api.post('/api/finance/calculate-emi', {
    principal,
    rate,
    tenure_years: tenureYears,
  });
  return response.data;
};

export const getMarketSummary = async () => {
  const response = await api.get('/api/finance/market-summary');
  return response.data;
};

export const getPopularStocks = async () => {
  const response = await api.get('/api/finance/popular-stocks');
  return response.data;
};

export const getPopularCryptos = async () => {
  const response = await api.get('/api/finance/popular-cryptos');
  return response.data;
};

export const convertCurrency = async (
  amount: number,
  fromCurrency: string,
  toCurrency: string
) => {
  const response = await api.get('/api/finance/currency-converter', {
    params: {
      amount,
      from_currency: fromCurrency,
      to_currency: toCurrency,
    },
  });
  return response.data;
};

export const calculateSIP = async (
  monthlyAmount: number,
  rate: number,
  years: number
) => {
  const response = await api.get('/api/finance/financial-calculators/sip', {
    params: {
      monthly_amount: monthlyAmount,
      rate,
      years,
    },
  });
  return response.data;
};

export const calculateCompoundInterest = async (
  principal: number,
  rate: number,
  years: number,
  compoundFrequency: string = 'annually'
) => {
  const response = await api.get('/api/finance/financial-calculators/compound-interest', {
    params: {
      principal,
      rate,
      years,
      compound_frequency: compoundFrequency,
    },
  });
  return response.data;
};

// Investment Advice API
export const getInvestmentAdvice = async (userProfile: any) => {
  const response = await api.post('/api/chat/investment-advice', userProfile);
  return response.data;
};

export const getTaxPlanningAdvice = async (income: number, currentDeductions: any) => {
  const response = await api.post('/api/chat/tax-planning', {
    income,
    current_deductions: currentDeductions,
  });
  return response.data;
};

export const analyzeDocument = async (documentContent: string, documentType: string) => {
  const response = await api.post('/api/chat/document-analysis', {
    document_content: documentContent,
    document_type: documentType,
  });
  return response.data;
};

// Health check
export const checkApiHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};

export const getApiStatus = async () => {
  const response = await api.get('/api/status');
  return response.data;
};

export default api;
