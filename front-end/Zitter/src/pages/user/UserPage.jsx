import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import TweetCard from '../../components/tweetcard';
import TweetInput from '../../components/tweetinput';
import SearchBar from "../../components/SearchBar/SearchBar";

export default function UserPage() {
  // States:
  const [data, setData] = useState({});
  const { username } = useParams();

  // Effect:
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`https://zitter.onrender.com/user/${username}`);
        const json = await response.json();
        setData(json);

        if(!response.ok){
            throw new Error("No user was found");
        }
      } catch (err) {
        console.log("Error fetching data:", err);
      }
    };
    fetchData();
  }, [username]);

 
  return (
    <>
      <h1>{data.username}</h1>
      <p>Joined Zitter on: {data.joined ? new Date(data.joined).toLocaleDateString() : 'Loading...'}</p>

      <TweetInput />
      <SearchBar/>

      {/* check if there are any tweets to display: */}
      {data.tweets && data.tweets.length > 0 ? (
        data.tweets.map((tweet, index) => ( //create tweetcards for each tweet
          <TweetCard key={index} username={data.username} message={tweet.message} />
        ))
      ) : (
        //if there are no tweets show message:
        <p>No tweets available.</p>
      )}
    </>
  );
}
