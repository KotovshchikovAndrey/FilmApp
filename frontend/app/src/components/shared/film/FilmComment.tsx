import React from "react"
import { Typography, Stack, Avatar, Button } from "@mui/material"
import { IComment, ICommentAuthor } from "../../../core/entities"
import { FilmChildComment } from "./FilmChildComment"
import { API_URL } from "../../../core/config"
import { useAppSelector } from "../../../store"

interface FilmCommentProps {
  comment: IComment
  onAddAnswer: (author: ICommentAuthor, parentCommentId: number) => void
}

export const FilmComment: React.FC<FilmCommentProps> = (props: FilmCommentProps) => {
  const { comment, onAddAnswer } = props

  const isAuth = useAppSelector((state) => state.auth.isAuth)
  const user = useAppSelector((state) => state.auth.user)

  return (
    <React.Fragment>
      <Stack alignItems="flex-end" marginBottom={3} width="100%" maxWidth="1200px">
        <Stack flexDirection="row" alignItems="flex-end" width="100%">
          <Avatar
            alt="Remy Sharp"
            src={
              comment.author.avatar
                ? `${API_URL}/users/media` + comment.author.avatar
                : "https://d2yht872mhrlra.cloudfront.net/user/138550/user_138550.jpg"
            }
            sx={{ width: 100, height: 100, marginRight: 3 }}
          />
          <Stack>
            <Typography fontWeight="bold" marginBottom="7px">
              {comment.author.name} {comment.author.surname}
            </Typography>
            <Typography>{comment.text}</Typography>
          </Stack>
        </Stack>
        {isAuth && user && user.status === "active" && (
          <Button onClick={() => onAddAnswer(comment.author, comment.comment_id)}>
            Add answer
          </Button>
        )}
      </Stack>
      {comment.child_comments.map((childComment) => (
        <FilmChildComment
          key={childComment.comment_id}
          parentCommentId={comment.comment_id}
          comment={childComment}
          onAddAnswer={onAddAnswer}
        />
      ))}
    </React.Fragment>
  )
}
