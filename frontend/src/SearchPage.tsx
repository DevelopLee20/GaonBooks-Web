import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const SearchPage: React.FC = () => {
  const { storeSpot } = useParams<{ storeSpot: string }>();
  const navigate = useNavigate();

  const handleLogout = () => {
    // 로그아웃 로직 (예: 토큰 삭제)
    alert('로그아웃 되었습니다.');
    navigate('/login'); // 로그인 페이지로 리다이렉션
  };

  return (
    <div className="container-fluid d-flex align-items-center justify-content-center vh-100 bg-light">
      <div className="card p-4 shadow-lg" style={{ width: '420px', borderTop: '5px solid #7ac142' }}>
        <h2 className="card-title text-success text-uppercase fw-bold mb-4 text-center">
          {storeSpot ? `${storeSpot} 검색 페이지` : '검색 페이지'}
        </h2>
        <div className="text-center mb-4">
          <p>환영합니다! 이곳은 {storeSpot} 지점의 검색 페이지입니다.</p>
          {/* 여기에 검색 입력 필드 및 버튼 추가 예정 */}
          <input type="text" className="form-control mb-3" placeholder="검색어를 입력하세요" />
          <button className="btn btn-primary w-100">검색</button>
        </div>
        <div className="d-grid mt-4">
          <button className="btn btn-outline-secondary rounded-pill" onClick={handleLogout}>
            로그아웃
          </button>
        </div>
      </div>
    </div>
  );
};

export default SearchPage;
