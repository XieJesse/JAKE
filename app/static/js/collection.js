document.addEventListener("DOMContentLoaded", function () {
    const collection = document.querySelector("#coll")
    const posts = collection.getElementsByClassName("card animated animatedFadeInUp fadeInUp")
    console.log(posts);
    for (let i = 0; i < posts.length; i++) { 
        button = posts[i].getElementsByClassName("fa-heart")[0]

        button.addEventListener("click", function () {
            console.log("clicked")
            if (button.classList.contains("fa-regular")) {
				this.classList.remove("fa-regular");
				this.classList.add("fa-solid");
                console.log(button)
            } 
            else {
                console.log("thumbs down to thumbs up");
				this.classList.remove("fa-solid");
				this.classList.add("fa-regular");
            }
        })
        //console.log(posts[i]);
    }
});