import React, {useState} from "react"
import SpeechRecognition, {useSpeechRecognition} from "react-speech-recognition"
import {
  TextField,
  Box,
  InputAdornment,
  Button,
  ButtonGroup,
  ToggleButtonGroup,
  ToggleButton,
  Container, Stack
} from "@mui/material"
import MicIcon from "@mui/icons-material/Mic"
import SearchIcon from "@mui/icons-material/Search"
import {useAppDispatch, useAppSelector} from "../../../store"
import {searchFilm} from "../../../store/actionCreators"
import FilmCardList from "./FilmCardList";
import Grid2 from "@mui/material/Unstable_Grid2";
import Grid from "@mui/material/Unstable_Grid2";

export default function FilmSearchInput() {
  const dispatch = useAppDispatch()

  const isAuth = useAppSelector((state) => state.auth.isAuth)
  const userStatus = useAppSelector((state) => state.auth.status)

  const [inputValue, setInputValue] = useState<string | null>(null)
  const [isUsingSmartSearch, setIsUsingSmartSearch] = useState<boolean>(false)

  const {listening, browserSupportsSpeechRecognition, finalTranscript} = useSpeechRecognition({
    clearTranscriptOnListen: true,
  })

  React.useEffect(() => {
    if (!isAuth || userStatus !== "active") setIsUsingSmartSearch(false)
  }, [isAuth])

  React.useEffect(() => setInputValue(finalTranscript), [finalTranscript])

  const fetchSearchFilm = async () => {
    if (inputValue) {
      dispatch(searchFilm(inputValue.trim(), isUsingSmartSearch))
      setInputValue("")
    }
  }

  const handleSearchToggle = (
    event: React.MouseEvent<HTMLElement>,
    newToggle: boolean,
  ) => {
    if (newToggle !== null) {
      setIsUsingSmartSearch(newToggle);
    }
  }


  return (
    <React.Fragment>

        {isAuth && userStatus === "active" && (
          <Box alignSelf="center">
          <ToggleButtonGroup
            value={isUsingSmartSearch}
            exclusive
            color="primary"
            onChange={handleSearchToggle}>
            <ToggleButton value={true}>
              Smart search
            </ToggleButton>
            <ToggleButton value={false}>
              Default search
            </ToggleButton>
          </ToggleButtonGroup>
          </Box>)}
      <Grid container spacing={1}>
        <Grid xs={12} sm={10}>
          <TextField
            fullWidth
            value={inputValue}
            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
              setInputValue(event.target.value)
            }}
            helperText={
              isUsingSmartSearch
                ? "Write some description of the film and we will try to find it"
                : "Search film by title"
            }
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  {browserSupportsSpeechRecognition && (
                    <Box
                      onClick={() =>
                        !listening
                          ? SpeechRecognition.startListening({language: "en"})
                          : SpeechRecognition.stopListening()
                      }
                    >
                      <MicIcon
                        sx={{
                          color: listening ? "red" : "black",
                          cursor: "pointer",
                        }}
                      />
                    </Box>
                  )}
                </InputAdornment>
              ),
            }}
          />
        </Grid>
        <Grid xs={12} sm={2}>
          <Button variant="contained" startIcon={<SearchIcon/>} onClick={() => fetchSearchFilm()} size="large"
                  sx={{width: "100%", height: 56}}>
            Search
          </Button>
        </Grid>
      </Grid>

    </React.Fragment>
  )
}
