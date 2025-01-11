import {Link} from 'react-router-dom'
import {useToken} from '../auth/useToken'

const NavBar=()=>{
    const [ , setToken]=useToken();
    const logOut=()=>{
        setToken(null);
    }
    return(
        <>
        <nav>
            <li>
                <Link to="/login">Login</Link>
            </li>
        </nav>
        <button onClick={logOut}>log out</button>
        </>
    )
}

export default NavBar