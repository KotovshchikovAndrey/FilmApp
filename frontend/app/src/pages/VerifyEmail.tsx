import {verificationSchema, VerificationSchema} from "../helpers/validators"
import {Controller, useForm, useFormState} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {Button, Container, Stack, TextField, Typography} from "@mui/material";
import React from "react";

export function VerifyEmail() {
    const {handleSubmit, control} = useForm<VerificationSchema>({
        resolver: zodResolver(verificationSchema)
    })
    const {errors} = useFormState({control})
    const onSubmit = (data: VerificationSchema) => {
        console.log({json: data})
    }

    return (
        <React.Fragment>
            <Container maxWidth="xs">
                <form onSubmit={handleSubmit(onSubmit)}>
                    <Stack spacing={3} mt={10}>
                        <Typography variant="h5">
                            Enter verification code
                        </Typography>
                        <Typography>
                            A verification code has been sent to {}.<br/>
                            Please enter it to verify your email
                        </Typography>
                        <Controller
                            control={control}
                            name="verificationCode"
                            render={({field}) => (
                                <TextField
                                    variant="outlined"
                                    fullWidth
                                    id="verificationCode"
                                    label="Verification code"
                                    name="verificationCode"
                                    onChange={(e) => field.onChange(e)}
                                    value={field.value}
                                    error={!!errors.verificationCode?.message}
                                    helperText={errors.verificationCode?.message}
                                />
                            )}
                        />
                        <Button
                            type="submit"
                            variant="contained"
                        >
                            Verify
                        </Button>
                    </Stack>
                </form>
            </Container>
        </React.Fragment>
    )
}

