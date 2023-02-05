var c;
var ctx;

function initialize() {
  c = document.getElementById("game");
  ctx = c.getContext("2d");
  c.width = window.innerWidth * 0.64;
  c.height = window.innerHeight * 0.48;
  c.style.backgroundColor = "rgba(255, 255, 255, 0.7)";
  if (!("rolls" in sessionStorage)) {
    sessionStorage["rolls"] = 1;
  }
  if (sessionStorage["refresh"]) {
    var sentence = document.getElementById("sentence");
    sentence.innerHTML = sessionStorage["refresh"];
    sessionStorage["refresh"] = "";
    sessionStorage["rolls"] = 1;
  }
}

function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("text/html", ev.target.id);
}

function drop(ev) {
  var _target = $("#" + ev.target.id);
  var data = ev.dataTransfer.getData("text/html");
  if ($(_target).hasClass("noDrop")) {
    console.log("no transfer");
    ev.preventDefault();
  } else {
    ev.preventDefault();
    ev.target.appendChild(document.getElementById(data));
  }
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
    sessionStorage["rolls"] = 1;
    window.location.replace("/reset");
  }
}

function refresh() {
  var sentence = document.getElementById("sentence");
  var initial = sentence.innerHTML;
  if (sessionStorage["rolls"] > 0) {
    sessionStorage["refresh"] = initial;
    sessionStorage["rolls"] -= 1;
    window.location.replace("/game");
  }
}

initialize();
