import { useState, useEffect } from "react"
import { Link, useParams } from "react-router-dom";

export default function UserResults(){
    const [isLoading, setIsLoading] = useState(false)
    //data from api
    const [data, setData] = useState([]);
    
    const [error, setError] = useState(false);
    //search query
    const { query } = useParams()
    //api call
    const apiUrl = `https://zitter.onrender.com/users/search?query=${query}`;
//to do add apiurl when it is complete:
useEffect(() => {
    const request = async () => {
        //set loading to true
        setIsLoading(true);
        //fetch data:
        const result = await fetch(apiUrl);
         if(!result.ok){
            setError(true)
            setIsLoading(false);
            
             throw Error("Failed to fetch users")
         }
         setData(await result.json());
         //set loading to false
         setIsLoading(false);
     };
     //call function
     request()
     
},[apiUrl]);

    if(isLoading){
        return ( 
        <>
        <h2>Users:</h2>
        <p>Loading...</p>
        </>
        )
    }

    if(error){
        return ( 
        <>
        <h2>Users:</h2>
        <p>No users was found</p>
        </>
        )
    }

    return (
        <>
        <h2>Users:</h2>
        {data.map(user => (
            <div key={user.id}>
                <Link to={`/user/${user.username}`}><h3>{user.username}</h3></Link>
                <p>Joined: {user.joined}</p>
            </div>
        ))}
        </>
    )
}