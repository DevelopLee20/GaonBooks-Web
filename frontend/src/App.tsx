import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from './LoginPage';
import SearchPage from './SearchPage';
import AdminPage from './AdminPage'; // Import AdminPage
import PrivateRoute from './PrivateRoute';

function App() {
  return (
    <BrowserRouter>
      <Routes>
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
        <Route path="*" element={<LoginPage />} /> {/* 기본 경로 또는 잘못된 경로 처리 */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
