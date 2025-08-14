import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, RefreshCw } from 'lucide-react';
import toast from 'react-hot-toast';
import { getPopularStocks, getPopularCryptos, getRBIRates } from '../../services/api';

const MarketData: React.FC = () => {
  const [stocks, setStocks] = useState<any[]>([]);
  const [cryptos, setCryptos] = useState<any[]>([]);
  const [rbiRates, setRbiRates] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMarketData();
  }, []);

  const fetchMarketData = async () => {
    try {
      setLoading(true);
      const [stocksData, cryptosData, rbiData] = await Promise.all([
        getPopularStocks(),
        getPopularCryptos(),
        getRBIRates(),
      ]);

      setStocks(stocksData.popular_stocks || []);
      setCryptos(cryptosData.popular_cryptos || []);
      setRbiRates(rbiData.rbi_rates || null);
    } catch (error) {
      console.error('Error fetching market data:', error);
      toast.error('Failed to load market data');
    } finally {
      setLoading(false);
    }
  };

  const getChangeColor = (change: number) => {
    return change >= 0 ? 'text-success-600' : 'text-danger-600';
  };

  const getChangeIcon = (change: number) => {
    return change >= 0 ? (
      <TrendingUp className="w-4 h-4 text-success-600" />
    ) : (
      <TrendingDown className="w-4 h-4 text-danger-600" />
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Market Data</h1>
          <p className="text-gray-600">Live financial market information</p>
        </div>
        <button
          onClick={fetchMarketData}
          disabled={loading}
          className="btn-primary flex items-center space-x-2"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          <span>{loading ? 'Refreshing...' : 'Refresh'}</span>
        </button>
      </div>

      {/* Stocks Section */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Popular Stocks</h2>
        {loading ? (
          <div className="space-y-3">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="h-16 bg-gray-200 rounded"></div>
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {stocks.map((stock, index) => (
              <div key={index} className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-2">
                  <div>
                    <h3 className="font-semibold text-gray-900">{stock.symbol}</h3>
                    <p className="text-sm text-gray-500">{stock.name}</p>
                  </div>
                  {getChangeIcon(stock.change_percent)}
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-lg font-bold text-gray-900">{stock.formatted_price}</span>
                  <span className={`text-sm font-medium ${getChangeColor(stock.change_percent)}`}>
                    {stock.formatted_change}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Cryptocurrencies Section */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Popular Cryptocurrencies</h2>
        {loading ? (
          <div className="space-y-3">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="h-16 bg-gray-200 rounded"></div>
              </div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {cryptos.map((crypto, index) => (
              <div key={index} className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-2">
                  <div>
                    <h3 className="font-semibold text-gray-900">{crypto.symbol}</h3>
                    <p className="text-sm text-gray-500">{crypto.name}</p>
                  </div>
                  {getChangeIcon(crypto.change_percent_24h)}
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-lg font-bold text-gray-900">{crypto.formatted_price}</span>
                  <span className={`text-sm font-medium ${getChangeColor(crypto.change_percent_24h)}`}>
                    {crypto.formatted_change}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* RBI Rates Section */}
      {rbiRates && (
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">RBI Interest Rates</h2>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Repo Rate</p>
              <p className="text-2xl font-bold text-gray-900">{rbiRates.repo_rate}%</p>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Reverse Repo</p>
              <p className="text-2xl font-bold text-gray-900">{rbiRates.reverse_repo_rate}%</p>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Bank Rate</p>
              <p className="text-2xl font-bold text-gray-900">{rbiRates.bank_rate}%</p>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">MCLR</p>
              <p className="text-2xl font-bold text-gray-900">{rbiRates.mclr}%</p>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Base Rate</p>
              <p className="text-2xl font-bold text-gray-900">{rbiRates.base_rate}%</p>
            </div>
          </div>
          <p className="text-sm text-gray-500 mt-4 text-center">
            Last updated: {new Date(rbiRates.effective_date).toLocaleDateString()}
          </p>
        </div>
      )}

      {/* Market Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card text-center">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Total Stocks</h3>
          <p className="text-3xl font-bold text-primary-600">{stocks.length}</p>
          <p className="text-sm text-gray-500">Tracked</p>
        </div>
        <div className="card text-center">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Total Cryptos</h3>
          <p className="text-3xl font-bold text-primary-600">{cryptos.length}</p>
          <p className="text-sm text-gray-500">Tracked</p>
        </div>
        <div className="card text-center">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Market Status</h3>
          <p className="text-3xl font-bold text-success-600">Live</p>
          <p className="text-sm text-gray-500">Real-time data</p>
        </div>
      </div>
    </div>
  );
};

export default MarketData;
