import { getPosts } from "@controllers/post";
import express from "express";

const router = express.Router();

router.route("/").get(getPosts);

export default router;
