import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [count, setCount] = useState(0);
  const API_URL = process.env.REACT_APP_API_URL;

  // 서버에서 초기 숫자 로드
  useEffect(() => {
    axios.get(`${API_URL}/number`)
      .then(response => setCount(response.data.value))
      .catch(error => console.error(error));
  }, [API_URL]);

  // 숫자를 증가시키는 함수
  const increment = () => {
    axios.post(`${API_URL}/plus`)
      .then(response => setCount(response.data.value))
      .catch(error => console.error(error));
  };

  // 숫자를 감소시키는 함수
  const decrement = () => {
    axios.post(`${API_URL}/minus`)
      .then(response => setCount(response.data.value))
      .catch(error => console.error(error));
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>값 : {count}</h1>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
    </div>
  );
}

export default App;
