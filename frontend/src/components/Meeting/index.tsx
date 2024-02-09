import { JaaSMeeting, JitsiMeeting } from "@jitsi/react-sdk";
import { IJitsiMeetExternalApi } from "@jitsi/react-sdk/lib/types";
import { useEffect, useRef } from "react";
import { useNavigate } from "react-router";

type Props = {
  jwt: string;
  roomName: string;
};

function Meeting(props: Props) {
  const apiRef = useRef<IJitsiMeetExternalApi>();
  const navigate = useNavigate();

  useEffect(() => {
    const api = apiRef.current;
    return () => {
      api?.removeListener("readyToClose", () => {
        navigate("/");
      });
    };
  }, [apiRef.current]);

  // return <JitsiMeeting domain="localhost:8000" roomName="tessdfsdfgd" />;

  return (
    <JaaSMeeting
      appId="vpaas-magic-cookie-2245ac56e2d94efe9ab7ef727989f4b1"
      onApiReady={(api) => {
        apiRef.current = api;
        api.addListener("readyToClose", () => {
          navigate("/");
        });
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
  );
}

export default Meeting;
