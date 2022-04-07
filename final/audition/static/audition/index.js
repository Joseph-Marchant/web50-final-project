document.addEventListener('DOMContentLoaded', function() {

    // Adding event listeners for the buttons
    document.querySelectorAll('.view').forEach(el => {
        el.addEventListener('click', () => view_audition(el.dataset.id));
    });
    document.querySelectorAll('.delete').forEach(el => {
        el.addEventListener('click', () => delete_audition(el.dataset.id));
    });

    // Default display all auditions
    display_auditions();
})

// Display all auditions
function display_auditions() {
    document.querySelector('.page-title').innerHTML = 'Your Auditions'
    document.querySelector('.all-auditions').style.display = 'block';
    document.querySelector('.single-audition').style.display = 'none';
};

// Function for viewing a single audition
function view_audition(id) {
    const single_audition = document.querySelector('.single-audition');

    // Fetch the auditon
    fetch(`/audition/${id}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(audition => {
        console.log(audition);
        document.querySelector('.page-title').innerHTML = `Audition for ${audition.role} in ${audition.title}`;
        
        // Add the date of the audition
        const date = document.createElement('div');
        date.innerHTML = `<h3 class=page-title>Audition on ${audition.date}</h3>`;
        date.setAttribute('id', 'single-date');
        single_audition.append(date);
    })
    
    // Fetch the scripts
    .then(() => {
        fetch(`/script/${id}`, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(scripts => {
            console.log(scripts);

            // Display the scripts
            const all_scripts = document.createElement('div')
            for (var i = 0; i < scripts.length; i++) {
                var script_display = document.createElement('div');
                script_display.innerHTML = `
                    <div class="script-name">
                        <textarea disabled="true" class="single-title" id=scene-${scripts[i].id}>${scripts[i].scene}</textarea>
                    </div>
                    <div class="script-body">
                        <textarea disabled="true" class="single-script" id=body-${scripts[i].id}>${scripts[i].script}</textarea>
                    </div>
                    <div class="script-buttons">
                        <button class=audition-buttons id="edit-${scripts[i].id}" data-audition_id="${id}" data-script_id="${scripts[i].id}" onclick="edit_script(this)" style="display: block;">Edit</button>
                        <a href="/self_tape/${scripts[i].id}"><button class=audition-buttons>Self-Shot</button></a>
                        <button class=audition-buttons id="save-${scripts[i].id}" data-script_id="${scripts[i].id}" onclick="save_edit(this)" style="display: none;">Save</button>
                        <button class=audition-buttons id="delete-${scripts[i].id}" data-script_id="${scripts[i].id}" onclick="delete_script(this)" style="display: none;">Delete</button>
                    </div>
                `
                script_display.setAttribute('class', 'script-display');
                script_display.setAttribute('id', `script-${scripts[i].id}`);
                all_scripts.append(script_display);
            }
            all_scripts.setAttribute('class', 'all-scripts');
            all_scripts.setAttribute('data-audition_id', `${id}`);
            single_audition.append(all_scripts);
        })
    })

    // Display only that audition
    .then(() => {
        document.querySelector('.all-auditions').style.display = 'none';
        document.querySelector('.single-audition').style.display = 'block';
    });
};

// Delete the audition
function delete_audition(id) {

    // Make the request to the server
    fetch(`/delete/${id}`, {
        method: 'POST'
    })

    // Remove the audition from the page
    .then(() => {
        const audition = document.getElementById(`${id}`);
        audition.style.display = 'none';
    })
};

// For editing scripts
function edit_script(button) {

    // Grab the title and the body of the script
    const title = document.getElementById(`scene-${button.dataset.script_id}`);
    const body = document.getElementById(`body-${button.dataset.script_id}`);

    // Update the elements to make the editable
    title.classList.add('single-title-edit');
    title.classList.remove('single-title');
    title.disabled = false;
    body.classList.add('single-script-edit');
    body.classList.remove('single-script');
    body.disabled = false;

    // Hide edit and selfshot buttons and show cancel and delete
    change_buttons(button, true);
}

// Save and edit
function save_edit(button) {

    // Grab the title and the body of the script
    const title = document.getElementById(`scene-${button.dataset.script_id}`);
    const body = document.getElementById(`body-${button.dataset.script_id}`);

    // Get the values from title and body
    const new_title = title.value;
    const new_body = body.value;
    const id = title.id.slice(6);

    // Make fetch request
    fetch('/save', {
        method: 'POST',
        body: JSON.stringify({
            "scene": new_title,
            "script": new_body,
            "id": id
        })
    })

    // Handle response
    .then(response => response.json())
    .then(result => {
        console.log(result);
    })
    .then(() => {
        // Update the elements to make the uneditable
        title.classList.add('single-title');
        title.classList.remove('single-title-edit');
        title.disabled = true;
        body.classList.add('single-script');
        body.classList.remove('single-script-edit');
        body.disabled = true;

        // Hide save and delete buttons and show edit and selfshot
        change_buttons(button, false);
    });

}

// Function to hide and show relevant buttond
function change_buttons(button, edit) {
    if(edit===true) {
        const edit = document.getElementById(`edit-${button.dataset.script_id}`);
        edit.style.display = 'none';
        const ss = document.getElementById(`ss-${button.dataset.script_id}`);
        ss.style.display = 'none';
        const save = document.getElementById(`save-${button.dataset.script_id}`);
        save.style.display = 'block';
        const del = document.getElementById(`delete-${button.dataset.script_id}`);
        del.style.display = 'block';
    } else {
        const edit = document.getElementById(`edit-${button.dataset.script_id}`);
        edit.style.display = 'block';
        const ss = document.getElementById(`ss-${button.dataset.script_id}`);
        ss.style.display = 'block';
        const save = document.getElementById(`save-${button.dataset.script_id}`);
        save.style.display = 'none';
        const del = document.getElementById(`delete-${button.dataset.script_id}`);
        del.style.display = 'none';
    };
}

// Delete script
function delete_script(button) {

    // Make the request to the server
    fetch(`/delete_script/${button.dataset.script_id}`, {
        method: 'POST'
    })

    // Handle response
    .then(response => response.json())
    .then(result => {
        console.log(result);
    })
    
    // Remove the audition from the page
    .then(() => {
        const script = document.getElementById(`script-${button.dataset.script_id}`);
        script.style.display = 'none';
    });
};

// Self shot
function self_shot(button) {
    
    // Make the request to the server
    fetch(`/self_tape/${button.dataset.script_id}`, {
        method: 'GET'
    })
}