import * as React from "react"
import {Button, Skeleton, Stack, Typography} from "@mui/material";
import {useAppDispatch, useAppSelector} from "../store";
import {Navigate} from "react-router-dom";
import {logoutUser} from "../store/actionCreators";
import {selectIsLoggedIn} from "../store/authReducer";
import ArrowHeader from "../components/shared/Header/ArrowHeader";
import ProfileDataField from "../components/shared/Profile/ProfileDataField";

export default function Profile() {
    const dispatch = useAppDispatch()

    const isLoggedIn = useAppSelector(selectIsLoggedIn)
    const profile = useAppSelector(state => state.auth.profileData)
    const loadProfileStatus = useAppSelector(state => state.auth.profileData.status)
    const loginStatus = useAppSelector(state => state.auth.authData.status)
    const renderProfile = () =>
        (
            <React.Fragment>
                <ArrowHeader/>
                <Stack spacing={3} mt={5} useFlexGap>
                    {(loadProfileStatus === "loading" || loginStatus === 'loading') && <>
                        <Skeleton variant='text' sx={{fontSize: '4rem'}}/>
                        <Skeleton variant='text' sx={{fontSize: '2rem'}}/>
                        <Skeleton variant='text' sx={{fontSize: '2rem'}}/>
                        <Skeleton variant='text' sx={{fontSize: '2rem'}}/>
                        <Skeleton variant='text' sx={{fontSize: '2rem'}}/>
                    </>
                    }
                    {loadProfileStatus === "succeeded" && <>
                        <Typography variant='h3'>Welcome {profile.profile!.name}</Typography>
                        <Stack spacing={3} my={5} maxWidth={600} useFlexGap>
                            <ProfileDataField userDataName="Name" userDataValue={profile.profile!.name}/>
                            <ProfileDataField userDataName="Surname" userDataValue={profile.profile!.surname}/>
                            <ProfileDataField userDataName="Email" userDataValue={profile.profile!.email}/>
                            <ProfileDataField userDataName="Password" userDataValue="●●●●●●●●●●●●"/>
                            <Button sx={{maxWidth: 150}} variant="outlined" onClick={() => dispatch(logoutUser())}>Log out</Button>
                        </Stack>
                        <Typography variant='h4'>Favorite films</Typography>
                    </>
                    }
                </Stack>
            </React.Fragment>
        )
    return (
        <React.Fragment>
            {isLoggedIn ? renderProfile() : <Navigate to="/"/>}
        </React.Fragment>
    )
}
