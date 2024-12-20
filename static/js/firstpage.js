window.onload = function () {
    // Check if a theme is saved in localStorage, otherwise default to light theme
    const savedTheme = localStorage.getItem('theme') || 'light'; 
    document.body.setAttribute('data-theme', savedTheme);
    
    // Apply the correct theme logos based on the current theme
    updateThemeLogo(savedTheme);

    // Fetch data for treeview as before
    fetch('/get_data')
        .then(response => response.json())
        .then(data => populateTreeView(data))
        .catch(error => console.error('Error loading data:', error));
};
function populateTreeView(data) {
    const treeview = document.getElementById('treeview');
    for (let db_name in data) {
        const dbItem = document.createElement('li');
        dbItem.classList.add('db');
        dbItem.textContent = `+ ${db_name}`;
        const tableList = document.createElement('ul');
        tableList.style.display = 'none';  // Initially collapsed
        dbItem.appendChild(tableList);

        for (let table_name in data[db_name]) {
            const tableItem = document.createElement('li');
            tableItem.classList.add('table');
            tableItem.textContent = table_name;
            const columnList = document.createElement('ul');
            columnList.style.display = 'none';  // Initially collapsed
            tableItem.appendChild(columnList);

            for (let column_name of data[db_name][table_name]) {
                const columnItem = document.createElement('li');
                columnItem.classList.add('column');
                columnItem.textContent = column_name;
                columnList.appendChild(columnItem);
            }

            tableItem.addEventListener('click', () => {
                columnList.style.display = columnList.style.display === 'none' ? 'block' : 'none';
            });

            tableList.appendChild(tableItem);
        }

        dbItem.addEventListener('click', () => {
            tableList.style.display = tableList.style.display === 'none' ? 'block' : 'none';
        });

        treeview.appendChild(dbItem);
    }
}
function updateThemeLogo(theme) {
    if (theme === 'dark') {
        document.body.setAttribute('data-theme', 'dark');
    } else {
        document.body.setAttribute('data-theme', 'light');
    }
}
function closeToast() {
    document.getElementById('toastPanel').classList.remove('active');
}
function redirectToLogout() {
    window.location.href = '/logout';
}
const themeButton = document.getElementById('theme-switcher');
function toggleTheme() {
    const currentTheme = document.body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.body.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);
    updateThemeLogo(newTheme);
}
function redirectToChangePassword() {
    window.location.href = '/change_password';
}
function toggleSidePanel() {
    const panel = document.getElementById('mySidePanel');
    panel.style.width = panel.style.width === '250px' ? '0' : '250px';
}
let isResizing = false;
function initResize(e) {
    isResizing = true;
    window.addEventListener('mousemove', resize);
    window.addEventListener('mouseup', stopResize);
}
function resize(e) {
    if (isResizing) {
        const panel = document.getElementById('mySidePanel');
        panel.style.width = Math.max(e.clientX, 250) + 'px';
    }
}
function stopResize() {
    isResizing = false;
    window.removeEventListener('mousemove', resize);
    window.removeEventListener('mouseup', stopResize);
}
const textarea = document.querySelector('.query-input');
textarea.addEventListener('input', () => {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 160) + 'px';
});
function sendMessage() {
    const textarea = document.querySelector('.query-input');
    const textBox = document.getElementById('dynamicTextBox');
    const sqlQueryBox = document.getElementById('sql-query');
    const sqlDataBox = document.getElementById('sql-data');

    const userInput = textarea.value;

    // Display the input query in the dynamic text box
    textBox.textContent = userInput;

    // Make a POST request to the Flask backend to process the query
    fetch('/process_query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: userInput })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update SQL query and SQL data from the backend response
            sqlQueryBox.textContent = data.query_result ? data.query_result : "No query results.";
            sqlDataBox.textContent = data.message ? data.message : "Query executed successfully.";
        } else {
            // Handle errors
            sqlQueryBox.textContent = "Error generating SQL query.";
            sqlDataBox.textContent = data.message || "An error occurred while processing your request.";
        }
    })
    .catch(error => {
        // Handle fetch errors
        sqlQueryBox.textContent = "Error connecting to the server.";
        sqlDataBox.textContent = `Error details: ${error}`;
    });

    // Reset the input field
    textarea.value = '';
}        
function toggleSettingsPanel() {
    const panel = document.getElementById('settingsPanel');
    panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
}
function changePassword() {
    alert("Change password functionality goes here!");
}