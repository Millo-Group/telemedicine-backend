import React, {
  PropsWithChildren,
  createContext,
  useEffect,
  useState,
} from "react";
import { IJitsiMeetExternalApi } from "@jitsi/react-sdk/lib/types";
type ChatState = {
  api?: IJitsiMeetExternalApi;
  messages: Array<IncomingMessage | OutgoingMessage>;
  setMessage: (message: ChatState["messages"][0]) => void;
  sendMessage: (message: string, to?: string, ignorePrivacy?: boolean) => void;
  setApi: (api: IJitsiMeetExternalApi) => void;
};
const defaultMethod = () => {
  throw new Error("Not implemented");
};

export const ChatContext = createContext<ChatState>({
  messages: [],
  setMessage: defaultMethod,
  sendMessage: defaultMethod,
  setApi: defaultMethod,
});

function ChatProvider(props: PropsWithChildren) {
  const [messages, setMessages] = useState<
    Array<IncomingMessage | OutgoingMessage>
  >([]);
  const [api, setApi] = useState<IJitsiMeetExternalApi>();

  const setMessage = (message: IncomingMessage | OutgoingMessage) => {
    setMessages((messages) => [message, ...messages]);
  };

  const sendMessage = (message: string, to?: string, ignorePrivacy = false) => {
    api?.executeCommand("sendChatMessage", message, ignorePrivacy, to);
  };

  useEffect(() => {
    api?.addListener("incomingMessage", setMessage);
    api?.addListener("outgoingMessage", setMessage);
  }, [api]);

  return (
    <ChatContext.Provider
      value={{ messages, setMessage, sendMessage, setApi, api }}
    >
      {props.children}
    </ChatContext.Provider>
  );
}

export default ChatProvider;
