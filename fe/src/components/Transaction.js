function Transaction({ transaction }) {
  const { input, output } = transaction;
  const recipients = Object.keys(output);

  const receipients_html = recipients.map((recipient) => (
    <div className="" key={recipient}>
      To: {recipient} | Amount: {output[recipient]}
    </div>
  ));
  return (
    <div className="Transaction">
      <div className="">From {input.address}</div>
      {receipients_html}
    </div>
  );
}

export default Transaction;
