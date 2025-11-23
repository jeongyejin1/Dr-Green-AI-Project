import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setResult(null);
      setError(null);

      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("먼저 파일을 선택해주세요.");
      return;
    }
    setIsLoading(true);
    setResult(null);
    setError(null);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      // ⭐️ 백엔드(localhost:8000)로 요청 전송
      const response = await axios.post("http://localhost:8000/analyze", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError("분석 중 오류가 발생했습니다. 백엔드 서버가 켜져 있는지 확인하세요.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌱 Dr. Green: 식물 질병 진단 AI</h1>
        <p>식물 잎 사진을 업로드하면 AI가 질병을 진단해 드립니다.</p>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={isLoading || !selectedFile}>
          {isLoading ? "분석 중..." : "진단하기"}
        </button>
        {error && <p className="error-message">{error}</p>}
        <div className="result-container">
          {preview && (
            <div className="image-preview">
              <h3>미리보기</h3>
              <img src={preview} alt="업로드된 식물 잎" />
            </div>
          )}
          {result && (
            <div className="analysis-result">
              <h3>AI 진단 결과</h3>
              <p><strong>진단명:</strong> {result.disease_name}</p>
              <p><strong>신뢰도:</strong> {result.confidence}</p>
              <p><strong>대처 방안:</strong> {result.solution}</p>
              <p><em>(참고: {result.predicted_class})</em></p>
            </div>
          )}
        </div>
      </header>
    </div>
  );
}
export default App;