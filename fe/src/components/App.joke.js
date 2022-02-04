import { useState } from "react";
import Joke from "./Joke";

function App() {
  const [userQuery, setUserQuery] = useState("");
  const updateUserQuery = (e) => {
    console.log("userQuery", userQuery);
    setUserQuery(e.target.value);
  };

  const searchQuery = (e) => {
    window.open("https://google.com/search?q=" + userQuery);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      searchQuery();
    }
  };

  return (
    <div className="App">
      <input
        value={userQuery}
        onChange={updateUserQuery}
        onKeyPress={handleKeyPress}
      />
      <div className="">{userQuery}</div>
      <button onClick={searchQuery}>Search</button>
      <hr />
      <Joke />
    </div>
  );
}

export default App;
