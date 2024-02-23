import React from "react";
import styles from "./index.module.css";
import clsx from "clsx";

type Props = React.HTMLAttributes<HTMLButtonElement> & { variant?: "primary" };
function IconButton(props: Props) {
  const { className = "", variant = "", ...rest } = props;
  return (
    <button
      {...rest}
      className={clsx(styles.button, className, styles[variant])}
    />
  );
}

export default IconButton;
