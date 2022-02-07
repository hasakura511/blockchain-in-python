import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "react-bootstrap";
import Transaction from "./Transaction";
import { API_BASE_URL, POLL_INTERVAL } from "../config";

function TransactionPool() {
  const navigate = useNavigate();

  const [transactions, setTransactions] = useState([]);
  const mineBlock = async () => {
    try {
      const data = await fetch(`${API_BASE_URL}/bc/mine`);
      navigate("/blockchain");
    } catch (err) {
      console.error(err);
    }
  };
  const fetchData = async () => {
    try {
      const data = await fetch(`${API_BASE_URL}/bc/transactions`);
      setTransactions(await data.json());
    } catch (err) {
      console.error(err);
    }
  };
  useEffect(() => {
    fetchData();
    const intervalID = setInterval(fetchData, POLL_INTERVAL);
    //stop timer once component is unmounted
    return () => clearInterval(intervalID);
  }, []);

  const transactionsHTML = transactions.map((tx) => (
    <div className="" key={tx.id}>
      <hr />
      <Transaction transaction={tx}></Transaction>
    </div>
  ));

  return (
    <div className="TransactionPool">
      <Link to="/">Home</Link>
      <hr />
      <h3>Transaction Pool</h3>
      <div className="">{transactionsHTML}</div>
      <hr />
      <Button variant="danger" onClick={mineBlock}>
        Mine a block of these transactions
      </Button>
    </div>
  );
}

export default TransactionPool;
