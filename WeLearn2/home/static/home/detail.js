function like(pk){
    var url = window.location.protocol+'//'+window.location.hostname+':'+window.location.port+'/pack/like/';
    var request = new XMLHttpRequest();
    request.open('POST', url);
    request.onload = ()=>{
        if(request.status == 200){
            var response = JSON.parse(request.responseText);
            var count = parseInt(document.getElementById('count-'+pk).innerHTML);
            if(response['liked']){
                count++;
                document.getElementById('like-'+pk).innerHTML = 'favorite';
                document.getElementById('count-'+pk).innerHTML = count;
            }
            else if(!response['liked']){
                count--;
                document.getElementById('like-'+pk).innerHTML = 'favorite_border';
                document.getElementById('count-'+pk).innerHTML = count;
            }    
        }
    };
    request.send(JSON.stringify({'pk':pk}));
}

function book(pk){
    var url = window.location.protocol+'//'+window.location.hostname+':'+window.location.port+'/pack/book/';
    var request = new XMLHttpRequest();
    request.open('POST', url);
    request.onload = ()=>{
        if(request.status == 200){
            var response = JSON.parse(request.responseText);
            if(response['marked']){
                document.getElementById('book-'+pk).innerHTML = 'bookmark';
            }
            else if(!response['marked']){
                document.getElementById('book-'+pk).innerHTML = 'bookmark_border';
            }    
        }
    };
    request.send(JSON.stringify({'pk':pk}));
}

function comment_like(pk){
    var url = window.location.protocol+'//'+window.location.hostname+':'+window.location.port+'/comment/like/';
    var request = new XMLHttpRequest();
    request.open('POST', url);
    request.onload = ()=>{
        if(request.status == 200){
            var response = JSON.parse(request.responseText);
            var count = parseInt(document.getElementById('comment-up-count-'+pk).innerHTML);
            if(response['liked']){
                count++;
                document.getElementById('comment-up-'+pk).style.color = 'blue';
                document.getElementById('comment-up-count-'+pk).innerHTML = count;
            }
            else if(!response['liked']){
                count--;
                document.getElementById('comment-up-'+pk).style.color = 'black';
                document.getElementById('comment-up-count-'+pk).innerHTML = count;
            }    
        }
    };
    request.send(JSON.stringify({'pk':pk}));
}

function reply_like(pk){
    var url = window.location.protocol+'//'+window.location.hostname+':'+window.location.port+'/reply/like/';
    var request = new XMLHttpRequest();
    request.open('POST', url);
    request.onload = ()=>{
        if(request.status == 200){
            var response = JSON.parse(request.responseText);
            var count = parseInt(document.getElementById('reply-up-count-'+pk).innerHTML);
            if(response['liked']){
                count++;
                document.getElementById('reply-up-'+pk).style.color = 'blue';
                document.getElementById('reply-up-count-'+pk).innerHTML = count;
            }
            else if(!response['liked']){
                count--;
                document.getElementById('reply-up-'+pk).style.color = 'black';
                document.getElementById('reply-up-count-'+pk).innerHTML = count;
            }    
        }
    };
    request.send(JSON.stringify({'pk':pk}));
}


function gettoday(){
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  var date = new Date();
  var day = date.getDate().toString();
  var month = monthNames[date.getMonth()];
  var year = date.getFullYear().toString();
  return `${day} ${month} ${year}`;
}

function comment_start(){
    document.getElementById('comment-input-area').style.display = 'block';
}

function comment_post(pk){
    var lt = /</g,gt = />/g,ap = /'/g,ic = /"/g;
    var input = document.getElementById('comment-input');
    var value = input.value.toString().replace(lt, "&lt;").replace(gt, "&gt;").replace(ap, "&#39;").replace(ic, "&#34;");
    if(value.length <= 0){
        document.getElementById('comment-input-error').style.display = 'block';
        input.style.borderColor = 'red';
    }
    else{
        var url = window.location.protocol+'//'+window.location.hostname+':'+window.location.port+'/comment/create/';
        var request = new XMLHttpRequest();
        request.open('POST',url);
        request.onload = ()=>{
            if(request.status == 200){
            var response = JSON.parse(request.responseText);
            if(response['added']){
                comment_end();
                var newComment = document.getElementById('temp-comment').cloneNode(true);
                newComment.setAttribute('id',`comment-set-${response['pk']}`);
                newComment.children[0].children[0].children[0].children[3].children[2].innerHTML = "commented " + gettoday();
                newComment.children[0].children[0].children[0].children[4].innerHTML = value;
                newComment.children[0].children[0].children[0].children[5].children[1].setAttribute('id',`comment-up-${response['pk']}`);
                newComment.children[0].children[0].children[0].children[5].children[1].children[0].setAttribute('onclick',`comment_like(${response['pk']})`);
                newComment.children[0].children[0].children[0].children[5].children[1].children[1].setAttribute('id',`comment-up-count-${response['pk']}`);
                newComment.children[1].setAttribute('id',`reply-section-${response['pk']}`);
                newComment.children[0].children[0].children[0].children[4].setAttribute('id',`comment-content-${response['pk']}`);
                newComment.children[0].children[0].children[0].children[5].children[0].setAttribute('id',`comment-edited-${response['pk']}`);
                newComment.children[0].children[0].children[0].children[0].children[1].children[0].setAttribute('onclick',`comment_edit_start(${response['pk']})`);
                newComment.children[0].children[0].children[0].children[5].children[2].children[0].setAttribute('id',`reply-btn-${response['pk']}`);
                newComment.children[0].children[0].children[0].children[5].children[2].children[0].setAttribute('onclick',`reply_start(${response['pk']})`);
                newComment.children[0].children[0].children[0].children[0].children[0].children[0].setAttribute('onclick',`comment_delete(${response['pk']})`);
                newComment.style.display = 'block';
                var section = document.getElementById('comment-section');
                section.insertAdjacentElement("afterbegin",newComment);
                var count = parseInt(document.getElementById('comments-count').innerHTML);
                count++;
                document.getElementById('comments-count').innerHTML = count;
            }
        }
    };
    request.send(JSON.stringify({'pack':pk,'content':value}));

    }
}

