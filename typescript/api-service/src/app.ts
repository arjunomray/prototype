import express from "express";
import pg from "pg";

const app = express();
app.use(express.json());

const createUserTable = `
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT
);
`

const dbClient = new pg.Client({
    user: "postgres",
    password: "example",
    host:"localhost",
    port: 5432
})

dbClient.connect()
dbClient.query(createUserTable)

app.get("/users",async (req, res) => {
    const users = await dbClient.query("SELECT * FROM users;")
    return res.json({
        users: users.rows,
    })
})

app.post("/users", async (req, res) => {
    const { name, email } = req.body;
    if (!name || !email) {
        return res.status(400).json({
            message: "Invalid data"
        })
    }

    const emailUniquenessCheck = await dbClient.query("SELECT COUNT(id) FROM users WHERE email = $1", [email])
    if (Number(emailUniquenessCheck.rows[0].count) > 0) {
    return res.status(400).json({
        message: "user already exists"
        })
    }

    await dbClient.query("INSERT INTO users (name, email) VALUES($1, $2)",[name, email])
    return res.status(201).json({
        message: "User is created"
    })
})

app.get("/users/:id",async (req, res) => {
    const id = Number(req.params.id)
    if (Number.isNaN(id)){
        return res.status(400).json({
            message: "Invalid data"
        })
    }

    const user = await dbClient.query("SELECT * FROM users WHERE id = $1", [id])
    if(user.rows[0]) {
        return res.json({
            user: user.rows[0]
        })
    } else {
        return res.status(404).json({
            "message": "user not found"
        })
    }
})

app.listen("8080", () => {
    console.log("server is running");
})