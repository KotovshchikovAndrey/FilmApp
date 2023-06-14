import React from "react"
import { FilmComment } from "./FilmComment"
import { useAppSelector, useAppDispatch } from "../../../store"
import { ICommentAuthor } from "../../../core/entities"
import { Avatar, Box, Button, CircularProgress, Stack, TextField } from "@mui/material"
import { addChildFilmComment, addFilmComment, getFilmComments } from "../../../store/actionCreators"
import { API_URL } from "../../../core/config"
import { AddAnswerFilmComment } from "./AddAnswerFilmComment"

interface IFilmCommentsListProps {
  filmId: number
}

export const FilmCommentsList: React.FC<IFilmCommentsListProps> = (
  props: IFilmCommentsListProps
) => {
  const dispatch = useAppDispatch()

  const isAuth = useAppSelector((state) => state.auth.isAuth)
  const user = useAppSelector((state) => state.auth.user)

  const comments = useAppSelector((state) => state.film.comments)
  const isLoading = useAppSelector((state) => state.film.isLoading)

  const [commentText, setCommentText] = React.useState<string>("")
  const [parentComment, setParentComment] = React.useState<{
    id: number
    author: ICommentAuthor
  } | null>(null)

  const addCommentAnswerHandler = (
    parentCommentAuthor: ICommentAuthor,
    parentCommentId: number
  ) => {
    setParentComment({ id: parentCommentId, author: parentCommentAuthor })
  }

  const addCommentHandler = () => {
    if (commentText && user) {
      const commentData = {
        author: {
          name: user.name,
          surname: user.surname,
          avatar: user.avatar ?? null,
        },
        text: commentText,
      }

      dispatch(addFilmComment(props.filmId, commentData))
      setCommentText("")
    }
  }

  React.useEffect(() => {
    dispatch(getFilmComments(props.filmId))
  }, [])

  return (
    <React.Fragment>
      {comments.map((comment) => (
        <>
          <FilmComment
            key={comment.comment_id}
            comment={comment}
            onAddAnswer={addCommentAnswerHandler}
          />
          {parentComment?.id === comment.comment_id && (
            <AddAnswerFilmComment
              key={comment.comment_id}
              filmId={props.filmId}
              parentComment={parentComment}
            />
          )}
        </>
      ))}

      {isAuth && user && user.status === "active" && (
        <Stack alignItems="flex-end">
          <Stack
            flexDirection="row"
            alignItems="flex-end"
            width="100%"
            maxWidth="1200px"
            marginBottom="10px"
          >
            <Avatar
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
            <Button variant="outlined" sx={{ width: 100 }} onClick={addCommentHandler}>
              Add
            </Button>
          )}
        </Stack>
      )}
    </React.Fragment>
  )
}
