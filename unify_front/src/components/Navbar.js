import {Link} from 'react-router-dom'

const NavBar=()=>{
    return(
        <nav>
            <li>
                <Link to="/login">Login</Link>
            </li>
        </nav>
    )
}

export default NavBar