import {useState, useEffect} from "react"
import { useParams } from "react-router-dom";
import TweetCard from "../../../components/tweetcard";


export default function TweetResults(){
    const [data, setData] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const { query } = useParams();
    const apiUrl = `http://localhost:8000/tweets/search?query=${query}`;


    useEffect(() => {
        const request = async () => {
            setIsLoading(true);
            const result = await fetch(apiUrl)
            if(!result.ok){
                throw Error("Failed to fetch tweets")
            }
            setData(await result.json());
            setIsLoading(false)
        }
        request();
    }, [apiUrl])
    
    if(isLoading){
        return <p>loading...</p>
    }

    return (
        <>
        <h2>Tweets:</h2>
        {data.map(tweet => (   
            <TweetCard key={tweet.id} username={tweet.username} message={tweet.message} date={tweet.time_created}/>
        ))}
        </>
    )
}


