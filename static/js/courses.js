// reference: w3schools.com

let navOpen = false;

function openNav() {
    document.getElementById("courses_sidenav").style.width = "250px";
    // document.getElementById("main").style.marginLeft = "250px";
    // adds a grey background on click
    // document.body.style.backgroundColor = "rgba(0,0,0,0.4)";

    navOpen = true;
}

function closeNav() {
    document.getElementById("courses_sidenav").style.width = "0";
    document.getElementById("courses_header").style.marginLeft= "0";
    document.body.style.backgroundColor = "white";

    navOpen = false;
}

function toggleNav() {
    if (navOpen === true){
        closeNav();
    }else{
        openNav();
    }
}

function highlightCurrentSection(){
    // highlight the section on the nav bar where the user is currently located
}
