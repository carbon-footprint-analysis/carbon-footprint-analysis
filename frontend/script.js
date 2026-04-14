const form = document.getElementById("carbonForm");
const result = document.getElementById("result");
const metrics = document.querySelector(".model-metrics");

let chart; // evita duplicar gráfico


form.addEventListener("submit", async function(e){

    e.preventDefault();

    const data = {
        energy_kwh: Number(document.getElementById("energy_kwh").value),
        month: Number(document.getElementById("month").value),
        state: document.getElementById("state").value,
        usage_type: document.getElementById("usage_type").value,
        season: document.getElementById("season").value
    };

    result.innerHTML = "Calculando emissões...";

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

    // ordena ranking do menor para o maior
    const sorted = Object.entries(data).sort((a,b)=>a[1]-b[1]);

    let html = "<h3>Resultado da comparação</h3>";
    html += "<ul>";

    sorted.forEach(([fonte, valor])=>{

        html += `<li><strong>${formatarFonte(fonte)}</strong>: ${valor.toFixed(2)} kg CO₂</li>`;

    });

    html += "</ul>";

    result.innerHTML = html;


    const labels = sorted.map(item => formatarFonte(item[0]));
    const values = sorted.map(item => item[1]);



    // cores automáticas baseadas na fonte
    const colors = sorted.map(item => {

        const fonte = item[0].toLowerCase();

        if(fonte.includes("hidre")) return "#2ecc71";
        if(fonte.includes("eol")) return "#27ae60";
        if(fonte.includes("nuclear")) return "#2ecc71";
        if(fonte.includes("solar")) return "#f1c40f";

        if(fonte.includes("ethanol")) return "#e67e22";

        return "#e74c3c"; // combustíveis fósseis

    });



    const ctx = document.getElementById("chart");

    // destrói gráfico antigo se existir
    if(chart){
        chart.destroy();
    }

    chart = new Chart(ctx, {

        type: "bar",

        data: {
            labels: labels,
            datasets: [{

                label: "Emissão de CO₂ (kg)",

                data: values,

                backgroundColor: colors,

                borderRadius: 6

            }]
        },

        options: {

            responsive: true,

            animation:{
                duration:900
            },

            plugins:{

                legend:{
                    display:false
                },

                tooltip:{
                    callbacks:{
                        label:function(context){

                            return context.raw.toFixed(2) + " kg CO₂";

                        }
                    }
                }

            },

            scales:{

                y:{

                    beginAtZero:true,

                    title:{
                        display:true,
                        text:"Emissão de CO₂ (kg)"
                    }

                },

                x:{

                    ticks:{
                        autoSkip:false
                    }

                }

            }

        }

    });
result.style.display = "block";
metrics.style.display = "block";
}



function formatarFonte(fonte){

    const nomes = {

        hidreletrica:"Hidrelétrica",
        eolica:"Eólica",
        nuclear:"Nuclear",
        solar:"Solar",
        termica:"Térmica",
        ethanol:"Etanol",
        diesel:"Diesel",
        gasoline:"Gasolina"

    };

    return nomes[fonte] || fonte;

}

form.addEventListener("reset", function(){

    // limpa resultado
    result.innerHTML = "";

    // esconde métricas
    metrics.style.display = "none";

    // remove gráfico
    if(chart){
        chart.destroy();
        chart = null;
    }
    // esconde resultado
    result.style.display = "none";

});