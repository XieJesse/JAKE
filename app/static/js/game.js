function initialize() {
  if (sessionStorage["refresh"]) {
    var sentence = document.getElementById("sentence");
    sentence.innerHTML = sessionStorage["refresh"];
    sessionStorage["refresh"] = "";
  }
}

function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
  var _target = $("#" + ev.target.id);
  var data = ev.dataTransfer.getData("text");
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
