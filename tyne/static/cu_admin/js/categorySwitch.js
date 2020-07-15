/* 
    Helps toogle between two diffrent states of a Category 
        i.e. album_category = true | false
    Toogles the inputs for artists and albums to help avoid errors when data is being processed
*/

const __categorySwitch = function () {
    const albumCategory = document.getElementById('id_album_category');

    if (albumCategory !== null) {
        // only if it has checked attribute

        if (albumCategory.hasAttribute('checked')) {
            // get the artists and albums field!
            const artistsChoices = document.getElementById('id_artist_items');
            const albumChoices = document.getElementById('id_album_items');
            const artistsField = artistsChoices.parentElement.parentElement;
            const albumField = albumChoices.parentElement.parentElement;

            // inital hiding of artists
            artistsField.style.display = 'none';
            artistsChoices.value = '';

            // add a listener to album category for change event
            albumCategory.addEventListener('change', () => {
                if (albumCategory.checked) {
                    artistsField.style.display = 'none';
                    artistsChoices.value = '';
                    albumField.style.display = '';
                } else {
                    artistsField.style.display = '';
                    albumField.style.display = 'none';
                    albumChoices.value = '';
                };
            });
        };
    };
};
    

document.addEventListener('readystatechange', () => {
    if (document.readyState === 'complete') {
        __categorySwitch();
    };
});
