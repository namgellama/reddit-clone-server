import express, { Request, Response } from "express";

const app = express();

app.get("", (request: Request, response: Response) => {
	response.json("Hello world");
});

app.listen(8000, () => {
	console.log(`Listening on PORT 8000`);
});
