import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import TweetCard from '../../components/tweetcard';
import TweetInput from '../../components/tweetinput';

export default function UserPage() {
  // States:
  const [data, setData] = useState({});
  const { username } = useParams();

  // Effect:
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://localhost:8000/user/${username}`);
        const json = await response.json();
        setData(json);
      } catch (err) {
        console.log("Error fetching data:", err);
      }
    };
    fetchData();
  }, [username]);

  console.log(data);

  return (
    <>
      <h1>Hello, {data.username}</h1>
      <p>You joined Zitter on: {data.joined ? new Date(data.joined).toLocaleDateString() : 'Loading...'}</p>

      <TweetInput />

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
