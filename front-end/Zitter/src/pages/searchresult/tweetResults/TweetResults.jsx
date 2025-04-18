import {useState, useEffect} from "react"
import { useParams } from "react-router-dom";
import TweetCard from "../../../components/tweetcard";


export default function TweetResults(){
    const [data, setData] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(false);
    const { query } = useParams();
    const apiUrl = `http://localhost:8000/tweets/search?query=${query}`;


    useEffect(() => {
        const request = async () => {
            setIsLoading(true);
            const result = await fetch(apiUrl)
            if(!result.ok){
                setError(true);
                setIsLoading(false);
                throw Error("Failed to fetch tweets");
            }
            setData(await result.json());
            setIsLoading(false)
        }
        request();
    }, [apiUrl])
    

    if(isLoading){
        return ( 
        <>
        <h2>Tweets:</h2>
        <p>loading...</p>
        </>
        )
    }
    if(error){
        return( 
        <>
        <h2>Tweets:</h2>
        <p>No tweets found</p>
        </>
        )
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


