import {useState, useEffect} from 'react'
import { Link } from 'react-router-dom';
import { useToken } from '../auth/useToken';
import axios from 'axios';

const ChatListPage=()=>{
    const [token, ]=useToken();
    const [chatList, setChatList]=useState([]);

    useEffect(()=>{
        const getChatList=async()=>{
            const response=await axios.get('/chat', 
                {headers:{Authorization:`Bearer ${token}`}});
            const {chats}=response.data;
            setChatList(chats);
        };
        getChatList();
    }, [token])

    
    return(
        <>
        <h1>Chat list</h1>
            <div>
            {chatList.length>0?
                (chatList.map((chat, i)=>(
                    <Link to={`/chat/${chat.chat_id}`}>
                    <ul key={i}>
                        <li>{chat.chat_name}</li>
                        <li>{chat.start_date}</li>
                    </ul>
                    </Link>
                ))):<div>No Chat Aviable</div>}
            </div>
        </>
    );
}

export default ChatListPage;
