
// smooth scroll
$(document).ready(function(){
    $(".navbar .nav-link").on('click', function(event) {

        if (this.hash !== "") {

            event.preventDefault();

            var hash = this.hash;

            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 700, function(){
                window.location.hash = hash;
            });
        } 
    });
}); 


function openForm1() {
    document.getElementById("myForm1").style.display = "block";
    document.getElementById("opbutton1").style.visibility = "hidden";
}

function closeForm1() {
    document.getElementById("myForm1").style.display = "none";
    document.getElementById("opbutton1").style.visibility = "visible"
}
function openForm2() {
    document.getElementById("myForm2").style.display = "block";
    document.getElementById("opbutton2").style.visibility = "hidden";
}

function closeForm2() {
    document.getElementById("myForm2").style.display = "none";
    document.getElementById("opbutton2").style.visibility = "visible"
}
function openForm3() {
    document.getElementById("myForm3").style.display = "block";
    document.getElementById("opbutton3").style.visibility = "hidden";
}

function closeForm3() {
    document.getElementById("myForm3").style.display = "none";
    document.getElementById("opbutton3").style.visibility = "visible"
}
function openForm4() {
    document.getElementById("myForm4").style.display = "block";
    document.getElementById("opbutton4").style.visibility = "hidden";
}

function closeForm4() {
    document.getElementById("myForm4").style.display = "none";
    document.getElementById("opbutton4").style.visibility = "visible"
}
function openForm5() {
    document.getElementById("myForm5").style.display = "block";
    document.getElementById("opbutton5").style.visibility = "hidden";
}

function closeForm5() {
    document.getElementById("myForm5").style.display = "none";
    document.getElementById("opbutton5").style.visibility = "visible"
}
function openForm6() {
    document.getElementById("myForm6").style.display = "block";
    document.getElementById("opbutton6").style.visibility = "hidden";
}

function closeForm6() {
    document.getElementById("myForm6").style.display = "none";
    document.getElementById("opbutton6").style.visibility = "visible"
}
