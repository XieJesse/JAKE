document.addEventListener("DOMContentLoaded", function () {
    const collection = document.querySelector("#coll")
    const posts = collection.getElementsByClassName("card animated animatedFadeInUp fadeInUp")
    console.log(posts);
    for (let i = 0; i < posts.length; i++) {
        button = posts[i].getElementsByClassName("fa-heart")[0]

        button.addEventListener("click", function () {
            console.log("clicked")
            this.classList.toggle('fa-regular');
            this.classList.toggle('fa-solid');
        }

        )
        copy = posts[i].getElementsByClassName("btn-primary")[0]

        copy.addEventListener("click", function() {
          console.log("copy")
          navigator.clipboard.writeText(posts[i].getElementsByClassName("content")[0].innerHTML);
        })
        //console.log(posts[i]);
    }
});
