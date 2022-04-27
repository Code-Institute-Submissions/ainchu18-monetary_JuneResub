const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
tableOutput.style.display = "none";
const tBody = document.querySelector(".tbody");
const noResults = document.querySelector(".no-results");

searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        paginationContainer.style.display = "none";
        tBody.innerHTML = "";

        fetch("/search-expense", {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
        }).then((res) => res.json()).then((data) => {
            console.log("data", data);
            appTable.style.display = "none";
            tableOutput.style.display = "block";

            if (data.length === 0) {
                noResults.style.display = "block";
                tableOutput.style.display = "none";
                paginationContainer.style.display = "none";
            } else {
                noResults.style.display = "none";
                data.forEach(item => {
                    tBody.innerHTML += `
                        <tr>
                            <td>${item.amount}</td>
                            <td>${item.description}</td>
                            <td>${item.category}</td>
                            <td>${item.date}</td>
                        </tr>`;     
                }); 
            }
        });

    } else {
        noResults.style.display = "none";
        tableOutput.style.display = "none"
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
    }

});