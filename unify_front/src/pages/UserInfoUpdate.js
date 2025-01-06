import {useState, useEffect} from 'react';
import {useParams, useNavigate} from 'react-router-dom';
import { useToken } from '../auth/useToken';
import axios from 'axios'

const UserInfoUpdatePage=()=>{
    const [userInfo, setUserInfo]=useState({
        user_name: '',
        user_semester: 0,
        user_major: '',
        user_info: '',
    });
    const {userId}=useParams();
    const navigate=useNavigate();
    const [token, setToken]=useToken();

    useEffect(()=>{
        const loadUserInfo=async()=>{
            const response=await axios.get(`/user`, 
                {
                    headers:{Authorization: `Bearer ${token}`}
                });
            const newUserInfo=response.data;
            setUserInfo(newUserInfo);
        }
        loadUserInfo();
    }, [userId, token]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setUserInfo((prevInfo) => ({
            ...prevInfo,
            [name]: value, 
        }));
    };

    const handleSave = async () => {
        try {
            await axios.patch(`/user/update`, userInfo, {
                headers:{Authorization: `Bearer ${token}`}
            });
            alert('수정 완료되었습니다.');
            navigate(`/user/${userId}`)
        } catch (error) {
            console.error('Error updating user information:', error);
            alert('Failed to update user information.');
        }
    };

    return(
        <>
        <h2>My Info</h2>
        <div className='userinfo-section'>
           <label>
            이름:
                <input 
                    type="text" 
                    value={userInfo.user_name} 
                    onChange={handleInputChange}
                />
            </label>
            <label>
                    전공:
                    <input
                        type="text"
                        name="user_major" // 필드 이름
                        value={userInfo.user_major}
                        onChange={handleInputChange}
                    />
                </label>
                <label>
                    학기:
                    <input
                        type="number"
                        name="user_semester" // 필드 이름
                        value={userInfo.user_semester}
                        onChange={handleInputChange}
                    />
                </label>
                <label>
                    유저정보:
                    <textarea
                        name="user_info" // 필드 이름
                        value={userInfo.user_info}
                        onChange={handleInputChange}
                    />
                </label>
           <button onClick={handleSave}>저장하기</button>
        </div>
        </>
    );
}

export default UserInfoUpdatePage