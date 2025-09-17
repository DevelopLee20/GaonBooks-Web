import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const AdminPage: React.FC = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [storeSpot, setStoreSpot] = useState<string>(''); // This will come from the logged-in user's context or a selection

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

  // In a real application, storeSpot would likely come from user context after login
  // For now, we'll try to get it from localStorage or prompt the user
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      alert('로그인이 필요합니다.');
      navigate('/login');
      return;
    }
    // In a real app, you'd decode the token or fetch user info to get storeSpot
    // For this example, let's assume storeSpot is also stored in localStorage or derived
    const storedStoreSpot = localStorage.getItem('storeSpot'); // Assuming storeSpot is stored during login
    if (storedStoreSpot) {
      setStoreSpot(storedStoreSpot);
    } else {
      setError('지점 정보를 찾을 수 없습니다. 다시 로그인해주세요.');
    }
  }, [navigate]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    } else {
      setFile(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage('');
    setError('');

    if (!file) {
      setError('엑셀 파일을 선택해주세요.');
      return;
    }

    if (!storeSpot) {
      setError('지점 정보가 없어 파일을 업로드할 수 없습니다.');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/books/upload/excel?store_spot=${storeSpot}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          // 'Content-Type': 'multipart/form-data' is automatically set by FormData
        },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || '파일 업로드 실패');
      }

      const result = await response.json();
      setMessage(`${result.detail}\n\n총 책 수: ${result.added_books_count}`);
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

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('storeSpot');
    navigate('/');
  };

  return (
    <div className="container-fluid d-flex align-items-center justify-content-center vh-100 bg-light">
      <div className="card p-4 shadow-lg" style={{ width: '500px', borderTop: '5px solid #7ac142' }}>
        <h2 className="card-title text-success text-uppercase fw-bold mb-4 text-center">관리자 페이지</h2>
        <form onSubmit={handleSubmit}>
          {error && <p className="text-danger text-center mb-3">{error}</p>}
          {message && <p className="text-success text-center mb-3">{message}</p>}

          <div className="mb-3">
            <label htmlFor="excelFile" className="form-label">엑셀 파일 업로드</label>
            <input
              type="file"
              id="excelFile"
              className="form-control"
              accept=".xlsx, .xls"
              onChange={handleFileChange}
              required
            />
          </div>

          <div className="mb-3">
            <p>현재 지점: <strong>{displayStoreSpot || '정보 없음'}</strong></p>
          </div>

          <button type="submit" className="btn btn-primary w-100" disabled={loading}>
            {loading ? '업로드 중...' : '엑셀 파일 업로드'}
          </button>
        </form>
        <div className="mt-3 text-center">
          <button className="btn btn-outline-secondary" onClick={handleLogout}>로그아웃</button>
        </div>
      </div>
    </div>
  );
};

export default AdminPage;
