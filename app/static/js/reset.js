var c;
var ctx;

function initialize() {
  c = document.getElementById("game");
  ctx = c.getContext("2d");

  c.width = window.innerWidth * 0.6;
  c.height = window.innerHeight * 0.8;
  c.style.border = "1px solid";
  c.style.backgroundColor = "#B4ABFC";
}

initialize();