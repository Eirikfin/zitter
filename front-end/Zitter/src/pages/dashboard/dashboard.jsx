import { useState, useEffect } from "react"
import TweetCard from "../../components/tweetcard"
import TweetInput from "../../components/tweetinput"
import SearchBar from "../../components/SearchBar/SearchBar";


export default function Dashboard(){
const [data, setData] = useState([]);
useEffect(() => {
    const fetchData = async () => {
        try{
            const response = await fetch("http://localhost:8000/tweets/all");
            const json = await response.json();
            setData(json);
        }catch(err){
            console.log("Error fething tweets:", err);
        }
    }

    fetchData();
},[])


console.log(data);
    return(
    <>
     <TweetInput/>
    {
        data.map((tweet, index) => {
            return (
                <TweetCard key={index} username={tweet.username} message={tweet.message} date={tweet.time_created} />
            )
        })
    }

   
    { //TODO: show username/userinfo

    
    //TODO: a search field where user can search hashtags
    <SearchBar/>
    }
    
    </> 
    )}
