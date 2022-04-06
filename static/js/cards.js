window.onload = function (e) {

    const sections = [{
        title: "Search",
        image: ["/static/assets/search_icon.jpg"],
        description: "Enter your symptoms as plain text",
        url: "/complaint",
        button: "enter",
        class: "",
        target: ""
    },
    {
        title: "Select",
        image: ["/static/assets/select_icon.jpg"],
        description: "Select from a wide range of symptoms for accurate diagnosis",
        url: "/search",
        button: "enter",
        class: "",
        target: ""
    },
    {
        title: "Lab Results",
        image: ["/static/assets/lab.jpg"],
        description: "Enter your lab test results for a more guided diagnosis",
        url: "/labresult",
        button: "enter",
        class: "",
        target: ""
    },
    ];


    const intro = document.querySelector('.intro'),
        socialItems = document.querySelector('.social');


    // Add the Intro Sections
    sections.forEach(function (el) {
        const randomImage = Math.floor(Math.random() * el.image.length);
        const template = `
        <a class="introItem ${el.class}" href="${el.url}" target="${el.target}" >
            <figure class="introItem__image">
                    <img src="${el.image[randomImage]}" alt="">
            </figure>
            <div class="introItem__content">
                <h2 class="introItem__title">${el.title}</h2>
                <p class="introItem__text">${el.description}</p>
                <div class="introItem__button"><p>${el.button}</p><span></span></div>
            </div>
        </a>
        `;

        intro.insertAdjacentHTML("beforeend", template);

    })

    //Animate Intro Section on Hover
    const introItem = document.querySelectorAll('.introItem');
    introItem.forEach(function (el) {
        el.addEventListener("mouseover", animeIn);
        el.addEventListener("mouseleave", animeOut);
    })

    function animeIn(e) {
        introItem.forEach(function (el) {
            el.style.opacity = "0.5";
            el.style.transform = "scale(0.95)";
        });
        e.currentTarget.style.opacity = "1";
        e.currentTarget.style.transform = "scale(1)";
    };

    function animeOut() {
        introItem.forEach(function (el) {
            el.style.opacity = "1";
            el.style.transform = "scale(1)";
        });

    };

    // Make the wrapper 100vh on mobile
    if (window.innerWidth <= 899) {
        document.querySelector('#wrapper').style.height = window.innerHeight + "px";
    }

};