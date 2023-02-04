var canvas = document.createElement("canvas");
canvas.width = window.innerWidth * 0.6;
canvas.height = window.innerHeight * 0.8;

canvas.id = "CursorLayer";
canvas.style.zIndex = 8;
canvas.style.display = "block";
canvas.style.position = "absolute";
canvas.style.border = "1px solid";

var body = document.getElementsByTagName("body")[0];
body.appendChild(canvas);

cursorLayer = document.getElementById("CursorLayer");
console.log(cursorLayer);

var ctx = canvas.getContext("2d");
ctx.font = "30px Comic Sans MS";
ctx.fillStyle = "red";
ctx.textAlign = "center";
ctx.fillText(
  "Train to Become the Rizzard of Oz",
  canvas.width / 2,
  canvas.height / 3
);
