import TweetCard from "../../components/tweetcard"
import TweetInput from "../../components/tweetinput"
export default function Dashboard(){


    return(
    <>
    <TweetInput/>
    { //TODO: show username/userinfo

    //TODO:Textfield where user can post a tweet

    //TODO: a search field where user can search hashtags
    
    //TODO: display all tweets
    }
    <TweetCard username="ElonDust" tweet="hurr durr woke mind virus hurr durr" hashtags="#verysmart #imsofunny" date="08.04.2025"/>
    <TweetCard username="NiceGuy" tweet="Hello :)" hashtags="#greeting #benice" date="08.04.2025"/>
    </>
    )
}