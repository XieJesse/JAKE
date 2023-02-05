var c;
var ctx;

function initialize() {
  c = document.getElementById("game");
  ctx = c.getContext("2d");
  c.width = window.innerWidth * 0.6;
  c.height = window.innerHeight * 0.8;
  c.style.border = "1px solid";
  c.style.backgroundColor = "rgba(255, 255, 255, 0.7)";
  ctx.font = "36px Inter";
  ctx.fillStyle = "red";
  ctx.textBaseline = "middle";
  ctx.textAlign = "center";
  ctx.fillText("Here is what you created: ", c.width / 2, 100);
  ctx.strokeStyle = "red";
  ctx.beginPath();
  ctx.roundRect(
    c.width / 2 - c.width * 0.4,
    c.height / 4,
    c.width * 0.8,
    c.height / 6,
    9
  );
  ctx.stroke();
  ctx.font = "36px Caveat";
  ctx.fillText(sessionStorage["sentence"], c.width / 2, c.height / 4 + c.height / 12);
}

function copy() {
  navigator.clipboard.writeText(sessionStorage["sentence"]);
}

initialize();
