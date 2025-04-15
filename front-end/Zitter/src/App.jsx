import TweetCard from './components/tweetcard'
import {BrowserRouter, Routes, Route} from "react-router-dom";
import Dashboard from './pages/dashboard/dashboard';
import UserPage from './pages/user/UserPage';

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard/>} />
        <Route path="/user/:username" element={<UserPage/>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App
