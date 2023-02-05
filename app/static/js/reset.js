var c;
var ctx;

function initialize() {
  c = document.getElementById("game");
  ctx = c.getContext("2d");
  c.width = window.innerWidth * 0.6;
  c.height = window.innerHeight * 0.8;
  c.style.border = "1px solid";
  c.style.backgroundColor = "rgba(0, 0, 0, 0.1)";

  ctx.font = "36px Helvetica";
  ctx.fillStyle = "red";
  ctx.textBaseline = "middle";
  ctx.textAlign = "center";
  ctx.fillText("Here is what you created: ", c.width / 2, 75);
  ctx.strokeStyle = "red";
  ctx.beginPath();
  ctx.roundRect(
    c.width / 2 - c.width * 0.4,
    c.height / 5,
    c.width * 0.8,
    c.height / 7,
    9
  );
  ctx.stroke();
  ctx.fillText(
    sessionStorage["sentence"],
    c.width / 2,
    c.height / 4
  );
}

initialize();
