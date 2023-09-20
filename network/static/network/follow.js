document.addEventListener('DOMContentLoaded', function(){

    const followButton = document.getElementById('follow-button');
    const unfollowButton = document.getElementById('unfollow-button');
    const profileUserDiv = document.getElementById('profile-user');

    const username = profileUserDiv.getAttribute('data-username');

    followButton.addEventListener('click', () => {
        toggleFollow(username);
    });

    unfollowButton.addEventListener('click', () => {
        toggleUnfollow(username);
    });

    function toggleFollow(username) {
        fetch(`/follow/${username}`, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            // if(data.message){
            //     alert(data.message); // Show a success message (optional)
            // }
            if(data.redirect_url){
                window.location.href = data.redirect_url;
            }
            followButton.style.display = 'none';
            unfollowButton.style.display = 'block';
        })
        .catch(error => {
            alert('Error: ' + error.message); // Show an error message (optional)
        });
    }

    function toggleUnfollow(username) {
        fetch(`/unfollow/${username}`, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            // if(data.message){
            //     alert(data.message); // Show a success message (optional)
            // }
            if(data.redirect_url){
                window.location.href = data.redirect_url;
            }
            followButton.style.display = 'block';
            unfollowButton.style.display = 'none';
        })
        .catch(error => {
            alert('Error: ' + error.message); // Show an error message (optional)
        });
    }
});