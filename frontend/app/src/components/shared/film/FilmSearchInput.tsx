import React from "react"
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition"
import { TextField, Box, InputAdornment, Button } from "@mui/material"
import MicIcon from "@mui/icons-material/Mic"
import SearchIcon from "@mui/icons-material/Search"
import { useAppDispatch, useAppSelector } from "../../../store"
import { searchFilm } from "../../../store/actionCreators"

export default function FilmSearchInput() {
  const dispatch = useAppDispatch()

  const isAuth = useAppSelector((state) => state.auth.isAuth)
  const userStatus = useAppSelector((state) => state.auth.status)

  const [inputValue, setInputValue] = React.useState<string | null>(null)
  const [useSmartSearch, setUseSmartSearch] = React.useState<boolean>(false)

  const { listening, browserSupportsSpeechRecognition, finalTranscript } = useSpeechRecognition({
    clearTranscriptOnListen: true,
  })

  React.useEffect(() => {
    if (!isAuth || userStatus !== "active") setUseSmartSearch(false)
  }, [isAuth])

  React.useEffect(() => setInputValue(finalTranscript), [finalTranscript])

  const fetchSearchFilm = async () => {
    if (inputValue) {
      dispatch(searchFilm(inputValue.trim(), useSmartSearch))
    }
  }

  return (
    <React.Fragment>
      <TextField
        helperText={
          useSmartSearch
            ? "Введите ваше описание. Например: криминальная драма с Домеником Торрето"
            : "Введите название фильма. Например: Форсаж 50: Самый последний заезд"
        }
        multiline
        fullWidth
        value={inputValue}
        onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
          setInputValue(event.target.value)
        }}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <Box onClick={() => fetchSearchFilm()}>
                <SearchIcon
                  sx={{
                    cursor: "pointer",
                  }}
                />
              </Box>
              {browserSupportsSpeechRecognition && (
                <Box
                  onClick={() =>
                    !listening
                      ? SpeechRecognition.startListening({ language: "ru" })
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
      {isAuth && userStatus === "active" && (
        <Button onClick={() => setUseSmartSearch(!useSmartSearch)}>
          {useSmartSearch ? "Disable smart search" : "Enable smart search"}
        </Button>
      )}
    </React.Fragment>
  )
}
