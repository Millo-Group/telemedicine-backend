import React, { useEffect } from "react";
import Meeting from "../components/Meeting";
import { Navigate, useLocation, useParams } from "react-router-dom";

function Join() {
  const { room = "" } = useParams();
  const { state } = useLocation();

  if (!state) return <Navigate to="/" />;

  return <Meeting roomName={room} jwt={state.jwt} />;
}

export default Join;
