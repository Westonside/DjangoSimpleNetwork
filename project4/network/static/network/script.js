// import {script} from '../..templates/network/index.html'



//transition this javascript to the react dom
document.addEventListener('DOMContentLoaded', () =>{
    
    //when the document loads start with loading the all posts
    // loadPage("following");

    document.querySelector('#follow_button').onclick = followUser;
    document.querySelector('#allPosts').addEventListener('click', () => loadPage("All Posts"));
    if(document.querySelectorAll('.nav-item').length === 4)
    {
        document.querySelector('#following').addEventListener('click', () => loadPage("Following"));
        document.querySelector('#username').addEventListener('click', () => loadPage(document.querySelector('#username').innerHTML));
        // document.querySelector('#follow_button').addEventListener('click', () => followUser(document.querySelector('#user_title').innerHTML));

    }
    
    
    // find how to access the content of the reacyt
    // console.log(document.querySelector('#new_post_but'));
    loadPage("All Posts");
    document.querySelector('#follow_button').style.display = 'none';
});

function loadPage(pageNum)
{
    //hide the follow button
    document.querySelector('#follow_button').style.display = 'none';
    // console.log(pageNum);
    // history.pushState({'title':pageNum}, pageNum,pageNum)
    if(pageNum ==="Following" || pageNum ==="All Posts")
    {
        // history.pushState({'title':pageNum}, pageNum,pageNum)
        document.title = pageNum;
        document.querySelector('#user_profile_view').style.display = 'none';
        // document.querySelector('#basic_profile').style.display = 'block';
        document.querySelector('#posts').style.display = 'block';
        document.querySelector('.container-fluid').style.display = 'block';
        // document.querySelector('.follow_button').style.display = 'none';
        
        
    }
    else if(pageNum === document.querySelector('#username').innerHTML){
        let title = document.querySelector('#user_title').innerHTML;
        document.title = title.substring(title);
        document.querySelector('#user_profile_view').style.display = 'block';
        console.log('username section!', document.querySelector('#user_title').innerHTML === document.querySelector('#username').innerHTML);
        if(document.querySelector('#user_title').innerHTML === document.querySelector('#username').innerHTML)
        {
            document.querySelector('#follow_button').style.display = 'none';
        }
        document.querySelector('#posts').style.display = 'block';
        document.querySelector('.container-fluid').style.display = 'none';
        // document.querySelector('.follow_user').style.display = 'block';
        // document.querySelector('.follow_user').style.display = 'block';
      
        // document.querySelector('follow_button').style.display = 'block';
        //make a fetch request to update posts div
        // document.querySelector('#popup_page').style.display = 'none';
        
        profileViewer();
    }
    
}

function profileViewer()
{
    console.error('profileViewer');
    document.querySelector('#user_title').innerHTML = document.querySelector('#username').innerHTML;
    document.title = document.querySelector('#username').innerHTML;
}
// window.onpopstate = function(event){
//     loadPage(event.state.title);
// }



function followUser()
{
    
    let followBut = document.querySelector('#follow_button');
    console.log('follow user place', document.querySelector('#user_title').innerHTML);
    fetch(`followUser/${document.querySelector('#user_title').innerHTML}`)
    .then(response => response.json())
    .then(result =>{
        console.log(result);
        
    });

    //make a fetch request that is a get request? or a post
    
}