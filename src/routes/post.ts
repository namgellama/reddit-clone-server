import { createPost, getPosts } from "@controllers/post";
import express from "express";

const router = express.Router();

router.route("/").get(getPosts).post(createPost);

export default router;
