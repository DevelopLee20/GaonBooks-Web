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

  // 지점을 한글로 변경하는 부분
  const storeSpotMap: { [key: string]: string } = {
    sch: '순천향대학교',
    sunmoon: "선문대학교",
    nasaret: "나사렛대학교",
    kongju: "공주대학교",
    mokwon: "목원대학교",
    // Add other store spots as needed
  };

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
      } catch (err) {
        if (err instanceof Error) {
          setOptionsError(err.message);
        } else {
          setOptionsError('알 수 없는 오류가 발생했습니다.');
        }
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
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('storeSpot', storeSpot); // Add this line
      console.log('Login successful:', data);
      // Here you would typically store the token (e.g., in localStorage or a state management solution)
      // and redirect the user to a protected route.
      // alert('Login successful! Token: ' + data.access_token); // 제거
      navigate(`/search/${storeSpot}`); // 추가
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('알 수 없는 오류가 발생했습니다.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container-fluid d-flex flex-column align-items-center justify-content-center vh-100 bg-light">
      <div className="card p-4 shadow-lg" style={{ width: '420px', borderTop: '5px solid #7ac142' }}>
        <h2 className="card-title text-success text-uppercase fw-bold mb-4">가온북스 도서검색</h2>
        <form onSubmit={handleSubmit} className="mt-4">
          {error && <p className="text-danger text-center mb-4">{error}</p>}
          <div className="mb-4">
            <label htmlFor="userId" className="form-label">
              관리자 아이디
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
              비밀번호
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
              가온북스 지점
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
                    {storeSpotMap[option] || option}
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
              {loading ? 'Logging in...' : '로그인'}
            </button>
          </div>
        </form>
      </div>
      <div className="text-center text-muted mt-3" style={{ fontSize: '0.8em' }}>
        <p className="mb-0">version 1.0.0</p>
        <p className="mb-0">author developlee20</p>
      </div>
    </div>
  );
};

export default LoginPage;
