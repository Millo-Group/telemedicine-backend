import { JaaSMeeting } from "@jitsi/react-sdk";
import { useNavigate } from "react-router";
import styles from "./index.module.css";
import Chat from "../Chat";
import useChat from "../../hooks/useChat";

type Props = {
  jwt: string;
  roomName: string;
};

function Meeting(props: Props) {
  const navigate = useNavigate();
  const { setApi } = useChat();

  const readyToClose = () => {
    navigate("/");
  };
  const toolbarButtons = [
    "camera",
    //  'chat',
    "closedcaptions",
    "desktop",
    "download",
    "embedmeeting",
    "etherpad",
    "feedback",
    "filmstrip",
    "fullscreen",
    "hangup",
    "help",
    "highlight",
    "invite",
    "linktosalesforce",
    "livestreaming",
    "microphone",
    "noisesuppression",
    "participants-pane",
    "profile",
    "raisehand",
    "recording",
    "security",
    "select-background",
    "settings",
    "shareaudio",
    "sharedvideo",
    "shortcuts",
    "stats",
    "tileview",
    "toggle-camera",
    "videoquality",
    "whiteboard",
  ];
  // return <JitsiMeeting domain="localhost:8000" roomName="tessdfsdfgd" />;

  return (
    <div className={styles.root}>
      <JaaSMeeting
        appId="vpaas-magic-cookie-2245ac56e2d94efe9ab7ef727989f4b1"
        onApiReady={(api) => {
          setApi(api);
          api.addListener("readyToClose", readyToClose);
        }}
        interfaceConfigOverwrite={{
          TOOLBAR_BUTTONS: toolbarButtons,
        }}
        configOverwrite={{
          startWithVideoMuted: true,
          startWithAudioMuted: true,
          prejoinPageEnabled: false,
          enableRecording: true,
        }}
        getIFrameRef={(iframeRef) => {
          iframeRef.style.height = "100vh";
        }}
        {...props}
      />
      <div className={styles.chat}>
        <Chat />
      </div>
    </div>
  );
}

export default Meeting;
