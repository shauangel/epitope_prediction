var result="wertyuiokjhgfdsxcvbnmmwertyuiokjhgfdsxcvbnmm";
//var vote= "01234560000002345000230012345000000234500023";
var v_ABCPred=[],v_BCpreds=[],v_Bcepred=[],v_BepiPred=[],v_LBtope=[],v_LEPS=[];
var vote=[];
var result_len=0;
var range=["2-7","14-17","21-22","25-29","36-39","43-44"];
var range_int=[];
var seq=["rtyui","dsxc","mm","rtyui","dsxc","mm"];
var forward=-1;
/*
{
    "result" : "",
    "vote" : "",
    "epitope" : [
        {
            "range" : "",
            "seq" : ""
        }, {},...,{}
    ]
}
*/

function data_processing(e){

    result=e.result;
    result_len=e.result.length;
    for(var a=0;a<result_len;a++){
        /*
        v_ABCPred[a]=parseInt(e.vote_6sys.ABCPred[a]);
        v_BCpreds[a]=parseInt(e.vote_6sys.BCpreds[a]);
        v_Bcepred[a]=parseInt(e.vote_6sys.Bcepred[a]);
        v_BepiPred[a]=parseInt(e.vote_6sys.BepiPred[a]);
        v_LBtope[a]=parseInt(e.vote_6sys.LBtope[a]);
        v_LEPS[a]=parseInt(e.vote_6sys.LEPS[a]);
        */
        vote[a]=e.vote[a];
    }

    for(var a=0;a<e.epitope.length;a++){
        range[a]=e.epitope[a].range;
        seq[a]=e.epitope[a].seq;
    }

    /*for(var a=0;a<vote.length;a++){
        vote_int[a]=parseInt(vote[a]);
    }*/
    var b=0;
    for(var a=0;a<range.length;a++){
        //var NewArray = parseInt(range[a].split("~"),10);
        var Array = range[a].split("-");
        var NewArray=[parseInt(Array[0],10),parseInt(Array[1],10)];
        range_int[b]=NewArray[0]-forward-1;
        b++;
        range_int[b]=NewArray[1]-NewArray[0]+1;
        b++;
        forward=NewArray[1];
    }
}


function show(e){
    data_processing(e);
    var showshow = document.getElementById("menu");
    var mes="";
    mes+='<p><table id="range_table" class="show_table">'+
         '<tr><td>tatol</td><td colspan="3">'+select_range[0]/100+'</td></tr>'+
         '<tr><td>LEPS</td><td>'+select_range[0]/100+'</td><td>ABCPred</td><td>'+select_range[3]/100+'</td></tr>'+
         '<tr><td>BCpreds</td><td>'+select_range[1]/100+'</td><td>Bcepred</td><td>'+select_range[4]/100+'</td></tr>'+
         '<tr><td>BepiPred-2</td><td>'+select_range[2]/100+'</td><td>LBtope</td><td>'+select_range[5]/100+'</td></tr>'+
         '</table></p>';

    mes+='<p><div class="show_table" style="text-align:center;"><font>Prediction result</font>'+
         '<div class="float"><table id="fasta_epitope"><colgroup>';
    for(var a=0;a<range_int.length;a++){
        if(a%2==0){mes+='<col span="'+range_int[a]+'" class="origin"></col>';}
        else{mes+='<col span="'+range_int[a]+'" class="highlight"></col>';}
    }
    mes+='<tr>';
    for(var a=0;a<result.length;a++){
        mes+='<td style="padding:1px 5px;">'+result[a]+'</td>';
    }
    mes+='</tr><tr style="color:white;">';
    for(var a=0;a<vote.length;a++){
        mes+='<td class="votecolor'+vote[a]+'">'+vote[a]+'</td>';
    }
    mes+='</tr></table></div></div></p><p><table id="epitope_table" class="show_table">'+
         '<col span="1" bgcolor="#8BC795" width=100px></col>'+
         '<col span="1" bgcolor="#C5E0C2" width=400px></col>';
    for(var a=0;a<range.length;a++){
        mes+='<tr><td>'+range[a]+'</td><td>'+seq[a]+'</td></tr>';
    }
    mes+="</table></p>"
    showshow.innerHTML = mes;
}