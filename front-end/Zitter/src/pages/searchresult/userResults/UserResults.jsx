import { useState, useEffect } from "react"
import { Link, useParams } from "react-router-dom";

export default function UserResults(){
    const [isLoading, setIsLoading] = useState(false)
    //data from api
    const [data, setData] = useState([]);
    //search query
    const { query } = useParams()
    //api call
    const apiUrl = `http://localhost:8000/users/search?query=${query}`;
//to do add apiurl when it is complete:
useEffect(() => {
    const request = async () => {
        //set loading to true
        setIsLoading(true);
        //fetch data:
        const result = await fetch(apiUrl);
         if(!result.ok){
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
        return <p>Loading...</p>
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