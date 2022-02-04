import { useState, useEffect } from "react";
import logo from "../assets/logo.png";
import { API_BASE_URL } from "../config";
import Blockchain from "./Blockchain";

function App() {
  const [walletInfo, setWalletInfo] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetch(`${API_BASE_URL}/wallet/info`);
      setWalletInfo(await data.json());
    };
    fetchData().catch(console.error);
  }, []);

  const { address, balance } = walletInfo;

  return (
    <div className="App">
      <img src={logo} alt="pychain logo" className="logo" />
      <h3>Welcome to Pychain</h3>
      <br />
      <div className="WalletInfo">
        <div className="">Address: {address}</div>
        <div className="">Balance: {balance}</div>
      </div>
      <br />
      <Blockchain />
    </div>
  );
}

export default App;
