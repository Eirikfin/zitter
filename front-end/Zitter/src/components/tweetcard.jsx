import styles from "./style.module.scss"
import {Route, Link} from "react-router-dom";

export default function TweetCard(props){


    return(
        <div className={styles.tweetcard}>
          <Link to={`/user/${props.username}`}><h3>{props.username}</h3></Link>
           <p>{props.message}</p> 
           <p>{props.date}</p> 
        </div>
    )
}