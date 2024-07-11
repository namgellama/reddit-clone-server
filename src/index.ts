import "module-alias/register";
import { errorHandler, notFound } from "@middlewares/errorMiddleware";
import postRoutes from "@routes/post";
import dotenv from "dotenv";
import express, { Request, Response } from "express";

dotenv.config();

const app = express();

app.use(express.json());

app.get("/", (request: Request, response: Response) => {
	response.send("Welcome to Reddit Clone API");
});

app.use("/api/posts", postRoutes);

app.use(notFound);
app.use(errorHandler);

const PORT = process.env.PORT || 8001;

app.listen(PORT, () => {
	console.log(`Listening on PORT ${PORT}`);
});
