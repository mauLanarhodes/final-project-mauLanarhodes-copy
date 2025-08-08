const express = require("express");
const path = require("path");
const bodyParser = require("body-parser");
const app = express();
const PORT = 3000;

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(express.static(path.join(__dirname, "public")));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

const BACKEND_URL = "http://127.0.0.1:5000"; // Flask server

// Login Page
app.get("/", (req, res) => res.render("login", { error: null }));

app.post("/login", async (req, res) => {
  const { username, password } = req.body;
  const response = await fetch(`${BACKEND_URL}/api/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (response.ok) {
    res.redirect("/floors");
  } else {
    res.render("login", { error: "Invalid credentials" });
  }
});

// Floors Page
app.get("/floors", async (req, res) => {
  const response = await fetch(`${BACKEND_URL}/api/floors`);
  const floors = await response.json();
  res.render("floors", { floors });
});

app.post("/floors/add", async (req, res) => {
  await fetch(`${BACKEND_URL}/api/floors`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req.body),
  });
  res.redirect("/floors");
});

app.post("/floors/delete/:id", async (req, res) => {
  await fetch(`${BACKEND_URL}/api/floors/${req.params.id}`, {
    method: "DELETE",
  });
  res.redirect("/floors");
});

// Rooms Page
app.get("/rooms", async (req, res) => {
  const [roomsRes, floorsRes] = await Promise.all([
    fetch(`${BACKEND_URL}/api/rooms`),
    fetch(`${BACKEND_URL}/api/floors`)
  ]);
  const rooms = await roomsRes.json();
  const floors = await floorsRes.json();
  res.render("rooms", { rooms, floors });
});

app.post("/rooms/add", async (req, res) => {
  await fetch(`${BACKEND_URL}/api/rooms`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req.body),
  });
  res.redirect("/rooms");
});

app.post("/rooms/delete/:id", async (req, res) => {
  await fetch(`${BACKEND_URL}/api/rooms/${req.params.id}`, {
    method: "DELETE",
  });
  res.redirect("/rooms");
});

// Residents Page
app.get("/residents", async (req, res) => {
  const [residentsRes, roomsRes] = await Promise.all([
    fetch(`${BACKEND_URL}/residents`),        
    fetch(`${BACKEND_URL}/api/rooms`)          
  ]);
  const residents = await residentsRes.json();
  const rooms = await roomsRes.json();
  res.render("residents", { residents, rooms });
});

app.post("/residents/add", async (req, res) => {
  await fetch(`${BACKEND_URL}/api/residents`, { 
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req.body),
  });
  res.redirect("/residents");
});

app.post("/residents/delete/:id", async (req, res) => {
  await fetch(`${BACKEND_URL}/api/residents/${req.params.id}`, {
    method: "DELETE",
  });
  res.redirect("/residents");
});
app.listen(PORT, () => {
  console.log(`Frontend running on http://127.0.0.1:${PORT}`);
});
