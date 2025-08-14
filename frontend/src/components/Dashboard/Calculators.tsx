import React, { useState } from 'react';
import { Calculator, DollarSign, TrendingUp, Percent } from 'lucide-react';
import toast from 'react-hot-toast';
import { calculateEMI, calculateSIP, calculateCompoundInterest } from '../../services/api';

const Calculators: React.FC = () => {
  const [activeCalculator, setActiveCalculator] = useState<'emi' | 'sip' | 'compound'>('emi');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);

  // EMI Calculator
  const [emiData, setEmiData] = useState({
    principal: '',
    rate: '',
    tenure: ''
  });

  // SIP Calculator
  const [sipData, setSipData] = useState({
    monthlyAmount: '',
    rate: '',
    years: ''
  });

  // Compound Interest Calculator
  const [compoundData, setCompoundData] = useState({
    principal: '',
    rate: '',
    years: '',
    frequency: 'annually'
  });

  const handleEMICalculation = async () => {
    if (!emiData.principal || !emiData.rate || !emiData.tenure) {
      toast.error('Please fill all fields');
      return;
    }

    try {
      setLoading(true);
      const response = await calculateEMI(
        parseFloat(emiData.principal),
        parseFloat(emiData.rate),
        parseInt(emiData.tenure)
      );
      setResults(response);
      toast.success('EMI calculated successfully!');
    } catch (error) {
      console.error('Error calculating EMI:', error);
      toast.error('Failed to calculate EMI');
    } finally {
      setLoading(false);
    }
  };

  const handleSIPCalculation = async () => {
    if (!sipData.monthlyAmount || !sipData.rate || !sipData.years) {
      toast.error('Please fill all fields');
      return;
    }

    try {
      setLoading(true);
      const response = await calculateSIP(
        parseFloat(sipData.monthlyAmount),
        parseFloat(sipData.rate),
        parseInt(sipData.years)
      );
      setResults(response);
      toast.success('SIP calculated successfully!');
    } catch (error) {
      console.error('Error calculating SIP:', error);
      toast.error('Failed to calculate SIP');
    } finally {
      setLoading(false);
    }
  };

  const handleCompoundInterestCalculation = async () => {
    if (!compoundData.principal || !compoundData.rate || !compoundData.years) {
      toast.error('Please fill all fields');
      return;
    }

    try {
      setLoading(true);
      const response = await calculateCompoundInterest(
        parseFloat(compoundData.principal),
        parseFloat(compoundData.rate),
        parseInt(compoundData.years),
        compoundData.frequency
      );
      setResults(response);
      toast.success('Compound interest calculated successfully!');
    } catch (error) {
      console.error('Error calculating compound interest:', error);
      toast.error('Failed to calculate compound interest');
    } finally {
      setLoading(false);
    }
  };

  const calculators = [
    {
      id: 'emi',
      title: 'EMI Calculator',
      icon: DollarSign,
      description: 'Calculate loan EMI and interest'
    },
    {
      id: 'sip',
      title: 'SIP Calculator',
      icon: TrendingUp,
      description: 'Calculate SIP returns'
    },
    {
      id: 'compound',
      title: 'Compound Interest',
      icon: Percent,
      description: 'Calculate compound interest'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Financial Calculators</h1>
        <p className="text-gray-600">Calculate EMI, SIP, and compound interest</p>
      </div>

      {/* Calculator Tabs */}
      <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
        {calculators.map((calc) => {
          const Icon = calc.icon;
          return (
            <button
              key={calc.id}
              onClick={() => setActiveCalculator(calc.id as any)}
              className={`flex-1 flex items-center justify-center space-x-2 py-3 px-4 rounded-md text-sm font-medium transition-colors ${
                activeCalculator === calc.id
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{calc.title}</span>
            </button>
          );
        })}
      </div>

      {/* Calculator Forms */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {activeCalculator === 'emi' && 'EMI Calculator'}
            {activeCalculator === 'sip' && 'SIP Calculator'}
            {activeCalculator === 'compound' && 'Compound Interest Calculator'}
          </h3>

          {activeCalculator === 'emi' && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Loan Amount (₹)
                </label>
                <input
                  type="number"
                  value={emiData.principal}
                  onChange={(e) => setEmiData({ ...emiData, principal: e.target.value })}
                  className="input-field"
                  placeholder="Enter loan amount"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Interest Rate (% per annum)
                </label>
                <input
                  type="number"
                  value={emiData.rate}
                  onChange={(e) => setEmiData({ ...emiData, rate: e.target.value })}
                  className="input-field"
                  placeholder="Enter interest rate"
                  step="0.1"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Loan Tenure (Years)
                </label>
                <input
                  type="number"
                  value={emiData.tenure}
                  onChange={(e) => setEmiData({ ...emiData, tenure: e.target.value })}
                  className="input-field"
                  placeholder="Enter loan tenure"
                />
              </div>
              <button
                onClick={handleEMICalculation}
                disabled={loading}
                className="w-full btn-primary"
              >
                {loading ? 'Calculating...' : 'Calculate EMI'}
              </button>
            </div>
          )}

          {activeCalculator === 'sip' && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Monthly Investment (₹)
                </label>
                <input
                  type="number"
                  value={sipData.monthlyAmount}
                  onChange={(e) => setSipData({ ...sipData, monthlyAmount: e.target.value })}
                  className="input-field"
                  placeholder="Enter monthly amount"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Expected Return (% per annum)
                </label>
                <input
                  type="number"
                  value={sipData.rate}
                  onChange={(e) => setSipData({ ...sipData, rate: e.target.value })}
                  className="input-field"
                  placeholder="Enter expected return"
                  step="0.1"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Investment Period (Years)
                </label>
                <input
                  type="number"
                  value={sipData.years}
                  onChange={(e) => setSipData({ ...sipData, years: e.target.value })}
                  className="input-field"
                  placeholder="Enter investment period"
                />
              </div>
              <button
                onClick={handleSIPCalculation}
                disabled={loading}
                className="w-full btn-primary"
              >
                {loading ? 'Calculating...' : 'Calculate SIP'}
              </button>
            </div>
          )}

          {activeCalculator === 'compound' && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Principal Amount (₹)
                </label>
                <input
                  type="number"
                  value={compoundData.principal}
                  onChange={(e) => setCompoundData({ ...compoundData, principal: e.target.value })}
                  className="input-field"
                  placeholder="Enter principal amount"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Interest Rate (% per annum)
                </label>
                <input
                  type="number"
                  value={compoundData.rate}
                  onChange={(e) => setCompoundData({ ...compoundData, rate: e.target.value })}
                  className="input-field"
                  placeholder="Enter interest rate"
                  step="0.1"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Time Period (Years)
                </label>
                <input
                  type="number"
                  value={compoundData.years}
                  onChange={(e) => setCompoundData({ ...compoundData, years: e.target.value })}
                  className="input-field"
                  placeholder="Enter time period"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Compound Frequency
                </label>
                <select
                  value={compoundData.frequency}
                  onChange={(e) => setCompoundData({ ...compoundData, frequency: e.target.value })}
                  className="input-field"
                >
                  <option value="annually">Annually</option>
                  <option value="semi-annually">Semi-annually</option>
                  <option value="quarterly">Quarterly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </div>
              <button
                onClick={handleCompoundInterestCalculation}
                disabled={loading}
                className="w-full btn-primary"
              >
                {loading ? 'Calculating...' : 'Calculate Compound Interest'}
              </button>
            </div>
          )}
        </div>

        {/* Results */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Results</h3>
          {results ? (
            <div className="space-y-4">
              {activeCalculator === 'emi' && results.emi_calculation && (
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                      <p className="text-sm text-gray-600">Monthly EMI</p>
                      <p className="text-xl font-bold text-primary-600">
                        {results.formatted.emi_amount}
                      </p>
                    </div>
                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                      <p className="text-sm text-gray-600">Total Interest</p>
                      <p className="text-xl font-bold text-primary-600">
                        {results.formatted.total_interest}
                      </p>
                    </div>
                  </div>
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600">Total Amount</p>
                    <p className="text-2xl font-bold text-primary-600">
                      {results.formatted.total_amount}
                    </p>
                  </div>
                </div>
              )}

              {activeCalculator === 'sip' && results.sip_calculation && (
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                      <p className="text-sm text-gray-600">Future Value</p>
                      <p className="text-xl font-bold text-primary-600">
                        {results.formatted.future_value}
                      </p>
                    </div>
                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                      <p className="text-sm text-gray-600">Total Investment</p>
                      <p className="text-xl font-bold text-primary-600">
                        {results.formatted.total_investment}
                      </p>
                    </div>
                  </div>
                  <div className="text-center p-3 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600">Total Returns</p>
                    <p className="text-2xl font-bold text-success-600">
                      {results.formatted.total_returns}
                    </p>
                  </div>
                </div>
              )}

              {activeCalculator === 'compound' && results.compound_interest && (
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                      <p className="text-sm text-gray-600">Final Amount</p>
                      <p className="text-xl font-bold text-primary-600">
                        {results.formatted.final_amount}
                      </p>
                    </div>
                    <div className="text-center p-3 bg-gray-50 rounded-lg">
                      <p className="text-sm text-gray-600">Interest Earned</p>
                      <p className="text-xl font-bold text-success-600">
                        {results.formatted.interest_earned}
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-12">
              <Calculator className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">Enter values and calculate to see results</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Calculators;
