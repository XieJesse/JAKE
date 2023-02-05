function copy() {
  navigator.clipboard.writeText(sessionStorage["sentence"]);
}

const node = document.createElement("p");
const textnode = document.createTextNode(sessionStorage["sentence"]);
node.appendChild(textnode);
document.getElementById("sentence").appendChild(node);
