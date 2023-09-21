document.addEventListener('DOMContentLoaded', function () {
    const postForm = document.getElementById('post-form');
    const postContent = document.getElementById('post-content');
    const editButton = document.getElementById('edit-button');

    postForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        const content = postContent.value.trim();
        if (content === '') {
            // Handle empty content if needed
            return;
        }

        // Create a FormData object and append the content to it
        const formData = new FormData();
        formData.append('content', content);

        // Send a POST request using fetch
        fetch('/create_post', {
            method: 'POST',
            body: formData,
        })
            .then(response => {
                if (response.ok) {
                    // The post was successfully created, you can update the UI as needed
                    postContent.value = ''; // Clear the input field
                    return response.json();
                } else {
                    throw new Error('Failed to create the post');
                }
            })
            .then(result => {
                console.log(result);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

});

