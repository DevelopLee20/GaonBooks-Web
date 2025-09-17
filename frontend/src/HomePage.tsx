import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [storeSpotOptions, setStoreSpotOptions] = useState<string[]>([]);
  const [storeSpot, setStoreSpot] = useState<string>('');
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
          throw new Error('지점 목록을 불러오는 데 실패했습니다.');
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

  const handleNavigate = () => {
    if (storeSpot) {
      navigate(`/search/${storeSpot}`);
    }
  };

  return (
    <div className="container-fluid d-flex flex-column align-items-center justify-content-center vh-100 bg-light">
      <div className="card p-4 shadow-lg" style={{ width: '420px', borderTop: '5px solid #7ac142' }}>
        <h2 className="card-title text-success text-uppercase fw-bold mb-4">가온북스 도서 검색</h2>
        <div className="mt-4">
          <div className="mb-6">
            <label htmlFor="storeSpot" className="form-label">
              가온북스 지점 선택
            </label>
            {optionsLoading ? (
              <p>지점 목록을 불러오는 중...</p>
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
              type="button"
              className="btn btn-success rounded-pill w-100 mt-4"
              onClick={handleNavigate}
              disabled={optionsLoading || !!optionsError}
            >
              검색 페이지로 이동
            </button>
          </div>
        </div>
      </div>
      <div className="text-center text-muted mt-3" style={{ fontSize: '0.8em' }}>
        <p className="mb-0">version 1.2.１</p>
        <p className="mb-0">author developlee20</p>
      </div>
    </div>
  );
};

export default HomePage;
