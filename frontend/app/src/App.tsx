import * as React from "react"
import { POSTRE_URL } from "./core/config"
import TestComponent from "./components/TestComponent"

function App() {
  console.log(POSTRE_URL)
  return (
      <>
          <div className="App">123</div>
          <TestComponent />
      </>
  )
}

export default App
