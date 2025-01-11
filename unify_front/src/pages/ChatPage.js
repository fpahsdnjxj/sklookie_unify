import {useState} from 'react';
import axios from 'axios'
import { useParams } from 'react-router-dom';
import {useToken} from '../auth/useToken'

const ChatPage=()=>{
    const {chatId}=useParams();
    const [token, ]=useToken();

    const [question, setQuestion]=useState('');
    const [answer, setAnswer]=useState('');

    const getAnswer=async()=>{
        setAnswer('답변이 나올 때까지 잠시만 기다려 주세요');
        const response=await axios.post(`/message/${chatId}`,{
            question:question
        }, {
            headers: {Authorization: `Bearer ${token}`}
        });
        const aiAnswer=response.data;
        setAnswer(aiAnswer.data);
        setQuestion('');
    }
    return(
        <>
        <h2>Please input question</h2>
        <label>
            Question:
            <textarea value={question}
            onChange={e=>setQuestion(e.target.value)}
            rows="4" cols="50"/>
        </label>
        <button onClick={getAnswer}>Send</button>
        <p>{answer}</p>
        </>
    )
}

export default ChatPage