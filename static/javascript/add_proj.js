/*code adapted from: https://www.w3schools.com/howto/howto_css_modals.asp*/
/*Accessed on 12/12/2024*/
/*modal pop up allowed me to implement a form to add a project*/
    var modal = document.getElementById("myModal");
    var btn = document.getElementById("add-proj-btn");
    var span = document.getElementsByClassName("close")[0];

    btn.addEventListener("click", function() {
        console.log("clicked");
        modal.style.display = "block";
    });

    span.addEventListener("click", function() {
        modal.style.display = "none";
    });

    window.addEventListener("click", function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
    
 /* submit form */
const form = document.getElementById("proj_form");
const project_container = document.getElementById("project-container");

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const inputData = {
        name : document.getElementById("name").value,
        proj_type : document.getElementById("proj_type").value,
        description : document.getElementById("description").value,
        proj_link : document.getElementById("proj_link").value,

    };
    const uploadElement = document.getElementById("photo_url");
    const file = uploadElement.files[0];
    const payload = new FormData();
    payload.append("photo_url", file);

    /* Code adapted from: https://openjavascript.info/2022/06/08/how-to-upload-a-file-using-the-fetch-api/ */
    /*Accessed on 12/12/2024*/
    /*This code allowed me to upload a file to the server*/
    try {
        const photoupload = await fetch('/upload', {
            method : 'POST', 
            body : payload,
        });

        if (!photoupload.ok) {
            console.error("Failed to upload file");
            return;
        }
        const photo_data = await photoupload.json();
        const photo_url = photo_data.file_url;
        
    
    
    
        const add_proj = await fetch('/add_project', {  
            method: 'POST',  
            headers: {  'Content-Type': 'application/json'},  
            body: JSON.stringify(
                {
                "name": inputData.name,
                "proj_type": inputData.proj_type,
                "description": inputData.description,
                "proj_link": inputData.proj_link,
                "photo_url": photo_url
                }
                )
            }
        )
        if (!add_proj.ok) {
            console.error("Failed to add project");
            return;
        }



        const new_proj = await add_proj.json();
        const new_proj_html = `
        <figure>
            <div class="each-proj-container">
                <figcaption class="project-desc"><strong>${new_proj.name}</strong></figcaption>
                <figcaption class="project-desc">${new_proj.proj_type}</figcaption>
            </div>
            <img src="${new_proj.photo_url}" alt="${new_proj.name}" class="project-image"></img>
            <div class="project-desc">
                <h6>Project description:</h6>
                <p class="description">${new_proj.description}</p>
            </div>
            <div>
                <h6>Code accessed here:</h6>
                <p class="description"><a href=${project.link}>${project.link}</a></p>
            </div>
            <div id="comments-header">
                <h6>Comments:</h6>
            </div>
            <form action="/comment" method="POST" class="comments-section">
                <input type="hidden" name="project_id" value="${new_proj.id}">
                <div class="comment-box">
                    <textarea name="comment" placeholder="Add a comment..." required></textarea>
                    <button type="submit">Submit</button>
                </div>
            </form>
            <div class="user-comments">
            </div>
        </figure>
        `;
        project_container.insertAdjacentHTML('beforeend', new_proj_html);

        form.reset();
        modal.style.display = "none";

    } catch (error) {
        console.error("Error:", error);
    }
});


    

        
