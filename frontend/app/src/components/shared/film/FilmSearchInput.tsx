import React from "react"
import SpeechRecognition, {useSpeechRecognition} from "react-speech-recognition"
import {TextField, Box, InputAdornment} from "@mui/material"
import MicIcon from "@mui/icons-material/Mic"
import SearchIcon from "@mui/icons-material/Search"

import {IFilm} from "../../../core/entities"
import api from "../../../api"
import {title} from "process"

export default function FilmSearchInput() {
    const [searchResult, setSearchResult] = React.useState<IFilm | null>(null)

    const [inputValue, setInputValue] = React.useState<string>("")
    const {listening, browserSupportsSpeechRecognition, finalTranscript} = useSpeechRecognition({
        clearTranscriptOnListen: true,
    })

    React.useEffect(() => setInputValue(finalTranscript), [finalTranscript])

    const fetchSearchFilm = async () => {
        if (inputValue) {
            const response = await api.films.searchFilmSmart(inputValue)
            setSearchResult(response.data)
        }
    }

    return (
        <React.Fragment>
            <TextField
                helperText="Введите ваше описание. Например: криминальная драма с Домеником Торрето"
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
                                            ? SpeechRecognition.startListening({language: "ru"})
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
        </React.Fragment>
    )
}
