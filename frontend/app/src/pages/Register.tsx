import * as React from "react"
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Container,
  Stack,
  TextField,
  Typography,
} from "@mui/material"
import Grid from "@mui/material/Unstable_Grid2"
import { useForm, Controller } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { registerSchema } from "../helpers/validators"
import { FC } from "react"
import { IRegisterRequest } from "../core/entities"
import { useNavigate } from "react-router-dom"
import { useAppDispatch, useAppSelector } from "../store"
import { registerUser } from "../store/actionCreators"
import ArrowHeader from "../components/shared/Header/ArrowHeader"
import { authActions } from "../store/authReducer"

const Register: FC = () => {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()

  const isAuth = useAppSelector((state) => state.auth.isAuth)
  const isLoading = useAppSelector((state) => state.auth.loading)
  const errorMessage = useAppSelector((state) => state.auth.errorMessage)

  const {
    handleSubmit,
    formState: { errors },
    control,
  } = useForm<IRegisterRequest>({
    resolver: zodResolver(registerSchema),
  })

  const onSubmit = async (data: IRegisterRequest) => {
    dispatch(registerUser(data))
  }

  React.useEffect(() => {
    if (isAuth) navigate("/verify")

    // Сбрасываю сообщение об ошибке при каждом рендере
    dispatch(authActions.setErrorMessage(null))
  }, [isAuth])

  return (
    <React.Fragment>
      <ArrowHeader />
      <Container maxWidth="xs">
        <form onSubmit={handleSubmit(onSubmit)}>
          <Stack spacing={3} mt={10} useFlexGap>
            <Typography variant="h5">Sign up</Typography>
            <Grid container spacing={2}>
              <Grid xs={12} sm={6}>
                <Controller
                  control={control}
                  name="name"
                  render={({ field }) => (
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
                  render={({ field }) => (
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
              render={({ field }) => (
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
              render={({ field }) => (
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
            <Typography variant="body2">
              🍪 This site uses cookie. By continuing your browsing after being presented with the
              cookie information you consent to such use.
            </Typography>
            {errorMessage !== null && <Alert severity="error">{errorMessage}</Alert>}
            {isLoading && (
              <Box display="flex" justifyContent="center">
                <CircularProgress size={60} />
              </Box>
            )}
          </Stack>
        </form>
      </Container>
    </React.Fragment>
  )
}
export default Register

// const Register: FC = () => {
//   // const navigate = useNavigate()
//   // const dispatch = useAppDispatch()
//   // const authStatus = useAppSelector((state) => state.auth.authData.status)
//   // const loadProfileStatus = useAppSelector((state) => state.auth.profileData.status)
//   // const authError = useAppSelector((state) => state.auth.authData.error)
//   // const {
//   //   handleSubmit,
//   //   formState: { errors },
//   //   control,
//   // } = useForm<IRegisterRequest>({
//   //   resolver: zodResolver(registerSchema),
//   // })

//   // useEffect(() => {
//   //   if (authStatus === "succeeded" && loadProfileStatus === "succeeded") {
//   //     navigate("/")
//   //   }
//   // }, [authStatus, loadProfileStatus])

//   // const onSubmit = async (data: IRegisterRequest) => {
//   //   dispatch(registerUser(data))
//   // }

//   return (
//     <React.Fragment>
//       <ArrowHeader />
//       <Container maxWidth="xs">
//         <form onSubmit={handleSubmit(onSubmit)}>
//           <Stack spacing={3} mt={10} useFlexGap>
//             <Typography variant="h5">Sign up</Typography>
//             <Grid container spacing={2}>
//               <Grid xs={12} sm={6}>
//                 <Controller
//                   control={control}
//                   name="name"
//                   render={({ field }) => (
//                     <TextField
//                       variant="outlined"
//                       fullWidth
//                       id="name"
//                       label="Name"
//                       autoFocus
//                       error={!!errors.name?.message}
//                       helperText={errors.name?.message}
//                       {...field}
//                     />
//                   )}
//                 />
//               </Grid>
//               <Grid xs={12} sm={6}>
//                 <Controller
//                   control={control}
//                   name="surname"
//                   render={({ field }) => (
//                     <TextField
//                       variant="outlined"
//                       fullWidth
//                       id="surname"
//                       label="Surname"
//                       error={!!errors.surname?.message}
//                       helperText={errors.surname?.message}
//                       {...field}
//                     />
//                   )}
//                 />
//               </Grid>
//             </Grid>
//             <Controller
//               control={control}
//               name="email"
//               render={({ field }) => (
//                 <TextField
//                   variant="outlined"
//                   fullWidth
//                   id="email"
//                   label="Email Address"
//                   error={!!errors.email?.message}
//                   helperText={errors.email?.message}
//                   {...field}
//                 />
//               )}
//             />
//             <Controller
//               control={control}
//               name="password"
//               defaultValue=""
//               render={({ field }) => (
//                 <TextField
//                   variant="outlined"
//                   fullWidth
//                   id="password"
//                   label="Password"
//                   type="password"
//                   error={!!errors.password?.message}
//                   helperText={errors.password?.message}
//                   {...field}
//                 />
//               )}
//             />
//             <Button type="submit" variant="contained">
//               Sign up
//             </Button>
//             <Typography variant="body2">
//               🍪 This site uses cookie. By continuing your browsing after being presented with the
//               cookie information you consent to such use.
//             </Typography>
//             {authStatus === "failed" && <Alert severity="error">{authError}</Alert>}
//             {(authStatus === "loading" || loadProfileStatus === "loading") && (
//               <Box display="flex" justifyContent="center">
//                 <CircularProgress size={60} />
//               </Box>
//             )}
//           </Stack>
//         </form>
//       </Container>
//     </React.Fragment>
//   )
// }
// export default Register
