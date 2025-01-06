import {useState, useEffect} from 'react';
import {useParams, Link} from 'react-router-dom';
import axios from 'axios'

const UserInfoPage=()=>{
    const [userInfo, setUserInfo]=useState({
        user_name: '',
        user_semester: 0,
        user_major: '',
        user_info: '',
    });
    const {userId}=useParams();
    useEffect(()=>{
        const loadUserInfo=async()=>{
            const response=await axios.get(`/temp/user/${userId}`);
            const newUserInfo=response.data
            setUserInfo(newUserInfo)
        }
        loadUserInfo();
    }, [userId]);
    return(
        <>
        <h2>My Info</h2>
        <div className='userinfo-section'>
           <div>
                <strong>이름</strong>{userInfo.user_name}
           </div>
           <div>
                <strong>전공</strong>{userInfo.user_major}
           </div>
           <div>
                <strong>학기</strong>{userInfo.user_semester}
           </div>
           <div>
                <strong>유저정보</strong>{userInfo.user_info}
           </div>
        </div>
        <Link to={`/user/${userId}/edit`}>
            <button>수정하기</button>
        </Link>
        </>
    );
}

export default UserInfoPage