import React, { useEffect, useRef } from "react";
import styles from "./index.module.css";
import ChatInput from "../ChatInput";
import ChatMessage from "../ChatMessage";
import useChat from "../../hooks/useChat";

function Chat() {
  const { messages } = useChat();
  return (
    <div className={styles.root}>
      <div className={styles.chat_list}>
        {messages.map((message, index) => (
          <ChatMessage key={index} data={message} />
        ))}
        <div className={styles.chat_end} />
      </div>
      <div className={styles.footer}>
        <ChatInput />
      </div>
    </div>
  );
}

export default Chat;
