var c;
var ctx;

function initialize() {
  c = document.getElementById("can");
  ctx = c.getContext("2d");
  c.width = window.innerWidth * 0.6;
  c.height = window.innerHeight * 0.8;
  c.style.border = "1px solid";
  c.style.backgroundColor = "#B4ABFC";
}

function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("Text", ev.target.id);
}

function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text");
  ev.target.appendChild(document.getElementById(data));
}


function sentence() {
  let sentence = "";
  var x = document.getElementById("sentence").children;
  for (let i = 0; i < x.length; i++) {
    sentence += x[i].name + " ";
  }

  fetch("/getdata", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },

    // A JSON payload
    body: JSON.stringify({
      sentence: sentence
    }),
  })
    .then(function (response) {
      // At this point, Flask has printed our JSON
      return response.text();
    })
    .then(function (text) {
      console.log("POST response: ");

      // Should be 'OK' if everything was successful
      console.log(text);
    });
    window.location.replace("/reset");
}

initialize();