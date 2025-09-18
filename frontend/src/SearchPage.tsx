import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

interface Book {
  book_title: string;
  publisher: string;
  location: string;
}

const SearchPage: React.FC = () => {
  const { storeSpot } = useParams<{ storeSpot: string }>();
  const navigate = useNavigate();

  const isAuthenticated = useRef(false); // To prevent multiple redirects

  // 지점을 한글로 변경하는 부분
  const storeSpotMap: { [key: string]: string } = {
    sch: '순천향대학교',
    sunmoon: "선문대학교",
    nasaret: "나사렛대학교",
    kongju: "공주대학교",
    mokwon: "목원대학교",
    // Add other store spots as needed
  };

  const displayStoreSpot = storeSpot ? storeSpotMap[storeSpot] || storeSpot : '';

  

  const [searchTerm, setSearchTerm] = useState<string>('');
  const [searchResults, setSearchResults] = useState<Book[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // const handleLogout = () => {
  //   // 로그아웃 로직 (예: 토큰 삭제)
  //   alert('로그아웃 되었습니다.');
  //   navigate('/login'); // 로그인 페이지로 리다이렉션
  // };

  const handleSearch = async () => {
    if (!searchTerm.trim()) {
      setError('검색어를 입력해주세요.');
      setSearchResults([]);
      return;
    }

    setLoading(true);
    setError(null);
    setSearchResults([]);

    try {
      const response = await fetch(`/books/search/${searchTerm}?store_spot=${storeSpot}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || '검색 중 오류가 발생했습니다.');
      }
      const data = await response.json();
      setSearchResults(data.books);
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
    <div className="container-fluid d-flex align-items-center justify-content-center bg-light">
      <div className="card p-4 shadow-lg d-flex flex-column" style={{ width: '90%', height: '90%', borderTop: '5px solid #7ac142' }}>
        <h2 className="card-title text-success text-uppercase fw-bold mb-4 text-center">
          {"가온북스 도서 위치 검색 페이지"}
          <button
            onClick={() => navigate('/admin')}
            style={{
              position: 'absolute',
              top: '10px',
              right: '10px',
              width: '20px',
              height: '20px',
              opacity: 0, // Hidden
              cursor: 'pointer',
            }}
            aria-label="Admin Page"
          ></button>
        </h2>
        <div className="text-center mb-4">
          <p>지점: {displayStoreSpot}</p>
          {/* 여기에 검색 입력 필드 및 버튼 추가 예정 */}
          <input
            type="text"
            className="form-control mb-3"
            placeholder="검색어를 입력하세요"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                handleSearch();
              }
            }}
          />
          <button className="btn btn-primary w-100" onClick={handleSearch} disabled={loading}>
            {loading ? '검색 중...' : '검색'}
          </button>
        </div>
        {/* 검색 결과 목록이 표시될 공간 */}
        <div className="search-results-container mt-4 flex-grow-1" style={{ overflowY: 'auto', border: '1px solid #e0e0e0', borderRadius: '5px', padding: '10px', minHeight: '0' }}>
          {loading && <p className="text-center">검색 중...</p>}
          {error && <p className="text-center text-danger">{error}</p>}
          {!loading && !error && searchResults.length === 0 && searchTerm.trim() !== '' && (
            <p className="text-center text-muted">검색 결과가 없습니다.</p>
          )}
          {!loading && !error && searchResults.length === 0 && searchTerm.trim() === '' && (
            <p className="text-center text-muted">책 제목이나 키워드로 입력하여 검색하세요.</p>
          )}
          {!loading && !error && searchResults.length > 0 && (
            <ul className="list-group list-group-flush">
              {searchResults.map((book, index) => (
                <li key={index} className="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <strong>{book.book_title}</strong>
                    <br />
                    <small className="text-muted">출판사: {book.publisher || 'N/A'}</small>
                    <br />
                    <small className="text-muted">위치: {book.location || 'N/A'}</small>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
        {/* <div className="d-grid mt-4">
          <button className="btn btn-outline-secondary rounded-pill" onClick={handleLogout}>
            로그아웃
          </button>
        </div> */}
      </div>
    </div>
  );
};

export default SearchPage;
