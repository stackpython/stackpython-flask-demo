// Single line comment

/* This is multi lines comment
you can comment many lines as you want*/

var a = "10"; // String
var b = "20"; // String
var result = a + b;
var newA = 10; // Number
var newB = 20; // Number
var result2 = newA + newB;

// Display to console
console.log("Total1:", result)  
console.log("Total2:", result2)  

// Loop
for (let i = 1; i <= 10; i++) {
    // console.log("Loop is running")
    console.log(i)
}

// Create a function
function getNum() {
    var val1 = 50;
    var val2 = 40;
    var result = val1 - val2;
    console.log("result is:", result)
}

// Call a function
getNum();

function myFunc1() {
    document.getElementById("id1").innerHTML = "Change to STACKPYTHON";
}

function myFunc2() {
    document.getElementById("id2").style.fontSize = "140px";
}

// Conditional statement and function
function myFunc3() {
    var msg;
    if(confirm("You must click OK to continue or CANCEL to cancel")){
        msg = "You pressed OK"
    }
    else {
        msg = "You pressed CANCEL"
    }
    document.getElementById("id3").innerHTML = msg;
}