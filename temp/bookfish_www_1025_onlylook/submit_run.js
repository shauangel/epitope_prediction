function send_message(){
    /*
    var json_text={
        "title" : document.getElementById("title").value,
        "data" : document.getElementById("fasta").value+"\n\n"+document.getElementById("other_fasta").value,
        "shortest" : textlong,
        "range" : {
            "LEPS" : select_range[1],
            "BCpreds" : select_range[2],
            "BepiPred-2" : select_range[3],
            "ABCPred" : select_range[4],
            "Bcepred" : select_range[5],
            "LBtope" : select_range[6],
        }
    };
    //alert(typeof select_range[0])
    console.log(
        JSON.stringify(json_text)  // 序列化成 JSON 字串
    );
    //document.getElementById("menu").innerHTML="";
    $.ajax({
        url: "http://127.0.0.1:5000/prediction",
        type: "POST",
        data : JSON.stringify(json_text),
        dataType: "json",
        contentType: "application/json; charset=utf-8",
       
        success: function(data){
            console.log(data);
        },
        
        error: function(){
        //window.alert('uh oh :(');        
        }
    });
    */
    show();

}


//接PYTHON的地方
