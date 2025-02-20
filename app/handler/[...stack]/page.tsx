import { StackHandler } from "@stackframe/stack";
import { stackServerApp } from "../../../stack";

export default function Handler(props: any) {
  console.log(props.params, props.searchParams);
  return <StackHandler fullPage app={stackServerApp} {...props} />;
}
