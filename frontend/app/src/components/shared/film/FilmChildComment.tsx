import React from "react"
import { Typography, Stack, Avatar, Button, Box } from "@mui/material"
import { IChildComment, ICommentAuthor } from "../../../core/entities"
import { API_URL } from "../../../core/config"
import { useAppSelector } from "../../../store"

interface FilmChildCommentProps {
  parentCommentId: number
  comment: IChildComment
  onAddAnswer: (author: ICommentAuthor, parentCommentId: number) => void
}

export const FilmChildComment: React.FC<FilmChildCommentProps> = (props: FilmChildCommentProps) => {
  const { parentCommentId, comment, onAddAnswer } = props

  const isAuth = useAppSelector((state) => state.auth.isAuth)
  const user = useAppSelector((state) => state.auth.user)

  return (
    <React.Fragment>
      <Stack alignItems="flex-end" marginBottom={3} maxWidth="1200px" pl={8} width="100%">
        <Stack flexDirection="row" alignItems="flex-start"  width="100%">
          <Avatar
            src={
              comment.author.avatar
                ? `${API_URL}/users/media` + comment.author.avatar
                : "https://d2yht872mhrlra.cloudfront.net/user/138550/user_138550.jpg"
            }
            sx={{ width: 40, height: 40, marginRight: 3 }}
          />
          <Stack>
            <Typography flexGrow={1} variant="subtitle1" fontWeight="bold" marginBottom="7px">
              {comment.author.name} {comment.author.surname}
            </Typography>
            <Typography variant="body1">{comment.text}</Typography>
          </Stack>
        </Stack>
        {isAuth && user && user.status === "active" && (
          <Button onClick={() => onAddAnswer(comment.author, parentCommentId)}>Reply</Button>
        )}
      </Stack>
    </React.Fragment>
  )
}
