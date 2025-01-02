// Opens Handle in New Tab 
function goDeveloperProfile() {
    const profileUrl = 'https://codeforces.com/profile/sapaul';
    
    //  Creating a New tab 
    chrome.tabs.create({ url: profileUrl });
}

// Opening Developer's Handle on Click
document.addEventListener('DOMContentLoaded', function () {
    const developerHandleID = document.getElementById('developerHandle');
    const developerContactID = document.getElementById('developerContact');
    
    // Click on Developer Contact Section 
    developerHandleID.addEventListener('click', goDeveloperProfile);
    developerContactID.addEventListener('click', goDeveloperProfile);
});




