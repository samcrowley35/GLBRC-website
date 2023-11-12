// Sends post request to the backend
function changeStatus(id){
    fetch('/change-status', {
        method: 'POST',
        body: JSON.stringify({id:id})
    }).then((_res) => {
        window.location.href = '/'
    });
}