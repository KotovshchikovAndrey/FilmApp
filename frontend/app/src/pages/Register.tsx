import * as React from "react"
import {
    Alert,
    Button,
    Container,
    Stack,
    TextField,
    Typography
} from "@mui/material";
import Grid from "@mui/material/Unstable_Grid2";
import {useForm, Controller} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {registerSchema} from "../helpers/validators"
import {Link} from "react-router-dom";
import {FC, useContext, useState} from "react";
import {IRegistration} from "../core/entities";
import {Context} from "../index";


const defaultValues: IRegistration = {
    name: "",
    surname: "",
    email: "",
    password: "",
}

const Register: FC = () => {
    const {store} = useContext(Context)
    const {
        handleSubmit,
        formState: {errors},
        control,
    } = useForm<IRegistration>({
        resolver: zodResolver(registerSchema),
        defaultValues: defaultValues,
    })
    const onSubmit = async (data: IRegistration) => {
        await store.register(data)
        setSubmitError(store.errors.registerError)
    }
    const [submitError, setSubmitError] = useState("")

    return (
        <React.Fragment>
            <Container maxWidth="xs">
                <form onSubmit={handleSubmit(onSubmit)}>
                    <Stack spacing={3} mt={10} useFlexGap>
                        <Typography variant="h5">Sign up</Typography>
                        <Grid container spacing={2}>
                            <Grid xs={12} sm={6}>
                                <Controller
                                    control={control}
                                    name="name"
                                    render={({field}) => (
                                        <TextField
                                            variant="outlined"
                                            fullWidth
                                            id="name"
                                            label="Name"
                                            autoFocus
                                            error={!!errors.name?.message}
                                            helperText={errors.name?.message}
                                            {...field}
                                        />
                                    )}
                                />
                            </Grid>
                            <Grid xs={12} sm={6}>
                                <Controller
                                    control={control}
                                    name="surname"
                                    render={({field}) => (
                                        <TextField
                                            variant="outlined"
                                            fullWidth
                                            id="surname"
                                            label="Surname"
                                            error={!!errors.surname?.message}
                                            helperText={errors.surname?.message}
                                            {...field}
                                        />
                                    )}
                                />
                            </Grid>
                        </Grid>
                        <Controller
                            control={control}
                            name="email"
                            render={({field}) => (
                                <TextField
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
                            defaultValue=""
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
                            Sign up
                        </Button>
                        <Typography variant="body2">🍪 This site uses cookie. By continuing your browsing after being presented with the
                            cookie information you consent to such use.</Typography>
                        {submitError !== "" &&
                        <Alert severity="error">{submitError}</Alert>}
                    </Stack>
                </form>
            </Container>
        </React.Fragment>
    )
}
export default Register