function comment_end(){
    document.getElementById('comment-input-area').style.display = 'none';
    document.getElementById('comment-input-error').style.display = 'none';
    document.getElementById('comment-input').style.borderColor = '';
    document.getElementById('comment-input').value = '';
}

function reply_start(pk){
    document.getElementById(`reply-btn-${pk}`).disabled = true;
    var reply = document.getElementById('reply-input-area').cloneNode(true);
    reply.setAttribute('id',`reply-input-area-${pk}`);
    reply.children[0].setAttribute('id',`reply-error-${pk}`);
    reply.children[1].children[0].setAttribute('id',`reply-input-${pk}`);
    reply.children[2].children[0].children[0].setAttribute('onclick',`reply_post(${pk})`);
    reply.children[2].children[1].children[0].setAttribute('onclick',`reply_end(${pk})`);
    reply.style.display = 'block';
    document.getElementById(`reply-section-${pk}`).insertAdjacentElement("afterbegin",reply)
}

function reply_post(pk){
    var lt = /</g,gt = />/g,ap = /'/g,ic = /"/g;
    var input = document.getElementById(`reply-input-${pk}`);
    var value = input.value.toString().replace(lt, "&lt;").replace(gt, "&gt;").replace(ap, "&#39;").replace(ic, "&#34;");
    if(value.length <= 0){
        document.getElementById(`reply-error-${pk}`).style.display = 'block';
        input.style.borderColor = 'red';
    }
    else{
        var url = window.location.protocol+'//'+window.location.hostname+':'+window.location.port+'/reply/create/';
        var request = new XMLHttpRequest();
        request.open('POST',url);
        request.onload = ()=>{
            if(request.status == 200){
                var response = JSON.parse(request.responseText);
                if(response['added']){
                reply_end(pk);
                var newReply = document.getElementById('temp-reply').cloneNode(true);
                newReply.setAttribute('id',`reply-${response['pk']}`);
                newReply.children[0].children[0].children[3].children[2].innerHTML = "replied " + gettoday();
                newReply.children[0].children[0].children[4].innerHTML = value;
                newReply.children[0].children[0].children[5].children[1].setAttribute('id',`reply-up-${response['pk']}`);
                newReply.children[0].children[0].children[0].children[1].children[0].setAttribute('onclick',`reply_edit_start(${response['pk']})`)
                newReply.children[0].children[0].children[4].setAttribute('id',`reply-content-${response['pk']}`);
                newReply.children[0].children[0].children[5].children[0].setAttribute('id',`reply-edited-${response['pk']}`);
                newReply.children[0].children[0].children[5].children[1].children[0].setAttribute('onclick',`reply_like(${response['pk']})`);
                newReply.children[0].children[0].children[5].children[1].children[1].setAttribute('id',`reply-up-count-${response['pk']}`);
                newReply.children[0].children[0].children[0].children[0].children[0].setAttribute('onclick',`reply_delete(${response['pk']})`);
                newReply.style.display = '';
                var section = document.getElementById(`reply-section-${pk}`);
                section.insertAdjacentElement("afterbegin",newReply);
                
            }

            }
        };

        request.send(JSON.stringify({'comment':pk,'content':value}));
    }
}

function reply_end(pk){
    var box = document.getElementById(`reply-input-area-${pk}`);
    box.parentNode.removeChild(box);
    document.getElementById(`reply-btn-${pk}`).disabled = false;
}

function comment_edit_start(pk){
    var value = document.getElementById(`comment-content-${pk}`).innerHTML;
    document.getElementById(`comment-set-${pk}`).children[0].style.display = 'none';
    var box = document.getElementById('update-input-area').cloneNode(true);
    box.setAttribute('id',`c-update-input-area-${pk}`);
    box.children[0].setAttribute('id',`c-update-error-${pk}`);
    box.children[1].children[0].setAttribute('id',`c-update-input-${pk}`);
    box.children[2].children[1].children[0].setAttribute('onclick',`comment_edit_end(${pk})`);
    box.children[2].children[0].children[0].setAttribute('onclick',`comment_edit_post(${pk})`);
    box.children[1].children[0].value = value.replace((/  |\r\n|\n|\r/gm),"");
    box.style.display = 'block';
    document.getElementById(`comment-set-${pk}`).insertAdjacentElement("afterbegin",box);
}

