import * as React from "react"
import Home from "./pages/Home"
import FilmDetail from "./pages/FilmDetail"
import {createBrowserRouter, RouterProvider} from "react-router-dom"
import {Register} from "./pages/Register";
import {Login} from "./pages/Login";
import {VerifyEmail} from "./pages/VerifyEmail";

const router = createBrowserRouter([
    {
        path: "/",
        element: <Home/>,
    },
    {
        path: "/:filmId",
        element: <FilmDetail/>,
    },
    {
        path: "/register",
        element: <Register/>,
    },
    {
        path: "/login",
        element: <Login/>,
    },
    {
        path: "/verify",
        element: <VerifyEmail/>,
    },
])

function App() {
    return (
        <React.Fragment>
            <RouterProvider router={router}/>
            {/* <FilmDetail /> */}
        </React.Fragment>
    )
}

export default App
