// JavaScript function
function showProjects() {
    const projectList = document.getElementById('project-list');
    if (projectList.style.display === 'none') {
        projectList.style.display = 'block';
    } else {
        projectList.style.display = 'none';
    }
}