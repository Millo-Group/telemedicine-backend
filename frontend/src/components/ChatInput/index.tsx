import React, { useState } from "react";
import styles from "./index.module.css";
import IconButton from "../IconButton";
import { ReactComponent as AttachmentIcon } from "../../assets/attachment.svg";
import { ReactComponent as MicIcon } from "../../assets/mic.svg";
import useChat from "../../hooks/useChat";

function ChatInput() {
  const { sendMessage } = useChat();
  const [message, setMessage] = useState("");

  const handleSendMessage = () => {
    sendMessage(message);
    setMessage("");
  };

  return (
    <div className={styles.root}>
      <IconButton>
        <AttachmentIcon />
      </IconButton>
      <textarea
        onChange={(e) => setMessage(e.target.value)}
        value={message}
        className={styles.input}
        placeholder="Type"
        rows={3}
      ></textarea>
      <IconButton variant="primary" onClick={handleSendMessage}>
        <MicIcon />
      </IconButton>
    </div>
  );
}

export default ChatInput;
