import * as React from "react"
import * as ReactDOM from "react-dom/client"
import "./index.css"
import App from "./App"
import Store from "./store/Store";
import {createContext} from "react";

const store = new Store()
export const Context = createContext({store})

const root = ReactDOM.createRoot(document.getElementById("root") as HTMLElement)
root.render(
  <React.StrictMode>
      <Context.Provider value={{store}}>
          <App />
      </Context.Provider>
  </React.StrictMode>
)
