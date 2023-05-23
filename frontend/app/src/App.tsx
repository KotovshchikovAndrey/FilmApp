import * as React from "react"
import Home from "./pages/Home"
import FilmDetail from "./pages/FilmDetail"
import Login from "./pages/Login";
import {createBrowserRouter, RouterProvider} from "react-router-dom"
import Register from "./pages/Register";
import {VerifyEmail} from "./pages/VerifyEmail";
import {useContext, useEffect} from "react";
import {Context} from "./index";

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
    const {store} = useContext(Context)
    useEffect(() => {
        if (localStorage.getItem('access_token')) {
            store.checkAuth()
        }
    }, [])
    return (
        <React.Fragment>
            <RouterProvider router={router}/>
            {/* <FilmDetail /> */}
        </React.Fragment>
    )
}

export default App
