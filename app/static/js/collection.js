document.addEventListener("DOMContentLoaded", function () {
    const collection = document.querySelector("#coll")
    const posts = collection.getElementsByClassName("card animated animatedFadeInUp fadeInUp")
    console.log(posts);
    for (let i = 0; i < posts.length; i++) { 
        button = posts[i].getElementsByClassName("fa")[0]

        button.addEventListener("click", function () {
            console.log("clicked")
            if (button.classList.contains("fa-thumbs-up")) {
				this.classList.remove("fa", "fa-thumbs-up");
				this.classList.add("fa", "fa-thumbs-down");
                  
            } else {
                console.log("thumbs down to thumbs up");
				this.classList.remove("fa,", "fa-thumbs-down", "unlike");
				this.classList.add("fa", "fa-thumbs-up", "like");
            }
            // button.classList.toggle("fa-thumbs-down");
        })
        //console.log(posts[i]);
    }
});