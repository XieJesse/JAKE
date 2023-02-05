document.addEventListener("DOMContentLoaded", function () {
    const carousel = document.querySelector(".carousel-inner")
    const items = carousel.getElementsByClassName("carousel-item")
    console.log(items);
    for (let i = 0; i < items.length; i++) {
        text = items[i].getElementsByClassName("d-block")[0] ;
        text.style.fontSize = String(100 - text.innerHTML.length) + "px" ;
        console.log(text.style.fontSize) ;
    }
})
