import React from "react"
import { Typography, Stack, Avatar, Button, Box } from "@mui/material"
import { useAppSelector } from "../../../store"
import { IComment } from "../../../core/entities"
import { FilmChildComment } from "./FilmChildComment"

interface FilmCommentProps {
  comment: IComment
  onAddAnswer: (author: string, parentCommentId: number) => void
}

export const FilmComment: React.FC<FilmCommentProps> = (props: FilmCommentProps) => {
  const { comment, onAddAnswer } = props

  return (
    <React.Fragment>
      <Stack alignItems="flex-end" marginBottom={3} width="100%" maxWidth="1200px">
        <Stack flexDirection="row" alignItems="flex-end" width="100%">
          <Avatar
            alt="Remy Sharp"
            src={"https://d2yht872mhrlra.cloudfront.net/user/138550/user_138550.jpg"}
            sx={{ width: 100, height: 100, marginRight: 3 }}
          />
          <Stack>
            <Typography fontWeight="bold" marginBottom="7px">
              {comment.author} {comment.id}
            </Typography>
            <Typography>{comment.text}</Typography>
          </Stack>
        </Stack>
        <Button onClick={() => onAddAnswer(comment.author, comment.id)}>Add answer</Button>
      </Stack>
      {comment.child_comments.map((childComment, index) => (
        <FilmChildComment key={index} comment={childComment} onAddAnswer={onAddAnswer} />
      ))}

      {/* <Stack alignItems="flex-end" marginBottom={3}>
        <Stack flexDirection="row" alignItems="flex-end" width="93%" maxWidth="1200px">
          <Avatar
            alt="Remy Sharp"
            src={"https://d2yht872mhrlra.cloudfront.net/user/138550/user_138550.jpg"}
            sx={{ width: 100, height: 100, marginRight: 3 }}
          />
          <Stack>
            <Typography fontWeight="bold" marginBottom="7px">
              Test User
            </Typography>
            <Typography>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae, culpa necessitatibus
              eos ratione molestias quo numquam nesciunt sapiente expedita accusamus magni quam
              soluta et facere laborum a fugit harum eaque! Lorem ipsum dolor sit amet consectetur,
              adipisicing elit. Possimus, ipsam neque ea voluptas pariatur quidem vitae, distinctio
              deleniti voluptate dolorem quibusdam quam nisi sint. Rem at nemo placeat magnam
              perspiciatis? ipsum dolor sit amet consectetur, adipisicing elit. Possimus, ipsam
              neque ea voluptas pariatur quidem vitae, distinctio deleniti voluptate dolorem
              quibusdam quam nisi sint. Rem at nemo pla
            </Typography>
          </Stack>
        </Stack>
        <Button>Add answer</Button>
      </Stack>

      <Stack alignItems="flex-end" marginBottom={3}>
        <Stack flexDirection="row" alignItems="flex-end" width="93%" maxWidth="1200px">
          <Avatar
            alt="Remy Sharp"
            src={"https://d2yht872mhrlra.cloudfront.net/user/138550/user_138550.jpg"}
            sx={{ width: 100, height: 100, marginRight: 3 }}
          />
          <Stack>
            <Typography fontWeight="bold" marginBottom="7px">
              Test User
            </Typography>
            <Typography>
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae, culpa necessitatibus
              eos ratione molestias quo numquam nesciunt sapiente expedita accusamus magni quam
              soluta et facere laborum a fugit harum eaque! Lorem ipsum dolor sit amet consectetur,
              adipisicing elit. Possimus, ipsam neque ea voluptas pariatur quidem vitae, distinctio
              deleniti voluptate dolorem quibusdam quam nisi sint. Rem at nemo placeat magnam
              perspiciatis? ipsum dolor sit amet consectetur, adipisicing elit. Possimus, ipsam
              neque ea voluptas pariatur quidem vitae, distinctio deleniti voluptate dolorem
              quibusdam quam nisi sint. Rem at nemo pla
            </Typography>
          </Stack>
        </Stack>
        <Button>Add answer</Button>
      </Stack> */}
    </React.Fragment>
  )
}
