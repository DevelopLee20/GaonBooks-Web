import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './HomePage';
import LoginPage from './LoginPage';
import SearchPage from './SearchPage';
import AdminPage from './AdminPage';
import PrivateRoute from './PrivateRoute';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/search/:storeSpot" element={<SearchPage />} />
        <Route
          path="/admin"
          element={
            <PrivateRoute>
              <AdminPage />
            </PrivateRoute>
          }
        />
        <Route path="*" element={<HomePage />} /> {/* 기본 경로 또는 잘못된 경로 처리 */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
