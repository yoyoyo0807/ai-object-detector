"use client";
import { useState } from 'react';

export default function Home() {
  const [result, setResult] = useState<any>(null);

  const uploadImage = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    // バックエンド（FastAPI）へ画像を送信
    const res = await fetch('http://localhost:8000/detect', {
      method: 'POST',
      body: formData,
    });
    const data = await res.json();
    setResult(data);
  };

  return (
    <main style={{ padding: '40px', fontFamily: 'sans-serif', textAlign: 'center' }}>
      <h1>AI Object Detector (YOLOv11)</h1>
      <p>画像をアップロードしてAIに物体を認識させてみましょう！</p>
      
      <div style={{ margin: '20px 0' }}>
        <input type="file" onChange={uploadImage} accept="image/*" />
      </div>
      
      {result && (
        <div style={{ marginTop: '30px', textAlign: 'left', display: 'inline-block' }}>
          <h3>検出結果 (JSON):</h3>
          <pre style={{ background: '#f4f4f4', padding: '15px', borderRadius: '8px', border: '1px solid #ddd' }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </main>
  );
}