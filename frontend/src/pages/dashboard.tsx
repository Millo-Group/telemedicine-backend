import React from "react";
import Box from "../components/Box";
import Button from "../components/Button";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigation = useNavigate();
  return (
    <Box
      display="flex"
      alignItems="center"
      flexDirection="row"
      columnGap="20px"
      height="100vh"
      width="100vw"
      justifyContent="center"
    >
      <Button
        onClick={() => navigation("/authenticate?customer_id=30&event_id=10")}
      >
        Join as Customer
      </Button>
      <Button
        onClick={() => navigation("/authenticate?employee_id=23&event_id=10")}
      >
        Join as Employee
      </Button>
    </Box>
  );
}

export default Dashboard;
