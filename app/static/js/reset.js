var c;
var ctx;

function initialize() {
  c = document.getElementById("can");
  ctx = c.getContext("2d");
  c.width = window.innerWidth * 0.6;
  c.height = window.innerHeight * 0.8;
  c.style.border = "1px solid";
  c.style.backgroundColor = "#B4ABFC";


  ctx.font = "36px Helvetica";
  ctx.fillStyle = "red";
  ctx.textAlign = "center"
  ctx.fillText("Here's what you came up with", c.height / 2, c.height / 8)
  ctx.strokeStyle = "red";
  ctx.beginPath();
  ctx.roundRect(c.width / 2 - c.width * .4, c.height / 4, c.width * 0.8, c.height / 6, 9);
  ctx.stroke();
}

initialize();
