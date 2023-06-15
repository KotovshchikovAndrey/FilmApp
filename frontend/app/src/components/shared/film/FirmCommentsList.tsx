import React from "react"
import {FilmComment} from "./FilmComment"
import {useAppSelector, useAppDispatch} from "../../../store"
import {IComment, ICommentAuthor} from "../../../core/entities"
import {
  Avatar,
  Box,
  Button,
  CircularProgress, Grid, List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Stack,
  TextField, Typography
} from "@mui/material"
import {addChildFilmComment, addFilmComment, getFilmComments} from "../../../store/actionCreators"
import {API_URL} from "../../../core/config"
import {AddAnswerFilmComment} from "./AddAnswerFilmComment"

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
    setParentComment({id: parentCommentId, author: parentCommentAuthor})
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

  const countComments = (comments: IComment[]): number => {
    let count = 0
    for (let comment of comments) {
      count += comment.child_comments.length + 1
    }
    return count
  }

  return (
    <React.Fragment>
      <Typography variant="h5">{countComments(comments)} comments</Typography>
      {isAuth && user && user.status === "active" && (
        <Box display="flex" alignItems="flex-start" gap={3}>
            <Avatar
              src={
                user.avatar
                  ? `${API_URL}/users/media` + user.avatar
                  : "https://d2yht872mhrlra.cloudfront.net/user/138550/user_138550.jpg"
              }
              sx={{width: 40, height: 40}}
            />
            <TextField
              variant="standard"
              sx={{flexGrow: 1}}
              placeholder="Add a comment..."
              fullWidth
              value={commentText}
              onChange={(event) => setCommentText(event.target.value)}
            />
            {isLoading ? (
              <Box display="flex" justifyContent="center">
                <CircularProgress size={60}/>
              </Box>
            ) : (
              <Button variant="outlined" sx={{width: 100}} onClick={addCommentHandler}>
                Comment
              </Button>
            )}

        </Box>
      )}

      <Stack>
        {comments.map((comment) => (
          <>
            <FilmComment
              key={comment.comment_id}
              comment={comment}
              onAddAnswer={addCommentAnswerHandler}
            />
            {
              parentComment?.id === comment.comment_id && (
                <AddAnswerFilmComment
                  key={comment.comment_id}
                  filmId={props.filmId}
                  parentComment={parentComment}
                />
              )
            }
          </>
        ))}
      </Stack>
    </React.Fragment>
  )
}
