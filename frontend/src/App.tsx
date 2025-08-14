import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/Common/Navbar';
import Sidebar from './components/Common/Sidebar';
import Chat from './components/Chat/ChatInterface';
import Dashboard from './components/Dashboard/Dashboard';
import Documents from './components/Documents/DocumentManager';
import MarketData from './components/Dashboard/MarketData';
import Calculators from './components/Dashboard/Calculators';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#22c55e',
                secondary: '#fff',
              },
            },
            error: {
              duration: 5000,
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },
          }}
        />
        
        <Navbar />
        
        <div className="flex">
          <Sidebar />
          
          <main className="flex-1 p-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/chat" element={<Chat />} />
              <Route path="/documents" element={<Documents />} />
              <Route path="/market" element={<MarketData />} />
              <Route path="/calculators" element={<Calculators />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
