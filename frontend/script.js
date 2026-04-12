const form = document.getElementById("carbonForm");
const result = document.getElementById("result");

form.addEventListener("submit", async function(e){

    e.preventDefault();

    const data = {
        energy_kwh: Number(document.getElementById("energy_kwh").value),
        month: Number(document.getElementById("month").value),
        state: document.getElementById("state").value,
        usage_type: document.getElementById("usage_type").value,
        season: document.getElementById("season").value
    };

    result.innerHTML = "Calculando...";

    try{

        const response = await fetch("http://92.246.131.104:8000/compare",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body: JSON.stringify(data)

        });

        if(!response.ok){
            throw new Error("Erro na API");
        }

        const json = await response.json();

        mostrarResultado(json);

    }
    catch(error){

        result.innerHTML = "Erro ao conectar com a API.";

        console.error(error);

    }

});


function mostrarResultado(data){

    let html = "<h3>Resultado da comparação</h3>";

    html += "<ul>";

    for(const fonte in data){

        html += `<li><strong>${fonte}</strong>: ${data[fonte]} kg CO₂</li>`;

    }

    html += "</ul>";

    result.innerHTML = html;

}