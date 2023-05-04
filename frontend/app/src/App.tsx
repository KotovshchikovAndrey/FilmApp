import * as React from "react"
import Home from "./pages/Home"
import FilmDetail from "./pages/FilmDetail"
import { createBrowserRouter, RouterProvider } from "react-router-dom"

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/:filmId",
    element: <FilmDetail />,
  },
])

function App() {
  return (
    <React.Fragment>
      <RouterProvider router={router} />
      {/* <FilmDetail /> */}
    </React.Fragment>
  )
}

export default App
