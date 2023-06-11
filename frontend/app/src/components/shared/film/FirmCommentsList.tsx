import React from "react"
import { FilmComment } from "./FilmComment"
import { useAppSelector, useAppDispatch } from "../../../store"
import { IChildComment, IComment } from "../../../core/entities"
import { filmActions } from "../../../store/filmReducer"
import { Avatar, Button, Stack, TextField } from "@mui/material"

let id = -1

export const FilmCommentsList: React.FC = () => {
  const dispatch = useAppDispatch()
  const comments = useAppSelector((state) => state.film.comments)

  const [answerCommentId, setAnswerCommentId] = React.useState<number | null>(null)
  const [commentText, setCommentText] = React.useState<string | null>(null)
  const [isScroll, setIsScroll] = React.useState(false)

  const addCommentAnswerHandler = (author: string, parentCommentId: number) => {
    console.log(parentCommentId)
    setAnswerCommentId(parentCommentId)
    setCommentText(`${author}, `)
  }

  const addCommentHandler = () => {
    if (commentText) {
      const commentInputData = {
        author: "Test User 1",
        text: commentText,
      }
      id += 1
      if (!answerCommentId) {
        const comment: IComment = {
          id: id,
          child_comments: [],
          ...commentInputData,
        }

        dispatch(filmActions.addComment(comment))
      } else {
        const childComment: IChildComment = {
          parentCommentId: answerCommentId,
          ...commentInputData,
        }

        dispatch(filmActions.addChildComment(childComment))
      }

      setIsScroll(!isScroll)
    }
  }

  React.useEffect(() => window.scrollTo(0, document.body.scrollHeight), [isScroll])

  return (
    <React.Fragment>
      {comments.map((comment, index) => (
        <FilmComment key={index} comment={comment} onAddAnswer={addCommentAnswerHandler} />
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
        <Button variant="outlined" sx={{ width: 100 }} onClick={addCommentHandler}>
          Add
        </Button>
      </Stack>
    </React.Fragment>
  )
}
