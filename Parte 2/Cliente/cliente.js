const readline = require("readline-sync");
const axios = require('axios').default;
const sleep = (waitTimeInMs) => new Promise(resolve => setTimeout(resolve, waitTimeInMs));
// Cadastrar o usuário inicialmente
cadastrarUsuario()

async function menu() {
    await(2000)
    // Display do menu
    console.log("\nBem-vindo(a) ao servico de enquetes!")
    console.log("As seguintes opções estão disponiveis: ")
    console.log("1: Cadastrar nova enquete")
    console.log("2: Consultar o status de uma enquete")
    console.log("3: Votar em uma enquete")

    // Lendo a opção desejada
    const readline = require('readline-sync');
    let selecao_menu = readline.question("Selecionar: ");

    // Switch case do menu
    switch (selecao_menu) {
        case "1":
            cadastrarEnquete()
            break;
        case "2":
            consultarEnquete()
            break;
        case "3":
            votarEnquete()
            break;
        default:
            console.log("Opcao invalida!")
            atualizar_novidades()
            menu()
    }
}
async function atualizar_novidades(){
    axios.get('http://127.0.0.1:5000/stream')
        .then(function (response){
            let dados = response['data'];
            console.log(dados['message']);
        });
}

async function cadastrarUsuario() {
    const readline = require('readline-sync');
    let nome_usuario = readline.question("\nDigite seu nome: ");

    axios.post('http://127.0.0.1:5000/cadastro', {nome: nome_usuario})
        .then(function (response) {
            let dados = response['data'];
            console.log(dados['message']);
        })
        .catch(function (error) {
            console.log(error);
        });
        await sleep(1000);
        await ouvirServidor(nome_usuario)
}

function ouvirServidor(nome_usuario){
    const EventSource = require('eventsource');
    const fonte = new EventSource('http://127.0.0.1:5000/stream');
    fonte.addEventListener(nome_usuario, function (event) {
        let dados = event.data
        let dados_json = JSON.parse(dados)
        console.log("\nNova mensagem do servidor:" + dados_json['message'])
    });

    fonte.addEventListener('error', function(event) {
        console.log("Error"+ event)
    });

    menu()
 }

async function cadastrarEnquete() {
    const readline = require('readline-sync');
    let nome_usuario = readline.question("\nDigite seu nome: ");
    let titulo_enquete = readline.question("Titulo da enquete: ");
    let local_enquete = readline.question("Local: ");
    let data1_enquete = readline.question("Opcao 1 de data: ");
    let horario1_enquete = readline.question("Horario: ");
    let data2_enquete = readline.question("Opcao 2 de data: ");
    let horario2_enquete = readline.question("Horario: ");
    let limite_enquete = readline.question("Data limite (formato AAAA-MM-DD): ");

    axios.post('http://127.0.0.1:5000/novaenquete', {
        nome: nome_usuario,
        titulo: titulo_enquete,
        local: local_enquete,
        data1: data1_enquete,
        horario1: horario1_enquete,
        data2: data2_enquete,
        horario2: horario2_enquete,
        limite: limite_enquete
        })
        .then(function (response) {
            let dados = response['data'];
            console.log(dados['message']);
        })
        .catch(function (error) {
            console.log(error);
        });
        await sleep(1000);
    
    menu()
}

async function consultarEnquete() {
    const readline = require('readline-sync');
    let nome_usuario = readline.question("\nDigite seu nome: ");
    let titulo_enquete = readline.question("Titulo da enquete: ");

    axios.post('http://127.0.0.1:5000/consultaenquete', {
        nome: nome_usuario,
        titulo: titulo_enquete
        })
        .then(function (response) {
            let dados = response['data'];
            console.log(dados['message']);
        })
        .catch(function (error) {
            console.log(error);
        });
        await sleep(1000);

    menu()
}

async function votarEnquete() {
    const readline = require('readline-sync');
    let nome_usuario = readline.question("\nDigite seu nome: ");
    let titulo_enquete = readline.question("Titulo da enquete: ");
    let voto_enquete = readline.question("Voto: ");

    axios.post('http://127.0.0.1:5000/votar', {
        nome: nome_usuario,
        titulo: titulo_enquete,
        voto: voto_enquete
        })
        .then(function (response) {
            let dados = response['data'];
            console.log(dados['message']);
        })
        .catch(function (error) {
            console.log(error);
        });
        await sleep(1000);

    menu()
}

