import './App.css';
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import Navbar from './components/Navbar'
import ChatPage from './pages/ChatPage';
import UserInfoPage from './pages/UserInfoPage';
import UserInfoUpdatePage from './pages/UserInfoUpdate';
import LoginPage from './pages/LogInPage';
import CreateAccountPage from './pages/CreateAccountPage'

function App() {
  return (
    <BrowserRouter>
    <div className="App">
      <h1>Unify</h1>
      <Navbar/>
      <div id="page-body">
        <Routes>
          <Route path="/login" element={<LoginPage/>}/>
          <Route path="/create-account" element={<CreateAccountPage/>}/>
          <Route path="/chat" element={<ChatPage/>}/>
          <Route path="/user/:userId" element={<UserInfoPage/>}/>
          <Route path="/user/:userId/edit" element={<UserInfoUpdatePage/>}/>
        </Routes>
      </div>
    </div>
    </BrowserRouter>
  );
}

export default App;
