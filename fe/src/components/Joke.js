import { useEffect, useState } from "react";

function Joke() {
  const [joke, setJoke] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch("https://icanhazdadjoke.com/", {
      headers: {
        Accept: "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setJoke(data.joke);
        setLoading(false);
      })
      .catch(() => {
        setError(true);
        setLoading(false);
      });
  }, []);

  return (
    <div>
      {loading ? <p>Loading...</p> : error ? <p>Error!</p> : <p>{joke}</p>}
    </div>
  );
}

export default Joke;
