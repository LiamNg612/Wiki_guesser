let fir=0;
$(document).ready(function () {
  $("form").submit(function (event) {

       let form = $(this);
       console.log(form.serialize());
    $.ajax({
      type: "POST",
      url: "/check",
      data: form.serialize(),
    }).done(function (data) {
      console.log(data);
      if(data=="True"){
          $("#response").html("You are right");
          $("#content").append("<form action='/game' id='refresh' method='POST'><input type='submit' style='margin: 12px 0px;' value='Next question'></form>");
      }
      else{ $("#response").html("You are Wrong");
      if(fir==0){
        fir=1;
        $("#content").append("<form action='/game' id='refresh' method='POST'><input type='submit' style='margin: 12px 0px;' value='Skip'></form>");}

    }
    });

    event.preventDefault();
  });
});