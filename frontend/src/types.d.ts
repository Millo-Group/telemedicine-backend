interface OutgoingMessage {
  message: string;
  privateMessage: boolean;
}

interface IncomingMessage extends OutgoingMessage {
  from: string;
  nick: string;
}
