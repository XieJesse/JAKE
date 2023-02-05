document.addEventListener("DOMContentLoaded", function () {
    const collection = document.querySelector("#coll")
    const posts = collection.getElementsByClassName("card animated animatedFadeInUp fadeInUp")
    console.log(posts);
    for (let i = 0; i < posts.length; i++) {
        button = posts[i].getElementsByClassName("fa-heart")[0]

        button.addEventListener("click", function () {
            this.classList.toggle('fa-regular');
            this.classList.toggle('fa-solid');
            if (this.classList.contains('fa-solid')) {
              this.innerHTML = "&nbsp; "+(parseInt(this.innerHTML.slice(7))+1) ;
            }
            else {
              this.innerHTML = "&nbsp; "+(parseInt(this.innerHTML.slice(7))-1) ;
            }
            var data = [
              {"method" : this.classList.contains('fa-solid')},
              {"username" : posts[i].getElementsByClassName("name")[0].innerHTML.slice(13)},
              {"content" : posts[i].getElementsByClassName("content")[0].innerHTML},
              {"datetime" : posts[i].getElementsByClassName("time")[0].innerHTML.slice(10)}
            ]
            $.ajax({
              type: "POST",
              url: "/collection",
              data: JSON.stringify(data),
              contentType: "application/json",
              dataType: 'json',
              success: function(result) {
                console.log("Result:");
                console.log(result);
              }
            });
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
