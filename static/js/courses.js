// reference: w3schools.com

let navOpen = false;

function openNav() {
    document.getElementById("courses_sidenav").style.width = "200px";
    document.getElementById("courses_sidenav").style.borderRight = "1px solid #c7cdd1";
    document.getElementById("courses_sidenav").style.zIndex = "10";


    // document.getElementById("main").style.marginLeft = "250px";
    // adds a grey background on click
    // document.body.style.backgroundColor = "rgba(0,0,0,0.4)";

    navOpen = true;
}

function closeNav() {
    document.getElementById("courses_sidenav").style.width = "0";
    document.getElementById("courses_sidenav").style.zIndex = "-1";
    document.getElementById("courses_header").style.marginLeft= "0";
    document.getElementById("courses_sidenav").style.borderRight = "0px";
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

var coll = document.getElementsByClassName("collapsible_header");
var i;

for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
}


var docWidth = document.documentElement.offsetWidth;

[].forEach.call(
    document.querySelectorAll('*'),
    function(el) {
        if (el.offsetWidth > docWidth) {
            console.log(el);
        }
    }
);


// FORM VALIDATION: CHANGE PASSWORD VALIDATION
// SITE https://getbootstrap.com/docs/5.0/forms/validation/
// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')


  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
})()