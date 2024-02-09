import React from "react";
import styles from "./index.module.css";

type Props = React.HTMLAttributes<HTMLButtonElement>;
function Button(props: Props) {
  const { className = "", ...rest } = props;
  return <button {...rest} className={`${styles.button} ${className}`} />;
}

export default Button;
