    



    function edit_details(){
        document.getElementById("edit_div").style.display = "block";
      }


    function getdata(){
    var s_id = $("#sports").val();
    console.log(s_id);
    $.ajax({
        
      type: "POST",
      url: "getground",
      data:  '{"id" : '+s_id+'}',
      contentType: "application/json",
      dataType: "json",
      success: function( result ) {
    
          $("#ground option").remove();
                            for (var i = result.length - 1; i >= 0; i--) {
                              console.log(result[i].id);
                                $("#ground").append('<option value='+result[i].id+' id='+result[i].id+'>'+ result[i].name +'</option>');
                            };
                            
      }
  });
      }


      

      
     


      
      

        





