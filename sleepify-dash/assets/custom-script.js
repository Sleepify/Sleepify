


document.addEventListener("click", function() {
    var image1 = document.getElementById("1");
    var image2 = document.getElementById("2");
    var image3 = document.getElementById("3");
    var image4 = document.getElementById("4");
    if (image1 !== null) {
        image1.style.visibility = "hidden";
        image2.style.visibility = "visible";
        image1.parentNode.removeChild(image1);
        return;
    }

    if (image2 !== null) {
        image2.style.visibility = "hidden";
        image3.style.visibility = "visible";
        image2.parentNode.removeChild(image2);
        return;
    }

    if (image3 !== null) {
        image3.style.visibility = "hidden";
        image4.style.visibility = "visible";
        image3.parentNode.removeChild(image3);
        return;
    }

    if (image4 !== null) {
        image4.style.visibility = "hidden";
        image4.parentNode.removeChild(image4);
        window.location = 'http://127.0.0.1:8050/apps/app1';
        return;
    }

    var app1 = document.getElementById("predictions");
    if (app1 !== null) {
        window.location = 'http://127.0.0.1:8050/apps/app3';
    } 
});

