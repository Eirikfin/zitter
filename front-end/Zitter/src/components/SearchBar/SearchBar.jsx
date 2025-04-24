import { useRef } from 'react';
import styles from "./searchbar.module.scss";
import { useNavigate } from "react-router-dom"

function SearchBar() {
  const navigate = useNavigate();
  const inputRef = useRef(null);
  
  
  const handleSearch = (e) => {
    e.preventDefault();
    const query = inputRef.current.value;
    navigate(`/search/${query}`)
  }

  return (
    <div className={styles.searchContainer}>
      <form onSubmit={handleSearch}>
      <input type="text" ref={inputRef} name="searchbar" className={styles.input} placeholder="Search" />
      <button type="submit" className={styles.button}>Search</button>
      </form>
    </div>
  );
}

export default SearchBar;
