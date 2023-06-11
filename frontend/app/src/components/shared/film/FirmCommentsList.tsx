import React from "react"
import { FilmComment } from "./FilmComment"
import { useAppSelector, useAppDispatch } from "../../../store"
import { ICommentAuthor } from "../../../core/entities"
import { Avatar, Box, Button, CircularProgress, Stack, TextField } from "@mui/material"
import { addChildFilmComment, addFilmComment, getFilmComments } from "../../../store/actionCreators"

interface IFilmCommentsListProps {
  filmId: number
}

export const FilmCommentsList: React.FC<IFilmCommentsListProps> = (
  props: IFilmCommentsListProps
) => {
  const dispatch = useAppDispatch()

  const comments = useAppSelector((state) => state.film.comments)
  const isLoading = useAppSelector((state) => state.film.isLoading)
  const errorMessage = useAppSelector((state) => state.film.errorMessage)

  const [answerCommentId, setAnswerCommentId] = React.useState<number | null>(null)
  const [commentText, setCommentText] = React.useState<string | null>(null)

  const addCommentAnswerHandler = (author: ICommentAuthor, parentCommentId: number) => {
    setAnswerCommentId(parentCommentId)
    setCommentText(`${author.name} ${author.surname}, `)
  }

  const addCommentHandler = () => {
    if (commentText) {
      const commentData = {
        author: {
          name: "User",
          surname: "Test",
          avatar: null,
        },
        text: commentText,
      }

      if (answerCommentId === null) {
        dispatch(addFilmComment(props.filmId, commentData))
      } else {
        dispatch(addChildFilmComment(props.filmId, commentData, answerCommentId))
      }
    }
  }

  React.useEffect(() => {
    dispatch(getFilmComments(props.filmId))
  }, [])

  React.useEffect(() => window.scrollTo(0, document.body.scrollHeight), [isLoading])

  return (
    <React.Fragment>
      {comments.map((comment) => (
        <FilmComment
          key={comment.comment_id}
          comment={comment}
          onAddAnswer={addCommentAnswerHandler}
        />
      ))}

      <Stack alignItems="flex-end">
        <Stack
          flexDirection="row"
          alignItems="flex-end"
          width="100%"
          maxWidth="1200px"
          marginBottom="10px"
        >
          <Avatar
            alt="Remy Sharp"
            src={"https://d2yht872mhrlra.cloudfront.net/user/138550/user_138550.jpg"}
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
          <Button variant="outlined" sx={{ width: 100 }} onClick={addCommentHandler}>
            Add
          </Button>
        )}
      </Stack>
    </React.Fragment>
  )
}
