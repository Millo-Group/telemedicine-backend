import React, { PropsWithChildren } from "react";

function Box(
  props: PropsWithChildren &
    React.HTMLAttributes<HTMLDivElement>["style"] & { className?: string }
) {
  const { children, className, ...style } = props;
  return (
    <div style={style} className={className}>
      {children}
    </div>
  );
}

export default Box;
