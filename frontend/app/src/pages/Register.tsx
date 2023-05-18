import * as React from "react"
import {
    Button,
    Container,
    Stack,
    TextField,
    Typography
} from "@mui/material";
import Grid from "@mui/material/Unstable_Grid2";
import {useForm, Controller, useFormState} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {authSchema, AuthSchema} from "../helpers/validators"
import ky from "ky";


export function Register() {

    const {handleSubmit, control} = useForm<AuthSchema>({
        resolver: zodResolver(authSchema)
    })
    const {errors} = useFormState({control})
    const onSubmit = async (data: AuthSchema) => {
        console.log({json: data})
        const json = await ky.post("https://127.0.0.1:8000/auth/register", {json: data}).json();
        console.log(json)
    }

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
                                            name="name"
                                            variant="outlined"
                                            fullWidth
                                            id="name"
                                            label="Name"
                                            autoFocus
                                            onChange={(e) => field.onChange(e)}
                                            value={field.value}
                                            error={!!errors.name?.message}
                                            helperText={errors.name?.message}
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
                                            name="surname"
                                            onChange={(e) => field.onChange(e)}
                                            value={field.value}
                                            error={!!errors.surname?.message}
                                            helperText={errors.surname?.message}
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
                                    name="email"
                                    onChange={(e) => field.onChange(e)}
                                    value={field.value}
                                    error={!!errors.email?.message}
                                    helperText={errors.email?.message}
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
                                    name="password"
                                    type="password"
                                    onChange={(e) => field.onChange(e)}
                                    value={field.value}
                                    error={!!errors.password?.message}
                                    helperText={errors.password?.message}
                                />
                            )}
                        />
                        <Button
                            type="submit"
                            variant="contained"
                        >
                            Sign up
                        </Button>
                    </Stack>
                </form>
            </Container>
        </React.Fragment>
    )
}
