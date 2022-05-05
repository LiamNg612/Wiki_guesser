
let first=0;
let hints="";
let showed=0;
let all=0;
let pic;
function getHint(){//when pressing the hints button will get new para
    if(first!=1){
    let sentence=$("#sentence").html();
    hints = sentence.split(".");
    pic=$("#pic").html();
    pic=pic.split("\n");

    const substring = 'https';
    const matches = pic.filter(element => {
    if (element.indexOf(substring) !== -1) {
    return true;
    }
    });
    for(let i=0;i<matches.length;i++){
        matches[i]=matches[i].replaceAll(" ", "");
    }
    hints.pop();
    pic=matches;

    first=1;
    }
    console.log(pic.length);
    console.log(hints);
    if(hints.length==0){

        if(all!=1){
            $("#para").append("<li>Shown all hints</li>");
            //$("<li>Shown all hints</li>").insertBefore("#para");
            $( "#start_btn" ).remove();
            $("#para").append("<button id='pic_button' onclick='getPic(pic)'>Show Picture</button>");
            all=1;
        }
        return 1;
    }
    show="";
    while(show.length<5){
        var ran=Math.floor(Math.random() * (hints.length-1) );
        var show=hints[ran];
        if(ran==hints.length){
        hints.splice(ran, 0);
    }else hints.splice(ran, 1);
    }
    if(showed==0){
        $("#para").append(" <li> "+show+" </li>");
        //$(" <li> "+show+" </li>").insertBefore("#para");
    }else $("#para").append(" <li> "+show+" <br>You have used " +showed+" hint(s)</li>");

    $("#start_btn").html("Get hint");
    showed+=1;
}
function getPic(picture){
    console.log(picture.length);
    if(picture.length>0){
    $("<img src='"+picture[picture.length-1]+"'><div>You have used "+showed+ " hint(s)</div>"  ).insertBefore("#pic_button");
    picture=picture.pop();
    showed++;
     if(pic.length==0){
            showed--;
            $("#pic_button").html("No more hints");
        }
    }
}

function rankCorrect(result){
    console.log("correct");
    $.ajax({
      type: "POST",
      url: "/leaderboard",
      data: {correct:"T"}
    }).done(function (data) {
      console.log(data);
      $( "table" ).replaceWith( data );
    });
}
function rankByQuestion(){
    console.log("question");
     $.ajax({
      type: "POST",
      url: "/leaderboard",
      data: {question:"T"}
    }).done(function (data) {
      console.log(data);
      $( "table" ).replaceWith( data );
    });
}