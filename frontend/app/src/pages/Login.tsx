import React, {FC, useContext, useEffect, useState} from "react";
import {Alert, Box, Button, CircularProgress, Container, Skeleton, Stack, TextField, Typography} from "@mui/material";
import {loginSchema} from "../helpers/validators"
import {Controller, useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {ILoginRequest} from "../core/entities";
import {loginUser} from "../store/actionCreators";
import {IRootState, store, useAppDispatch, useAppSelector} from "../store";
import {useNavigate, redirect} from "react-router-dom";
import {useSelector} from "react-redux";


const Login: FC = () => {
    const navigate = useNavigate()
    const dispatch = useAppDispatch()
    const loginStatus = useAppSelector(state => state.auth.authData.status)
    const loadProfileStatus = useAppSelector(state => state.auth.profileData.status)
    const loginError = useAppSelector(state => state.auth.authData.error)
    const {
        handleSubmit,
        formState: {errors},
        control,
    } = useForm<ILoginRequest>({
        resolver: zodResolver(loginSchema),
        defaultValues: {
            email: "",
            password: ""
        }
    })
    useEffect(() => {
        if (loginStatus === 'succeeded' && loadProfileStatus === 'succeeded') {
            navigate('/')
        }
    }, [loginStatus, loadProfileStatus])
    const onSubmit = (data: ILoginRequest) => {
        dispatch(loginUser(data))
    }
    return (
        <React.Fragment>
            <Container maxWidth="xs">
                <form onSubmit={handleSubmit(onSubmit)}>
                    <Stack spacing={3} mt={10} useFlexGap>
                        <Typography variant="h5">Log in</Typography>
                        <Controller
                            control={control}
                            name="email"
                            render={({field}) => (
                                <TextField
                                    autoFocus
                                    variant="outlined"
                                    fullWidth
                                    id="email"
                                    label="Email Address"
                                    error={!!errors.email?.message}
                                    helperText={errors.email?.message}
                                    {...field}
                                />
                            )}

                        />
                        <Controller
                            control={control}
                            name="password"
                            render={({field}) => (
                                <TextField
                                    variant="outlined"
                                    fullWidth
                                    id="password"
                                    label="Password"
                                    type="password"
                                    error={!!errors.password?.message}
                                    helperText={errors.password?.message}
                                    {...field}
                                />
                            )}
                        />
                        <Button type="submit" variant="contained">
                            Log in
                        </Button>
                        {loginStatus === 'failed' &&
                            <Alert severity="error">{loginError}</Alert>}
                        {(loginStatus === 'loading' || loadProfileStatus === 'loading') &&
                            <Box display='flex' justifyContent="center"><CircularProgress size={60}/></Box>}
                    </Stack>
                </form>
            </Container>
        </React.Fragment>
    );
};
export default Login