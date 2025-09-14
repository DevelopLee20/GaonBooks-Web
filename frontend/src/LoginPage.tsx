import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [storeSpotOptions, setStoreSpotOptions] = useState<string[]>([]);
  const [storeSpot, setStoreSpot] = useState<string>('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [optionsLoading, setOptionsLoading] = useState(true);
  const [optionsError, setOptionsError] = useState('');

  useEffect(() => {
    const fetchStoreSpotOptions = async () => {
      try {
        const response = await fetch('/auth/store-spots');
        if (!response.ok) {
          throw new Error('Failed to fetch store spot options');
        }
        const data: string[] = await response.json();
        setStoreSpotOptions(data);
        if (data.length > 0) {
          setStoreSpot(data[0]);
        }
      } catch (err: any) {
        setOptionsError(err.message);
      } finally {
        setOptionsLoading(false);
      }
    };
    fetchStoreSpotOptions();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('/auth/login', { // Assuming your backend is on the same origin
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: userId, password, store_spot: storeSpot }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
      }

      const data = await response.json();
      console.log('Login successful:', data);
      // Here you would typically store the token (e.g., in localStorage or a state management solution)
      // and redirect the user to a protected route.
      // alert('Login successful! Token: ' + data.access_token); // 제거
      navigate(`/search/${storeSpot}`); // 추가
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container-fluid d-flex align-items-center justify-content-center vh-100 bg-light">
      <div className="card p-4 shadow-lg" style={{ width: '420px', borderTop: '5px solid #7ac142' }}>
        <h2 className="card-title text-success text-uppercase fw-bold mb-4">Login</h2>
        <form onSubmit={handleSubmit} className="mt-4">
          {error && <p className="text-danger text-center mb-4">{error}</p>}
          <div className="mb-4">
            <label htmlFor="userId" className="form-label">
              User ID
            </label>
            <input
              type="text"
              id="userId"
              className="form-control mb-3"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              required
            />
          </div>
          <div className="mb-4">
            <label htmlFor="password" className="form-label">
              Password
            </label>
            <input
              type="password"
              id="password"
              className="form-control mb-3"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="mb-6">
            <label htmlFor="storeSpot" className="form-label">
              Store Spot
            </label>
            {optionsLoading ? (
              <p>Loading store spots...</p>
            ) : optionsError ? (
              <p className="text-danger">{optionsError}</p>
            ) : (
              <select
                id="storeSpot"
                className="form-control mb-3"
                value={storeSpot}
                onChange={(e) => setStoreSpot(e.target.value)}
                required
              >
                {storeSpotOptions.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            )}
          </div>
          <div className="d-grid">
            <button
              type="submit"
              className="btn btn-success rounded-pill w-100 mt-4"
              disabled={loading}
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
