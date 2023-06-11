import React from "react"
import { FilmComment } from "./FilmComment"
import { useAppSelector, useAppDispatch } from "../../../store"
import { ICommentAuthor, IUser } from "../../../core/entities"
import { Avatar, Box, Button, CircularProgress, Stack, TextField } from "@mui/material"
import { addChildFilmComment, addFilmComment, getFilmComments } from "../../../store/actionCreators"
import { API_URL } from "../../../core/config"

interface IAddAnswerFilmCommentProps {
  filmId: number
  parentComment: {
    id: number
    author: ICommentAuthor
  }
}

export const AddAnswerFilmComment: React.FC<IAddAnswerFilmCommentProps> = (
  props: IAddAnswerFilmCommentProps
) => {
  const dispatch = useAppDispatch()

  const isAuth = useAppSelector((state) => state.auth.isAuth)
  const user = useAppSelector((state) => state.auth.user)
  const isLoading = useAppSelector((state) => state.film.isLoading)

  const { filmId, parentComment } = props
  const [commentText, setCommentText] = React.useState<string>(
    `${parentComment.author.name} ${parentComment.author.surname}, `
  )

  const addAnswerCommentHandler = () => {
    if (commentText && user) {
      const commentData = {
        author: {
          name: user.name,
          surname: user.surname,
          avatar: user.avatar ?? null,
        },
        text: commentText,
      }

      dispatch(addChildFilmComment(filmId, commentData, parentComment.id))
    }
  }

  return (
    <React.Fragment>
      {isAuth && user && (
        <Stack
          width="100%"
          maxWidth="1200px"
          alignItems="flex-end"
          marginRight={7}
          marginBottom={5}
        >
          <Stack flexDirection="row" alignItems="flex-end" marginBottom="10px">
            <Avatar
              alt="Remy Sharp"
              src={
                user.avatar
                  ? `${API_URL}/users/media` + user.avatar
                  : "https://d2yht872mhrlra.cloudfront.net/user/138550/user_138550.jpg"
              }
              sx={{ width: 100, height: 100, marginRight: 3 }}
            />
            <TextField
              placeholder="Your comment"
              multiline
              sx={{ width: 500 }}
              value={commentText}
              onChange={(event) => setCommentText(event.target.value)}
            />
          </Stack>
          {isLoading ? (
            <Box display="flex" justifyContent="center">
              <CircularProgress size={60} />
            </Box>
          ) : (
            <Button variant="outlined" sx={{ width: 100 }} onClick={addAnswerCommentHandler}>
              Add
            </Button>
          )}
        </Stack>
      )}
    </React.Fragment>
  )
}