function comment_edit_post(pk){
    var lt = /</g,gt = />/g,ap = /'/g,ic = /"/g;
    var input = document.getElementById(`c-update-input-${pk}`);
    var value = input.value.toString().replace(lt, "&lt;").replace(gt, "&gt;").replace(ap, "&#39;").replace(ic, "&#34;");
    if(value.length <= 0){
        document.getElementById(`c-update-error-${pk}`).style.display = 'block';
        input.style.borderColor = 'red';
    }
    else{
        var url = window.location.protocol+'//'+window.location.hostname+':'+window.location.port+'/comment/edit/';
        var request = new XMLHttpRequest();
        request.open('POST',url);
        request.onload = ()=>{
            if(request.status == 200){
                var response = JSON.parse(request.responseText);
                if(response['added']){
                    document.getElementById(`comment-content-${pk}`).innerHTML = value;
                    document.getElementById(`comment-edited-${pk}`).style.display = 'inline';
                    comment_edit_end(pk);
                }
            }
        };
        request.send(JSON.stringify({'comment':pk,'content':value}));
    }
}

function comment_edit_end(pk){
    var box = document.getElementById(`c-update-input-area-${pk}`);
    box.parentNode.removeChild(box);
    document.getElementById(`comment-set-${pk}`).children[0].style.display = '';   
}

function reply_edit_start(pk){
    var value = document.getElementById(`reply-content-${pk}`).innerHTML;
    document.getElementById(`reply-${pk}`).style.display = 'none';
    var box = document.getElementById('update-input-area').cloneNode(true);
    box.setAttribute('id',`r-update-input-area-${pk}`);
    box.children[0].setAttribute('id',`r-update-error-${pk}`);
    box.children[1].children[0].setAttribute('id',`r-update-input-${pk}`);
    box.children[2].children[1].children[0].setAttribute('onclick',`reply_edit_end(${pk})`);
    box.children[2].children[0].children[0].setAttribute('onclick',`reply_edit_post(${pk})`);
    box.children[1].children[0].value = value.replace((/  |\r\n|\n|\r/gm),"");
    box.style.display = 'block';
    document.getElementById(`reply-${pk}`).insertAdjacentElement("beforebegin",box);
}

function reply_edit_post(pk){
    var lt = /</g,gt = />/g,ap = /'/g,ic = /"/g;
    var input = document.getElementById(`r-update-input-${pk}`);
    var value = input.value.toString().replace(lt, "&lt;").replace(gt, "&gt;").replace(ap, "&#39;").replace(ic, "&#34;");
    if(value.length <= 0){
        document.getElementById(`r-update-error-${pk}`).style.display = 'block';
        input.style.borderColor = 'red';
    }
    else{
        var url = window.location.protocol+'//'+window.location.hostname+':'+window.location.port+'/reply/edit/';
        var request = new XMLHttpRequest();
        request.open('POST',url);
        request.onload = ()=>{
            if(request.status == 200){
                var response = JSON.parse(request.responseText);
                if(response['added']){
                    document.getElementById(`reply-content-${pk}`).innerHTML = value;
                    document.getElementById(`reply-edited-${pk}`).style.display = 'inline';
                    reply_edit_end(pk);
                }
            }
        };
        request.send(JSON.stringify({'reply':pk,'content':value}));

    }


}


function reply_edit_end(pk){
    var box = document.getElementById(`r-update-input-area-${pk}`);
    box.parentNode.removeChild(box);
    document.getElementById(`reply-${pk}`).style.display = '';

}

function comment_delete(pk){
    if(confirm('Are you sure you want to delete this comment?')){
        var url =  window.location.protocol+'//'+window.location.hostname+':'+window.location.port+'/comment/delete/';
        var request = new XMLHttpRequest();
        request.open('POST',url);
        request.onload = ()=>{
            if(request.status == 200){
                var response = JSON.parse(request.responseText);
                if(response['deleted']){
                    var comment = document.getElementById(`comment-set-${pk}`);
                    comment.parentNode.removeChild(comment);
                    var count = parseInt(document.getElementById('comments-count').innerHTML);
                    count --;
                    document.getElementById('comments-count').innerHTML = count;
                }
            }
        };
        request.send(JSON.stringify({'pk':pk}));
    } 
}


function reply_delete(pk){
    if(confirm('Are you sure you want to delete this reply?')){
        var url =  window.location.protocol+'//'+window.location.hostname+':'+window.location.port+'/reply/delete/';
        var request = new XMLHttpRequest();
        request.open('POST',url);
        request.onload = ()=>{
            if(request.status == 200){
                var response = JSON.parse(request.responseText);
                if(response['deleted']){
                    var reply = document.getElementById(`reply-${pk}`);
                    reply.parentNode.removeChild(reply);
                }
            }
        };
        request.send(JSON.stringify({'pk':pk}));
    } 
}