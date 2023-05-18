import React from "react";
import {Button, Container, Stack, TextField, Typography} from "@mui/material";
import {authSchema, AuthSchema} from "../helpers/validators"
import {Controller, useForm, useFormState} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import ky from "ky";
import Grid from "@mui/material/Unstable_Grid2";


export function Login() {

    const {handleSubmit, control} = useForm<AuthSchema>({
        resolver: zodResolver(authSchema)
    })
    const {errors} = useFormState({control})
    const onSubmit = (data: AuthSchema) => {
        console.log({json: data})
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
                            Log in
                        </Button>
                    </Stack>
                </form>
            </Container>
        </React.Fragment>
    );
};
