import React from "react"

export default function Test() {
  const [counter, setCounter] = React.useState<number>(0)
  return (
    <React.Fragment>
      {counter}
      <div onClick={() => setCounter((prevState: number) => prevState + 1)}>test</div>
    </React.Fragment>
  )
}
