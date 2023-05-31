import * as React from "react"
import {Button, Typography} from "@mui/material";
import {IRootState, useAppDispatch, useAppSelector} from "../store";
import {Navigate} from "react-router-dom";
import {getMyProfile, logoutUser} from "../store/actionCreators";
import {selectIsLoggedIn} from "../store/authReducer";

export default function Profile() {
    const dispatch = useAppDispatch()

    const isLoggedIn = useAppSelector(selectIsLoggedIn)
    const profile = useAppSelector(state => state.auth.profileData)
    const renderProfile = () =>
        (
            <React.Fragment>
                <Typography>Welcome {profile.profile?.name}</Typography>
                <Button variant="outlined" onClick={() => dispatch(logoutUser())}>Log out</Button>
                <Button variant="outlined" onClick={() => dispatch(getMyProfile())}>UpdateProfile</Button>
            </React.Fragment>
        )
    return (
        <React.Fragment>
            {isLoggedIn ? renderProfile() : <Navigate to="/"/>}
        </React.Fragment>
    )
}
