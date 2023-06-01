import * as React from "react"
import Home from "./pages/Home"
import FilmDetail from "./pages/FilmDetail"
import Login from "./pages/Login";
import {createBrowserRouter, RouterProvider} from "react-router-dom"
import Register from "./pages/Register";
import {VerifyEmail} from "./pages/VerifyEmail";
import Root from "./pages/Root";
import Error from "./pages/Error";
import {useAppDispatch, useAppSelector} from "./store";
import Profile from "./pages/Profile";
import {selectIsLoggedIn} from "./store/authReducer";
import {useEffect} from "react";
import {refreshToken} from "./store/actionCreators";

const router = createBrowserRouter([
    {
        path: "/",
        element: <Root/>,
        errorElement: <Error/>,
        children: [
            {
                path: "",
                element: <Home/>,
            },
            {
                path: "/film/:id",
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
            {
                path: "/profile",
                element: <Profile/>,
            },
        ],
    },
])

function App() {
    const dispatch = useAppDispatch()
    const isLoggedIn = useAppSelector(selectIsLoggedIn)
    useEffect(() => {
        if (isLoggedIn) {
            dispatch(refreshToken())
        }
    }, [])
    return (
        <React.Fragment>
            <RouterProvider router={router}/>
        </React.Fragment>
    )
}

export default App
