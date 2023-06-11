import React from "react"
import { Typography, Stack, Avatar, Button, Box } from "@mui/material"
import { IChildComment, ICommentAuthor } from "../../../core/entities"
import { API_URL } from "../../../core/config"

interface FilmChildCommentProps {
  parentCommentId: number
  comment: IChildComment
  onAddAnswer: (author: ICommentAuthor, parentCommentId: number) => void
}

export const FilmChildComment: React.FC<FilmChildCommentProps> = (props: FilmChildCommentProps) => {
  const { parentCommentId, comment, onAddAnswer } = props

  return (
    <React.Fragment>
      <Stack alignItems="flex-end" marginBottom={3} width="93%" maxWidth="1200px">
        <Stack flexDirection="row" alignItems="flex-end" width="93%">
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
        <Button onClick={() => onAddAnswer(comment.author, parentCommentId)}>Add answer</Button>
      </Stack>
    </React.Fragment>
  )
}
