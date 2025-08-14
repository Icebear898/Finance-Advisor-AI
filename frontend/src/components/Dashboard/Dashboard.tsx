import React, { useState, useEffect } from 'react';
import { TrendingUp, DollarSign, PieChart, Activity, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import toast from 'react-hot-toast';
import { getMarketSummary, getPopularStocks, getPopularCryptos } from '../../services/api';

interface MarketData {
  stocks: any[];
  cryptocurrencies: any[];
  rbi_rates: any;
}

const Dashboard: React.FC = () => {
  const [marketData, setMarketData] = useState<MarketData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMarketData();
  }, []);

  const fetchMarketData = async () => {
    try {
      setLoading(true);
      const [summary, stocks, cryptos] = await Promise.all([
        getMarketSummary(),
        getPopularStocks(),
        getPopularCryptos(),
      ]);

      setMarketData({
        stocks: stocks.popular_stocks || [],
        cryptocurrencies: cryptos.popular_cryptos || [],
        rbi_rates: summary.market_summary?.rbi_rates || null,
      });
    } catch (error) {
      console.error('Error fetching market data:', error);
      toast.error('Failed to load market data');
    } finally {
      setLoading(false);
    }
  };

  const stats = [
    {
      title: 'Total Portfolio Value',
      value: '₹2,45,000',
      change: '+12.5%',
      changeType: 'positive',
      icon: DollarSign,
    },
    {
      title: 'Monthly Returns',
      value: '₹18,500',
      change: '+8.2%',
      changeType: 'positive',
      icon: TrendingUp,
    },
    {
      title: 'Risk Score',
      value: 'Medium',
      change: '-2.1%',
      changeType: 'negative',
      icon: Activity,
    },
    {
      title: 'Asset Allocation',
      value: 'Balanced',
      change: 'Stable',
      changeType: 'neutral',
      icon: PieChart,
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Welcome back! Here's your financial overview.</p>
        </div>
        <button
          onClick={fetchMarketData}
          disabled={loading}
          className="btn-primary"
        >
          {loading ? 'Refreshing...' : 'Refresh Data'}
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
                <div className="flex items-center justify-center w-12 h-12 bg-primary-100 rounded-lg">
                  <Icon className="w-6 h-6 text-primary-600" />
                </div>
              </div>
              <div className="mt-4 flex items-center">
                {stat.changeType === 'positive' ? (
                  <ArrowUpRight className="w-4 h-4 text-success-600" />
                ) : stat.changeType === 'negative' ? (
                  <ArrowDownRight className="w-4 h-4 text-danger-600" />
                ) : null}
                <span
                  className={`text-sm font-medium ml-1 ${
                    stat.changeType === 'positive'
                      ? 'text-success-600'
                      : stat.changeType === 'negative'
                      ? 'text-danger-600'
                      : 'text-gray-600'
                  }`}
                >
                  {stat.change}
                </span>
                <span className="text-sm text-gray-500 ml-1">from last month</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Market Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Popular Stocks */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Popular Stocks</h3>
            <button className="text-sm text-primary-600 hover:text-primary-700">
              View All
            </button>
          </div>
          {loading ? (
            <div className="space-y-3">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="animate-pulse">
                  <div className="h-12 bg-gray-200 rounded"></div>
                </div>
              ))}
            </div>
          ) : (
            <div className="space-y-3">
              {marketData?.stocks.slice(0, 5).map((stock, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900">{stock.symbol}</p>
                    <p className="text-sm text-gray-500">{stock.name}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-gray-900">{stock.formatted_price}</p>
                    <p className={`text-sm ${
                      stock.change_percent > 0 ? 'text-success-600' : 'text-danger-600'
                    }`}>
                      {stock.formatted_change}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Popular Cryptocurrencies */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Popular Cryptocurrencies</h3>
            <button className="text-sm text-primary-600 hover:text-primary-700">
              View All
            </button>
          </div>
          {loading ? (
            <div className="space-y-3">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="animate-pulse">
                  <div className="h-12 bg-gray-200 rounded"></div>
                </div>
              ))}
            </div>
          ) : (
            <div className="space-y-3">
              {marketData?.cryptocurrencies.slice(0, 5).map((crypto, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900">{crypto.symbol}</p>
                    <p className="text-sm text-gray-500">{crypto.name}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-gray-900">{crypto.formatted_price}</p>
                    <p className={`text-sm ${
                      crypto.change_percent_24h > 0 ? 'text-success-600' : 'text-danger-600'
                    }`}>
                      {crypto.formatted_change}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* RBI Rates */}
      {marketData?.rbi_rates && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">RBI Interest Rates</h3>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">Repo Rate</p>
              <p className="text-lg font-semibold text-gray-900">
                {marketData.rbi_rates.repo_rate}%
              </p>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">Reverse Repo</p>
              <p className="text-lg font-semibold text-gray-900">
                {marketData.rbi_rates.reverse_repo_rate}%
              </p>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">Bank Rate</p>
              <p className="text-lg font-semibold text-gray-900">
                {marketData.rbi_rates.bank_rate}%
              </p>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">MCLR</p>
              <p className="text-lg font-semibold text-gray-900">
                {marketData.rbi_rates.mclr}%
              </p>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">Base Rate</p>
              <p className="text-lg font-semibold text-gray-900">
                {marketData.rbi_rates.base_rate}%
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="p-4 text-left border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors">
            <div className="flex items-center mb-2">
              <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center mr-3">
                <TrendingUp className="w-4 h-4 text-primary-600" />
              </div>
              <h4 className="font-medium text-gray-900">Get Investment Advice</h4>
            </div>
            <p className="text-sm text-gray-600">Get personalized investment recommendations</p>
          </button>
          
          <button className="p-4 text-left border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors">
            <div className="flex items-center mb-2">
              <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center mr-3">
                <DollarSign className="w-4 h-4 text-primary-600" />
              </div>
              <h4 className="font-medium text-gray-900">Calculate EMI</h4>
            </div>
            <p className="text-sm text-gray-600">Calculate loan EMI and interest</p>
          </button>
          
          <button className="p-4 text-left border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors">
            <div className="flex items-center mb-2">
              <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center mr-3">
                <PieChart className="w-4 h-4 text-primary-600" />
              </div>
              <h4 className="font-medium text-gray-900">Tax Planning</h4>
            </div>
            <p className="text-sm text-gray-600">Optimize your tax savings</p>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
