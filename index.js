const { SerialPort } = require("serialport");
const cobs = require("./cobs.js");
const express = require("express");

const app = express();

const port = new SerialPort(
  {
    path: "COM14",
    baudRate: 9600,
  },
  (err) => {
    if (err) {
      console.log(err.message);
    }
  }
);

function intsToBytes(arr) {
  var data = new Uint32Array(arr);
  var buffer = new ArrayBuffer(data.byteLength);
  var intView = new Uint32Array(buffer).set(data);
  var byteView = new Uint8Array(buffer);

  return byteView;
}

function floatsToBytes(arr) {
  var data = new Float32Array(arr);
  var buffer = new ArrayBuffer(data.byteLength);
  var floatView = new Float32Array(buffer).set(data);
  var byteView = new Uint8Array(buffer);

  return byteView;
}

function pack(msg, payload, msgCount) {
  // const length = 1+msg.length+1+payload.length+1;
  const buffer = [];

  if (msg.length > 255) console.error("msg too long");
  buffer.push(msg.length);
  msg.split("").forEach((char) => buffer.push(char.charCodeAt(0)));
  if (payload.length > 255) console.error("payload too long");
  buffer.push(payload.length);
  payload.forEach((byte) => buffer.push(byte));
  buffer.push(msgCount);
  // buffer.push(TERMINATOR);

  return new Uint8Array(buffer);
}

let msgCount = 0;

function send(msg, payload = []) {
  let packedMsg = pack(msg, payload, msgCount);
  packedMsg = cobs.encode(packedMsg);

  port.write(packedMsg, (err) => {
    if (err) {
      console.log("Error on write");
      return;
    }
  });

  msgCount = (msgCount + 1) % 9;
}

async function servo(angle) {
  const bytes = intsToBytes([angle]);
  await send("servo", bytes);
}

async function goTo(x, y) {
  const bytes = floatsToBytes([x, y]);
  await send("go", bytes);
}

async function penup() {
  await servo(100);
}

async function pendown() {
  await servo(2000);
}

app.get("/up", (req, res) => {
  penup();
  res.json({ status: "ok" });
});

app.get("/down", (req, res) => {
  pendown();
  res.json({ status: "ok" });
});

app.get("/goto", (req, res) => {
  let x = req.query.x;
  let y = req.query.y;
  goTo(x, y);
  res.json({ status: "ok" });
});

app.listen(3000);
