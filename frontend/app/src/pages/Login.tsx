import React, {FC, useContext, useState} from "react";
import {Alert, Button, Container, Stack, TextField, Typography} from "@mui/material";
import {loginSchema} from "../helpers/validators"
import {Controller, useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {Context} from "../index";
import {ILogin} from "../core/entities";

const defaultValues: ILogin = {
    email: "",
    password: "",
}


const Login: FC = () => {
    const {store} = useContext(Context)
    const {
        handleSubmit,
        formState: {errors},
        control,
    } = useForm({
        resolver: zodResolver(loginSchema),
        defaultValues: defaultValues
    })
    const onSubmit = async (data: ILogin) => {
        await store.login(data)
        setSubmitError(store.errors.loginError)
    }

    const [submitError, setSubmitError] = useState("")

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
                        {submitError !== "" &&
                            <Alert severity="error">{submitError}</Alert>}
                    </Stack>
                </form>
            </Container>
        </React.Fragment>
    );
};
export default Login