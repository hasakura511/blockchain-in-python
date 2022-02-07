import { useState, useEffect } from "react";
import { FormGroup, FormControl, Button } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";

import { API_BASE_URL } from "../config";

function ConductTransaction() {
  const navigate = useNavigate();
  const [amount, setAmount] = useState(0);
  const [recipient, setRecipient] = useState("");
  const [knownAddresses, setKnownAddresses] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetch(`${API_BASE_URL}/bc/known-addresses`);
      setKnownAddresses(await data.json());
    };
    fetchData().catch(console.error);
  }, []);

  const knownAddressesHTML = knownAddresses.map((address, i) => (
    <span key={address} onClick={() => setRecipient(address)}>
      <u>{address}</u>
      {i !== knownAddresses.length - 1 ? ", " : ""}
    </span>
  ));

  const updateRecipient = (e) => {
    setRecipient(e.target.value);
  };

  const updateAmount = (e) => {
    setAmount(Number(e.target.value));
  };

  const submitTransaction = async (e) => {
    const res = await fetch(`${API_BASE_URL}/wallet/transact`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ recipient, amount }),
    });
    const res_json = await res.json();
    console.log(JSON.stringify({ recipient, amount }));
    console.log(res_json);
    navigate("/transaction-pool");
  };

  return (
    <div className="ConductTransaction">
      <Link to="/">Home</Link>
      <hr />
      <h3>Conduct a transaction</h3>
      <br />
      <FormGroup>
        <FormControl
          input="text"
          placeholder="recipient"
          value={recipient}
          onChange={updateRecipient}
        />
      </FormGroup>
      <FormGroup>
        <FormControl
          input="number"
          placeholder="amount"
          value={amount}
          onChange={updateAmount}
        />
      </FormGroup>
      <div className="">
        <Button variant="danger" onClick={submitTransaction}>
          Submit
        </Button>
      </div>
      <br />
      <h3>Known Addresses</h3>
      <div className="">{knownAddressesHTML}</div>
    </div>
  );
}

export default ConductTransaction;
