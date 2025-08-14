import React, { useState } from 'react';
import Login from './Login';
import Register from './Register';
import ForgotPassword from './ForgotPassword';

type AuthMode = 'login' | 'register' | 'forgot-password';

const AuthWrapper: React.FC = () => {
  const [authMode, setAuthMode] = useState<AuthMode>('login');

  const switchToLogin = () => setAuthMode('login');
  const switchToRegister = () => setAuthMode('register');
  const switchToForgotPassword = () => setAuthMode('forgot-password');

  switch (authMode) {
    case 'login':
      return (
        <Login
          onSwitchToRegister={switchToRegister}
          onSwitchToForgotPassword={switchToForgotPassword}
        />
      );
    case 'register':
      return <Register onSwitchToLogin={switchToLogin} />;
    case 'forgot-password':
      return <ForgotPassword onSwitchToLogin={switchToLogin} />;
    default:
      return (
        <Login
          onSwitchToRegister={switchToRegister}
          onSwitchToForgotPassword={switchToForgotPassword}
        />
      );
  }
};

export default AuthWrapper;
