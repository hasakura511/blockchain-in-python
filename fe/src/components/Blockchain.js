import { useState, useEffect } from "react";
import { Button } from "react-bootstrap";
import { API_BASE_URL } from "../config";
import Block from "./Block";

const PAGE_RANGE = 3;

function Blockchain() {
  const [blockchain, setBlockchain] = useState([]);
  const [blockchainLength, setBlockchainLength] = useState(0);

  const fetchBlockchainPage = async ({ start, end }) => {
    const bc_page = await fetch(
      `${API_BASE_URL}/bc/range?start=${start}&end=${end}`
    );
    const bc_page_json = await bc_page.json();
    setBlockchain(bc_page_json);
  };

  useEffect(() => {
    const fetchData = async () => {
      fetchBlockchainPage({ start: 0, end: PAGE_RANGE });
      // const bc_data = await fetch(`${API_BASE_URL}/bc`);
      // setBlockchain(await bc_data.json());

      const bc_length = await fetch(`${API_BASE_URL}/bc/length`);
      setBlockchainLength(await bc_length.json());
    };
    fetchData().catch(console.error);
  }, []);
  // console.log(blockchainLength);
  // console.log(blockchain);
  const blockchain_html = blockchain.map((block) => (
    <Block key={block.hash} block={block}></Block>
  ));

  const buttonNumbers = [];
  for (let i = 0; i < blockchainLength / PAGE_RANGE; i++) {
    buttonNumbers.push(i);
  }

  const page_buttons = buttonNumbers.map((number) => {
    const start = number * PAGE_RANGE;
    const end = (number + 1) * PAGE_RANGE;

    return (
      <span key={number} onClick={() => fetchBlockchainPage({ start, end })}>
        <Button size="sm" variant="danger">
          {number + 1}
        </Button>
      </span>
    );
  });

  return (
    <div className="Blockchain">
      <h3>Blockchain</h3>
      <div className="">{blockchain_html}</div>
      <div className="">{page_buttons}</div>
    </div>
  );
}

export default Blockchain;
