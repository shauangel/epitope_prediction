var select_range=[]
var textlong

function reset(){
    for(var a=0;a<6;a++){
        select_range[a]=50;
    }
    textlong=5;
}

function more_set(){
    var left = document.getElementById("more_set");
    var mes="";
    mes+='<tr><td>LEPS</td><td><input type="range" min="0" max="100" value="'+select_range[0]+'" class="Slider" id="select0"></input></td><td id="show0">'+select_range[0]/100+'</td></tr>'
        +'<tr><td>BCpreds</td><td><input type="range" min="0" max="100" value="'+select_range[1]+'" class="Slider" id="select1"></input></td><td id="show1">'+select_range[1]/100+'</td></tr>'
        +'<tr><td>BepiPred-2</td><td><input type="range" min="0" max="100" value="'+select_range[2]+'" class="Slider" id="select2"></input></td><td id="show2">'+select_range[2]/100+'</td></tr>'
        +'<tr><td>ABCPred</td><td><input type="range" min="0" max="100" value="'+select_range[3]+'" class="Slider" id="select3"></input></td><td id="show3">'+select_range[3]/100+'</td></tr>'
        +'<tr><td>Bcepred</td><td><input type="range" min="0" max="100" value="'+select_range[4]+'" class="Slider" id="select4"></input></td><td id="show4">'+select_range[4]/100+'</td></tr>'
        +'<tr><td>LBtope</td><td><input type="range" min="0" max="100" value="'+select_range[5]+'" class="Slider" id="select5"></input></td><td id="show5">'+select_range[5]/100+'</td></tr>'
        +'<tr><td>最短長度</td><td><input type="range" min="1" max="20" value="'+textlong+'" class="Slidert" id="textlong"></input></td><td id="tl">'+textlong+'</td></tr>';
    left.innerHTML = mes;
    //document.getElementById("select1").addEventListener("oninput", function(){select_range[0]=100}, false);
    //document.getElementById("test").addEventListener("click", function(){alert(select_range[0])}, false);
    document.getElementById("select0").oninput=function(){
        
        select_range[0]=parseInt(this.value);
        document.getElementById("show0").innerHTML=select_range[0]/100;
    }
    document.getElementById("select1").oninput=function(){
        select_range[1]=parseInt(this.value);
        document.getElementById("show1").innerHTML=select_range[1]/100;
    }
    document.getElementById("select2").oninput=function(){
        select_range[2]=parseInt(this.value);
        document.getElementById("show2").innerHTML=select_range[2]/100;
    }
    document.getElementById("select3").oninput=function(){
        select_range[3]=parseInt(this.value);
        document.getElementById("show3").innerHTML=select_range[3]/100;
    }
    document.getElementById("select4").oninput=function(){
        select_range[4]=parseInt(this.value);
        document.getElementById("show4").innerHTML=select_range[4]/100;
    }
    document.getElementById("select5").oninput=function(){
        select_range[5]=parseInt(this.value);
        document.getElementById("show5").innerHTML=select_range[5]/100;
    }
    document.getElementById("textlong").oninput=function(){
        textlong=parseInt(this.value);
        document.getElementById("tl").innerHTML=textlong;
    }
}

function check(){
    const rule0=/^>/;
    const rule1=/[A-Z]/;
    var mask=0;
    var f_data=document.getElementById("fasta").value;
    var o_data=document.getElementById("other_fasta").value;
    var f_Array = f_data.split("\n");
    
    //console.log(rule0.test(f_Array[0]));
    //console.log(rule1.test(f_Array[1]));
    if(rule0.test(f_Array[0])!==true){
        alert("主目標的fasta開頭要符合格式哦");
        mask++;
    }
    if(rule1.test(f_Array[1])!==true){
        alert("主目標的fasta內容要符合格式哦");
        //alert(f_Array[1]);
        mask++;
    }
    if(o_data!=""){
        var o_Array = o_data.split("\n");
        for(var a=0;a<o_Array.length;a++){
            if(rule0.test(o_Array[a])!==true){
                alert("additon_fasta開頭要符合格式哦");
                mask++;
            }
            if(rule1.test(o_Array[a+1])!==true){
                alert("additon_fasta內容要符合格式哦");
                mask++;
            }
            a++;
        }
    }
    /*if (data==""){
        alert("必須要放主目標的fasta的資料哦");
        mask++;
    }
    else{
        var Array = data.split(">");
        if(data[0]!=">"){
            alert("請用>當fasta標題的開頭");
            mask++;
        }
        
    }*/
    if(mask==0){send_message();}
}

function start(){
    reset();
    document.getElementById("more").addEventListener("click", more_set, false);
    document.getElementById("submit").addEventListener("click", send_message, false);
}

window.addEventListener("load", start, false);