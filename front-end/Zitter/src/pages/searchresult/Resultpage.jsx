import TweetResults from "./tweetResults/TweetResults"
import UserResults from "./userResults/UserResults"

export default function ResultPage(){



    return(
        <>
        <h1>This is where search results should be displayed:</h1>
        <UserResults/>
        <TweetResults/>
        {/* 
           show accounts matching result:
           Show tweets matching result:
           Show tweet mathing hastag? (should this be different?):  
            */}
        </>
    )
}