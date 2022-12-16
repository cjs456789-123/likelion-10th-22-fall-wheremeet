function changeColor1(t) {
    tr = t.parentNode;
    tr.style.color = (t.checked) ?"#FF6C0F" :"#7C7A7A";
    document.getElementById("user-01").src = (t.checked) ?'img/1user-01.svg' :'img/user-01.svg';
    /*if(t.checked == true) {
        tr = t.parentNode;
        t.style.color = "#FF6C0F";
        docum
        document.getElementById("user-01").src = 'img/1user-01.svg';
    } else {
        tr.style.color = "#7C7A7A";
        document.getElementById("user-01").src = 'img/user-01.svg';
    }*/
}
function changeColor2(t) {
    tr = t.parentNode;
    tr.style.color = (t.checked) ?"#FF6C0F" :"#7C7A7A";
    document.getElementById("user-02").src = (t.checked) ?'img/1user-02.svg' :'img/user-02.svg';
}
function changeColor3(t) {
    tr = t.parentNode;
    tr.style.color = (t.checked) ?"#FF6C0F" :"#7C7A7A";
    document.getElementById("user-03").src = (t.checked) ?'img/1user-03.svg' :'img/user-03.svg';
}
function changeColor4(t) {
    tr = t.parentNode;
    tr.style.color = (t.checked) ?"#FF6C0F" :"#7C7A7A";
    document.getElementById("circle").src = (t.checked) ?'img/1circle.svg' :'img/circle.svg';
}
function changeColor5(t) {
    tr = t.parentNode;
    tr.style.color = (t.checked) ?"#FF6C0F" :"#7C7A7A";
    document.getElementById("square").src = (t.checked) ?'img/1square.svg' :'img/square.svg';
}
function changeColor6(t) {
    tr = t.parentNode;
    tr.style.color = (t.checked) ?"#FF6C0F" :"#7C7A7A";
    document.getElementById("left-seat").src = (t.checked) ?'img/1left-seat.svg' :'img/left-seat.svg';
}
function changeColor7(t) {
    tr = t.parentNode;
    tr.style.color = (t.checked) ?"#FF6C0F" :"#7C7A7A";
    document.getElementById("grid").src = (t.checked) ?'img/1grid.svg' :'img/grid.svg';
}

function reset() {
    location.reload(true);
}

/*function oneCheckbox(a) {
    const obj = document.getElementsByName("people");

    /*
    obj.forEach((cb) => {
        cb.checked = false;
    })
    a.checked = true;

    for(var i=0; i<obj.length; i++) {
        if (obj[i] != a) {
            obj[i].checked = false;
        }
    }
}*/