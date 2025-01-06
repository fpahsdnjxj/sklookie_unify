
import {Routes, Route} from 'react-router-dom'
import ChatPage from './pages/ChatPage';
import UserInfoPage from './pages/UserInfoPage';
import UserInfoUpdatePage from './pages/UserInfoUpdate';
import LoginPage from './pages/LogInPage';
import CreateAccountPage from './pages/CreateAccountPage';
import { PrivateRoute } from './auth/PrivateRoute';
import ChatListPage from './pages/ChatListPage';
export const AppRoutes=()=>{
    return(
        <Routes>
          <Route path="/login" element={<LoginPage/>}/>
          <Route path="/create-account" element={<CreateAccountPage/>}/>
          <Route path="/chat/:chatId" element={<PrivateRoute element={<ChatPage/>}/>}/>
          <Route path="/user/:userId" element={<PrivateRoute element={<UserInfoPage/>}/>}/>
          <Route path="/user/:userId/edit" element={<PrivateRoute element={<UserInfoUpdatePage/>}/>}/>
          <Route path="/chatlist" element={<PrivateRoute element={<ChatListPage/>}/>}/>
        </Routes>
    );
};



