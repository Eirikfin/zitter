import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import styles from "./login.module.scss"

export default function LoginPage(){
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch("https://zitter.onrender.com/login", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        throw new Error("Login failed");
      }

      const data = await response.json();
      localStorage.setItem("token", data.token);
      console.log("Login successful:", data);

      localStorage.setItem("token", data.token);

      navigate("/dashboard");
    } catch (err) {
      setError("invalid username or password");
      console.error(err);
    }
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.card}>
        <h2 className={styles.title}>Login to Zitter</h2>
        <form onSubmit={handleLogin} className={styles.form}>
          <input
            className={styles.input}
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            className={styles.input}
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit" className={styles.button}>
            Log In
          </button>
        </form>
        {error && <p className={styles.error}>{error}</p>}
      </div>
    </div>
  );  
}

