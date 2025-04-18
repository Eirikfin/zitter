import React from "react";
import styles from "./searchbar.module.scss";

function SearchBar() {
  return (
    <div className={styles.searchContainer}>
      <input type="text" className={styles.input} placeholder="Search" />
      <button className={styles.button}>Search</button>
    </div>
  );
}

export default SearchBar;
