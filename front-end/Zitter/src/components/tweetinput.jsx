import { useState } from "react";
import styles from "./tweetInput.module.scss";

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
        message: tweet, //tweet to be submitted
      };
      //API call
    
      const response = await fetch("https://zitter.onrender.com/tweets", {
        method: "POST",
        headers: {
          "Content-type": "application/json; charset=UTF-8",
          "Authorization": localStorage.getItem('token')
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
  <div className={styles.wrapper}>
    <form className={styles.tweetcard} onSubmit={postTweet}>
      <label>Your Tweet:</label>
      <textarea
        className={styles.textarea}
        placeholder="What's happening?"
        value={tweet}
        onChange={(e) => setTweet(e.target.value)}
        rows={3}
      />
      <input className={styles.send_btn} type="submit" value="Post" />
    </form>
  </div>
    </>
  );
}
