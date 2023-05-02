import * as React from "react"
import { POSTER_URL } from "./core/config"
import Home from "./pages/Home"

function App() {
  console.log(POSTER_URL)
  return (
    <React.Fragment>
      <Home />
    </React.Fragment>
  )
}

export default App
