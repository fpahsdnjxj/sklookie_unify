import {useState} from 'react';
import {Link, useNavigate} from 'react-router-dom';
import { useToken } from '../auth/useToken';
import axios from 'axios';

const LoginPage=()=>{
    const [logInID, setLogInId]=useState('');
    const [password, setPassword]=useState('');
    const [error, setError]=useState('');
    const [,setToken]=useToken();
    const navigate=useNavigate();
    const logIn=async()=>{
        try{
            const loginInfo={
                user_loginid: logInID,
                user_password: password,
            }
            const response=await axios.post('auth/login', loginInfo);
            const {access_token}=response.data;
            setToken(access_token); 
            navigate(`/user/${logInID}`);
        }catch(e){
            setError(e.message);
        }
    }

    return(
        <>
        <h1>Log in</h1>
        {error && <p className="error">{error}</p>}
        <input
        placeholder="ID"
        value={logInID}
        onChange={(e)=>setLogInId(e.target.value)}
        />
        <input 
        type="password"
        placeholder="Your password"
        value={password}
        onChange={(e)=>setPassword(e.target.value)}
        />
        <button onClick={logIn}>Log In</button>
        <Link to="/create-account">
        Don't have an account? Create one here
        </Link>
        </>
    );
}

export default LoginPage;