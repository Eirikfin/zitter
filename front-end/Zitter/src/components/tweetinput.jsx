import { useState } from "react";
import styles from "./style.module.scss";

export default function TweetInput() {
  //states:
  const [tweet, setTweet] = useState("");
  //temprary: replace with userid from authorization
  // const user = ;

  const postTweet = async (e) => {
    e.preventDefault(); //prevents reload when from is submitted
    try {
    //request to send to server:
      const request = {
        user_id: 1, //replace with userid later
        message: tweet, //tweet to be submitted
      };
      //API call
      const response = await fetch("http://localhost:8000/tweets", {
        method: "POST",
        headers: {
          "Content-type": "application/json; charset=UTF-8",
        },
        body: JSON.stringify(request), //send the request in body
      });
      //if sucessful:
      if (response.ok) {
        setTweet(""); //reset tweet state to empty
        console.log("Tweet was posted!");
      } else {
        console.log("Failed to tweet");
      }
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <>
      <form className={styles.tweetcard} onSubmit={postTweet}>
        <label>Your Tweet:</label>
        <input
          type="text"
          name="tweet"
          placeholder="What's happening?"
          onChange={(e) => setTweet(e.target.value)}
        ></input>
        <input className={styles.send_btn} type="submit" value="Post"></input>
      </form>
    </>
  );
}
