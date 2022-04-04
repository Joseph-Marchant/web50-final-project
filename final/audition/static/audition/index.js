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
    const single = document.querySelector('.single-audition')

    // Remove any data that was there before
    while (single.firstChild) {
        single.removeChild(single.firstChild)
    }
    single.style.display = 'none';
};

// Function for viewing a single audition
function view_audition(id) {
    console.log(`view ${id}`);
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
    fetch(`/script/${id}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(scripts => {
        console.log(scripts)

        // Display the scripts
        const all_scripts = document.createElement('div')
        for (var i = 0; i < scripts.length; i++) {
            var script_display = document.createElement('div');
            script_display.innerHTML = `
                <div class="script-name">
                    <textarea disabled="true" class="single-title">${scripts[i].scene}</textarea>
                </div>
                <div class="script-body">
                    <textarea disabled="true" class="single-script">${scripts[i].script}</textarea>
                </div>
                <div class="script-buttons">
                    <button class=audition-buttons data-script_id="${scripts[i].id}">Edit</button>
                    <button class=audition-buttons data-script_id="${scripts[i].id}">Self-Shot</button>
                </div>
            `
            script_display.setAttribute('class', 'script-display')
            all_scripts.append(script_display)
        }
        all_scripts.setAttribute('class', 'all-scripts')
        single_audition.append(all_scripts)
    })

    // Display only that audition
    document.querySelector('.all-auditions').style.display = 'none';
    document.querySelector('.single-audition').style.display = 'block';
};

function delete_audition(id) {
    console.log(`delete ${id}`);
};