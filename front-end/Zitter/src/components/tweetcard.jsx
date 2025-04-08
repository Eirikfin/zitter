import styles from "./style.module.scss"

export default function TweetCard(props){


    return(
        <div className={styles.tweetcard}>
           <h3>{props.username}</h3>
           <p>{props.tweet} {props.hashtags}</p> 
           <p>{props.date}</p> 
        </div>
    )
}