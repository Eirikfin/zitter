import styles from "./style.module.scss";

export default function TweetInput(){


    return(
        <>
        <form className={styles.tweetcard} method="POST">
            <label>Your Tweet:</label>
            <input type="textarea" name="tweet" placeholder="What's happening?"></input>
            <input className={styles.send_btn} type="submit" value="Post"></input>
        </form>
        
        
        </>
    )
}