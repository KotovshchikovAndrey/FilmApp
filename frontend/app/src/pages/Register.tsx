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
import * as zod from "zod";

const registerSchema = zod.object({
    email: zod.string().email("Invalid email address"),
    password: zod.string().min(8, "Must be 8 or more characters long").max(32, "Must be 32 or fewer characters long"),
    name: zod.string().max(30, "Must be 30 or fewer characters long"),
    surname: zod.string().max(30, "Must be 30 or fewer characters long"),
});
type IRegisterSchema = zod.infer<typeof registerSchema>

export function Register() {

    const {handleSubmit, control} = useForm<IRegisterSchema>({
        resolver: zodResolver(registerSchema)
    })
    const {errors} = useFormState({control})
    const onSubmit = (data: IRegisterSchema) => {
        console.log(data)
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
