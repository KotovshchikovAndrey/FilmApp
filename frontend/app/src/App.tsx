import * as React from "react"
import Home from "./pages/Home"
import FilmDetail from "./pages/FilmDetail"
import Login from "./pages/Login"
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import Register from "./pages/Register"
import { VerifyEmail } from "./pages/VerifyEmail"
import Root from "./pages/Root"
import Error from "./pages/Error"
import { useAppDispatch, useAppSelector } from "./store"
import Profile from "./pages/Profile"
import { useEffect } from "react"
import { authenticateUser, fetchFilms } from "./store/actionCreators"
import Cookies from "js-cookie"

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <Error />,
    children: [
      {
        path: "",
        element: <Home />,
      },
      {
        path: "/film/:id",
        element: <FilmDetail />,
      },
      {
        path: "/register",
        element: <Register />,
      },
      {
        path: "/login",
        element: <Login />,
      },
      {
        path: "/verify",
        element: <VerifyEmail />,
      },
      {
        path: "/profile",
        element: <Profile />,
      },
    ],
  },
])

function App() {
  const dispatch = useAppDispatch()
  const isAuth = useAppSelector((state) => state.auth.isAuth)
  const user = useAppSelector((state) => state.auth.user)
  const filter = useAppSelector((state) => state.film.filter)

  useEffect(() => {
    if (user) return

    const token = localStorage.getItem("token")
    if (token) dispatch(authenticateUser())
  }, [isAuth])

  useEffect(() => {
    dispatch(
      fetchFilms({ limit: 20, genreId: filter.genre?.id, countryIso: filter.country?.iso_3166_1 })
    )
  }, [filter])

  return (
    <React.Fragment>
      <RouterProvider router={router} />
    </React.Fragment>
  )
}

export default App
