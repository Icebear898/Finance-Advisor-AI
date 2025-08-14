import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, 
  MessageSquare, 
  FileText, 
  TrendingUp, 
  Calculator,
  BarChart3,
  Settings,
  HelpCircle
} from 'lucide-react';

const Sidebar: React.FC = () => {
  const location = useLocation();

  const menuItems = [
    {
      path: '/',
      icon: Home,
      label: 'Dashboard',
      description: 'Overview & Analytics'
    },
    {
      path: '/chat',
      icon: MessageSquare,
      label: 'AI Chat',
      description: 'Ask Financial Questions'
    },
    {
      path: '/documents',
      icon: FileText,
      label: 'Documents',
      description: 'Upload & Analyze Files'
    },
    {
      path: '/market',
      icon: TrendingUp,
      label: 'Market Data',
      description: 'Live Market Updates'
    },
    {
      path: '/calculators',
      icon: Calculator,
      label: 'Calculators',
      description: 'Financial Tools'
    }
  ];

  const isActive = (path: string) => {
    if (path === '/' && location.pathname === '/') return true;
    if (path !== '/' && location.pathname.startsWith(path)) return true;
    return false;
  };

  return (
    <aside className="w-64 bg-white shadow-sm border-r border-gray-200 min-h-screen">
      <div className="p-6">
        {/* Quick Actions */}
        <div className="mb-8">
          <h3 className="text-sm font-semibold text-gray-900 mb-3">Quick Actions</h3>
          <div className="space-y-2">
            <button className="w-full btn-primary text-sm">
              Ask AI Advisor
            </button>
            <button className="w-full btn-secondary text-sm">
              Upload Document
            </button>
          </div>
        </div>

        {/* Main Navigation */}
        <nav className="space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.path);
            
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  active
                    ? 'bg-primary-100 text-primary-700 border-r-2 border-primary-600'
                    : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                }`}
              >
                <Icon className={`w-5 h-5 mr-3 ${active ? 'text-primary-600' : 'text-gray-400'}`} />
                <div className="flex-1">
                  <div className="font-medium">{item.label}</div>
                  <div className="text-xs text-gray-500">{item.description}</div>
                </div>
              </Link>
            );
          })}
        </nav>

        {/* Bottom Section */}
        <div className="mt-8 pt-6 border-t border-gray-200">
          <div className="space-y-1">
            <button className="flex items-center w-full px-3 py-2 text-sm font-medium text-gray-600 rounded-lg hover:bg-gray-100 hover:text-gray-900 transition-colors">
              <BarChart3 className="w-5 h-5 mr-3 text-gray-400" />
              Analytics
            </button>
            <button className="flex items-center w-full px-3 py-2 text-sm font-medium text-gray-600 rounded-lg hover:bg-gray-100 hover:text-gray-900 transition-colors">
              <Settings className="w-5 h-5 mr-3 text-gray-400" />
              Settings
            </button>
            <button className="flex items-center w-full px-3 py-2 text-sm font-medium text-gray-600 rounded-lg hover:bg-gray-100 hover:text-gray-900 transition-colors">
              <HelpCircle className="w-5 h-5 mr-3 text-gray-400" />
              Help & Support
            </button>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
