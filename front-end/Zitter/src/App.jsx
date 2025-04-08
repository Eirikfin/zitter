import { useState } from 'react'
import TweetCard from './components/tweetcard'
import {BrowserRouter, Routes, Route} from "react-router-dom";
import Dashboard from './pages/dashboard/dashboard';

function App() {
  const [count, setCount] = useState(0)

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard/>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
