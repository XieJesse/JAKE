var c;
var ctx;

function initialize() {
  c = document.getElementById("game");
  ctx = c.getContext("2d");
  c.width = window.innerWidth * 0.64;
  c.height = window.innerHeight * 0.36;
  c.style.backgroundColor = "rgba(255, 255, 255, 0.7)";
  if (sessionStorage["refresh"]) {
    var sentence = document.getElementById("sentence");
    sentence.innerHTML = sessionStorage["refresh"];
    sessionStorage["refresh"] = ""
  }
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

  if (sentence.length > 0) {
    fetch("/getdata", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },

      // A JSON payload
      body: JSON.stringify({
        sentence: sentence,
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
    sessionStorage.clear();
    sessionStorage["sentence"] = sentence;
    window.location.replace("/reset");
  }
}

function refresh() {
  var sentence = document.getElementById("sentence");
  var initial = sentence.innerHTML;
  sessionStorage["refresh"] = initial;
  window.location.replace("/game");
}

initialize();
