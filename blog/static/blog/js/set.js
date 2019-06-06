var back = document.getElementById('back');
var forward = document.getElementById('forward');

function GetData(){
    //var div1 = document.getElementById("div1");
    function success(response){
        //div1.innerHTML = response;
    }
    GET("/?page=1",success,"txt");
}

//back.onclick = function(){
//	alert("back")
//}

//forward.onclick = function(){
//	alert("fwd")
//}

back.onclick = GetData;
