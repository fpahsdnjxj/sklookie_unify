import {Navigate} from 'react-router-dom';
import {useToken} from './useToken'

export const PrivateRoute=({element})=>{
    const [token]=useToken();

    if(!token) return <Navigate to="/login"/>

    return element
}