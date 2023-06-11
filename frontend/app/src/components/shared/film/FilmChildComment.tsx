import React from "react"
import { Typography, Stack, Avatar, Button, Box } from "@mui/material"
import { IChildComment } from "../../../core/entities"

interface FilmChildCommentProps {
  comment: IChildComment
  onAddAnswer: (author: string, parentCommentId: number) => void
}

export const FilmChildComment: React.FC<FilmChildCommentProps> = (props: FilmChildCommentProps) => {
  const { comment, onAddAnswer } = props

  return (
    <React.Fragment>
      <Stack alignItems="flex-end" marginBottom={3} width="93%" maxWidth="1200px">
        <Stack flexDirection="row" alignItems="flex-end" width="93%">
          <Avatar
            alt="Remy Sharp"
            src={"https://d2yht872mhrlra.cloudfront.net/user/138550/user_138550.jpg"}
            sx={{ width: 100, height: 100, marginRight: 3 }}
          />
          <Stack>
            <Typography fontWeight="bold" marginBottom="7px">
              {comment.author}
            </Typography>
            <Typography>{comment.text}</Typography>
          </Stack>
        </Stack>
        <Button onClick={() => onAddAnswer(comment.author, comment.parentCommentId)}>
          Add answer
        </Button>
      </Stack>
    </React.Fragment>
  )
}
