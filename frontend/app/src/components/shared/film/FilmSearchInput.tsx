import React from "react"
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition"
import { TextField, Box, InputAdornment } from "@mui/material"
import MicIcon from "@mui/icons-material/Mic"
import SearchIcon from "@mui/icons-material/Search"

export default function FilmSearchInput() {
  const [inputValue, setInputValue] = React.useState<string>("")
  const { listening, browserSupportsSpeechRecognition, finalTranscript } = useSpeechRecognition({
    clearTranscriptOnListen: true,
  })

  React.useEffect(() => setInputValue(finalTranscript), [finalTranscript])

  return (
    <React.Fragment>
      <TextField
        helperText="Введите ваше описание. Например: криминальная драма с Домеником Торрето"
        multiline
        rows={4}
        value={inputValue}
        onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
          setInputValue(event.target.value)
        }}
        InputProps={{
          endAdornment: (
            <InputAdornment position="start">
              <SearchIcon
                sx={{
                  marginRight: 1.2,
                  cursor: "pointer",
                }}
              />
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
        sx={{
          width: 900,
        }}
      />
    </React.Fragment>
  )
}
