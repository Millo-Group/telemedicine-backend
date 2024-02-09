import React, { useEffect } from "react";
import Spinner from "../components/Spinner";
import Box from "../components/Box";
import useApi from "../hooks/useApi";
import { useNavigate, useSearchParams } from "react-router-dom";

type AuthPayload = {
  employee_id?: number;
  customer_id?: number;
  event_id: number;
};

function Authorization() {
  const api = useApi();
  const [searchParams] = useSearchParams();

  const navigate = useNavigate();

  const event_id = searchParams.get("event_id");
  const employee_id = searchParams.get("employee_id");
  const customer_id = searchParams.get("customer_id");

  const authUser = async (params: AuthPayload) => {
    try {
      const { data } = await api.post<{
        token: string;
        jitsi_jwt: string;
        room_name: string;
      }>("/authenticate", params);

      navigate(`/join/${data.room_name}`, {
        state: {
          jwt: data.jitsi_jwt,
        },
      });

      localStorage.setItem("token", data.token);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    if (event_id != null && (employee_id != null || customer_id != null)) {
      authUser({
        event_id: parseInt(event_id),
        employee_id: employee_id ? parseInt(employee_id) : undefined,
        customer_id: customer_id ? parseInt(customer_id) : undefined,
      });
    } else {
      navigate("/");
    }
  }, []);

  return (
    <Box
      display="flex"
      alignItems="center"
      justifyContent="center"
      width="100vw"
      height="100vh"
      flexDirection="column"
    >
      <h5>Please wait a moment we'll navigate to meeting shortly</h5>
      <Spinner />
    </Box>
  );
}

export default Authorization;
