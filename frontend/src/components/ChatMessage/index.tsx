import React from "react";
import styles from "./index.module.css";
import clsx from "clsx";

type Props = {
  data: IncomingMessage | OutgoingMessage;
};

function isIncomingMessage(object: any): object is IncomingMessage {
  return "from" in object;
}

function ChatMessage(props: Props) {
  const { data } = props;

  const message = data.message;

  const isIncoming = isIncomingMessage(data);

  const className = clsx({
    [styles.root]: true,
    [isIncoming ? styles.incoming : styles.outgoing]: true,
  });

  return (
    <div className={className}>
      <div>{message}</div>
    </div>
  );
}

export default ChatMessage;
