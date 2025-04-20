import React, { useState, useContext } from 'react'
import { GlobalContext } from '../context/GlobalState';

export const NewTweet = () => {
    const [content, setContent] = useState('');
    const { addTweet } = useContext(GlobalContext);
    const handleNewTweet = () => addTweet(content);

    return (
        <div className="new-tweet">
            <div className="right">
                <div className="flex-align-center">
                    <input className="w-100" placeholder="What's happening?" type="text" onChange={(event) => setContent(event.target.value)} />
                </div>
                <div className="new-tweet-options">
                    <div className="tweet" onClick={handleNewTweet}>
                        <div className="btn tweet-btn text-center">Tweet</div>
                    </div>
                </div>
            </div>
        </div>
    )
}
