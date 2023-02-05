document.addEventListener("DOMContentLoaded", function () {
    const carousel = document.querySelector(".carousel-inner")
    const items = carousel.getElementsByClassName("carousel-item")
    console.log(items);
    for (let i = 0; i < items.length; i++) {
        text = items[i].getElementsByClassName("d-block")[0] ;
        text.style.fontSize = String(50 - ((text.innerHTML.length - 50) / 7)) + "px" ;
        console.log(text.innerHTML.length) ;
        console.log(text.style.fontSize) ;
    }
})
