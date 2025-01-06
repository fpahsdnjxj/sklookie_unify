import {Link} from 'react-router-dom'

const NavBar=()=>{
    return(
        <nav>
            <li>
                <Link to="/chat">Chat</Link>
            </li>
        </nav>
    )
}

export default NavBar