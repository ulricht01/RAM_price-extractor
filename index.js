import express from "express";
import sqlite3 from "sqlite3"

const PORT = 3000;
const app = express()

const db = new sqlite3.Database("./ramky.db", (err) => {
    if (err) return console.error(err.message)
    else console.log("Připojeno k DB!")
})

export default db;

app.get("/all", (req,res) => {
    db.all("SELECT * FROM ramky", [], (err, rows) => {
        if(err){
            res.status(500).send("Nastal error: "+err.message);
            return;
        }
        res.json(rows)
    })
})  

app.get("/all/:op/:datum", (req,res) => {
    const {op, datum} = req.params
    const operators = {
        gt: ">",
        lt: "<",
        eq: "="
    }

    if(!operators[op]) return res.status(400).send("Neplatný operátor! Použij gt, lt nebo eq");

    const query = `SELECT * FROM ramky WHERE dt_insert ${operators[op]} ?`

    db.all(query, [datum], (err, rows) => {
        if(err){
            res.status(500).send("Nastal error: "+err.message);
            return;
        }
        res.json(rows)
    })
})  

app.listen(PORT, () =>{
    console.log("Server running on port: "+PORT)
})

