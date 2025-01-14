import {useState} from 'react';
import {Link, useNavigate} from 'react-router-dom';
import axios from 'axios'

const CreateAccountPage=()=>{
    const [logInId, setLogInId]=useState('');
    const [password, setPassword]=useState('');
    const [name, setName]=useState('');
    const [error, setError]=useState('');
    const [confirmPassword, setConfirmPassword]=useState('');
    const navigate=useNavigate();

    const createAccount=async()=>{
        try{
            if(password!==confirmPassword){
                setError('Password and confirm password do not match');
                return;
            }
            const userInfo={
                user_loginid: logInId,
                user_password: password,
                user_name: name
            }
            await axios.post('/api/auth/sign-up', userInfo);
            navigate('/login');
        }catch(e){
            setError(e.message);
        }
    }

    return(
        <>
        <h1>Create Account</h1>
        {error && <p className="error">{error}</p>}
        <input
        placeholder="Name"
        value={name}
        onChange={(e)=>setName(e.target.value)}
        />
        <input
        placeholder="ID"
        value={logInId}
        onChange={(e)=>setLogInId(e.target.value)}
        />
        <input 
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e)=>setPassword(e.target.value)}
        />
        <input 
        type="password"
        placeholder="Re-enter Your password"
        value={confirmPassword}
        onChange={(e)=>setConfirmPassword(e.target.value)}
        />
        <button onClick={createAccount}>Create Account</button>
        <Link to="/login">
        Already have an account? Log in here
        </Link>
        </>
    );
}



export default CreateAccountPage;