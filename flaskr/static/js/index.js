

async function getPlaceDivs(postData){
    let response = await fetch("/api/places", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(postData)
    });

    return ( await response.json() ) 
}



function addTagEvents(){
    const buttons = document.querySelectorAll(".tag-button")

    buttons.forEach(tagButton => {
        tagButton.addEventListener("click", e =>{
            e.preventDefault()
            const state = e.target.getAttribute("data-state")
            if (state == "ignore"){e.target.setAttribute("data-state", "include")}
            else if (state == "include"){e.target.setAttribute("data-state", "exclude")}
            else if (state == "exclude"){e.target.setAttribute("data-state", "ignore")}
            submitFilterForm()
        });
    });
}

function resetTags(){
    let buttons = document.querySelectorAll(".tag-button");
    buttons.forEach(button => {
        button.setAttribute("data-state", "ignore")
    });
}


function buildPostData(){
    let data = {
        "tags": {},
        "sort": ""
    }

    let buttons = document.querySelectorAll(".tag-button");
    buttons.forEach(button => {
        const tag_state = button.getAttribute("data-state");
        if (tag_state == "include"){
            data["tags"][button.innerHTML] = true
        } else if (tag_state == "exclude"){
            data["tags"][button.innerHTML] = false
        }
    });

    let sort_type = document.querySelector("#sort-type").value;
    data["sort"] = sort_type

    return data

}


function showPlaceDivs(data){
    let placeList = document.querySelector(".places-list");

    placeList.innerHTML = data
    
}


async function submitFilterForm(){
    postData = buildPostData();
    places = await getPlaceDivs(postData);
    showPlaceDivs(await places);
}

addTagEvents();
submitFilterForm()

