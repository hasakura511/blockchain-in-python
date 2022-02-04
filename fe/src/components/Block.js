import { useState } from "react";
import { Button } from "react-bootstrap";
import { MILLISECONDS_PY } from "../config";
import Transaction from "./Transaction";

function ToggleTransactionDisplay({ block }) {
  const { data } = block;
  const [showTransactions, setShowTransactions] = useState(false);
  const toggleShowTransaction = () => {
    setShowTransactions(!showTransactions);
  };

  const data_html = data.map((transaction) => (
    <div className="" key={transaction.id}>
      <hr />
      <Transaction transaction={transaction} />
    </div>
  ));

  if (showTransactions) {
    return (
      <div className="Block">
        <div className="">
          <Button
            variant="danger"
            size="sm"
            onClick={() => {
              setShowTransactions(false);
            }}
          >
            Hide Transaction
          </Button>
        </div>
        <div className="">{data_html}</div>
      </div>
    );
  }

  return (
    <div className="">
      <br />
      <Button variant="danger" size="sm" onClick={toggleShowTransaction}>
        Show more
      </Button>
    </div>
  );
}

function Block({ block }) {
  const { timestamp, hash } = block;
  const hashDisplay = `${hash.substring(0, 15)}...${hash.substring(
    hash.length - 15
  )}`;
  const timestampDisplay = new Date(
    timestamp / MILLISECONDS_PY
  ).toLocaleString();

  return (
    <div className="Block">
      <div className="">Hash: {hashDisplay}</div>
      <div className="">Timestamp: {timestampDisplay}</div>
      <ToggleTransactionDisplay block={block} />
    </div>
  );
}

export default Block;
