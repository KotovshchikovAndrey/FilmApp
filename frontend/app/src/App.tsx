import * as React from "react"
import { POSTRE_URL } from "./core/config"
import FilmCardList from "./components/shared/film/FilmCardList"
import TestComponent from "./components/TestComponent"

function App() {
  console.log(POSTRE_URL)
  return (
    <React.Fragment>
      <FilmCardList />
      {/* <TestComponent /> */}
    </React.Fragment>
  )
}

export default App
