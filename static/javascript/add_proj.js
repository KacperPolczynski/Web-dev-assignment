
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
const responseMessage = document.getElementById("responseMessage");

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

    /*https://openjavascript.info/2022/06/08/how-to-upload-a-file-using-the-fetch-api/*/
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
        form.reset();
        modal.style.display = "none";
    } catch (error) {
        console.error("Error:", error);
    }
});
    

        
