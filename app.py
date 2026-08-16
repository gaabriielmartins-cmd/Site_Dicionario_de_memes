from flask import Flask, jsonify, send_from_directory, request
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

# ============================================
# ARQUIVO DE DADOS DOS VISITANTES
# ============================================

ARQUIVO_DADOS = "dados_cliente.json"


def criar_arquivo_dados():
    """Cria o arquivo JSON caso ele ainda não exista."""

    if not os.path.exists(ARQUIVO_DADOS):
        with open(
            ARQUIVO_DADOS,
            "w",
            encoding="utf-8"
        ) as arquivo:
            json.dump([], arquivo, ensure_ascii=False, indent=4)

        print("✅ dados_cliente.json criado!")


def salvar_dado(dado):
    """Adiciona um novo registro ao arquivo JSON."""

    criar_arquivo_dados()

    try:
        with open(
            ARQUIVO_DADOS,
            "r",
            encoding="utf-8"
        ) as arquivo:
            dados = json.load(arquivo)

    except (json.JSONDecodeError, FileNotFoundError):
        dados = []

    dados.append(dado)

    with open(
        ARQUIVO_DADOS,
        "w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

# ============================================
# SUAS LISTAS
# ============================================

common = [
    "Noobini Pizzanini",
    "Lirilì Larilà",
    "Tim Cheese",
    "Fluriflura",
    "Talpa Di Fero",
    "Svinina Bombardino",
    "Pipi Kiwi",
    "Noobini Santanini",
    "Raccooni Jandelini",
    "Tartaragno",
    "Pipi Corni",
    "Holy Arepa",
]

rare = [
    "Trippi Troppi",
    "Gangster Footera",
    "Bandito Bobritto",
    "Boneca Ambalabu",
    "Cacto Hipopotamo",
    "Ta Ta Ta Ta Sahur",
    "Tric Trac Baraboom",
    "Cupcake Koala",
    "Frogo Elfo",
    "Pipi Abacate",
    "Pengolino Nuvoletto",
    "Pinealotto Fruttarino",
]

epic = [
    "Cappuccino Assassino",
    "Brr Brr Patapim",
    "Avocadini Antilopini",
    "Trulimero Trulicina",
    "Bambini Crostini",
    "Bananita Dolphinita",
    "Perochello Lemonchello",
    "Brri Brri Bicus Dicus Bombicus",
    "Avocadini Guffo",
    "Salamino Penguino",
    "Wombo Rollo",
    "Bandido Axolito",
    "Malame Amarale",
    "Ti Ti Ti Sahur",
    "Mangolini Parrocini",
    "Frogato Pirato",
    "Gato Celesto",
    "Doi Doi Do",
    "Pinguim Tree",
    "Penguino Cocosino",
    "Mummio Rappitto",
]

legendary = [
    "Burbaloni Luliloli",
    "Chimpanzini Bananini",
    "Ballerina Cappuccina",
    "Chef Crabracadabra",
    "Lionel Cactuseli",
    "Glorbo Fruttodrillo",
    "Quivioli Ameleonni",
    "Blueberrini Octopusini",
    "Pipi Potato",
    "Strawberrelli Flamingelli",
    "Pandaccini Bananini",
    "Sigma Boy",
    "Clickerino Crabo",
    "Caramello Filtrello",
    "Cocosini Mama",
    "Bandito Axolito",
    "Quackula",
    "Pi Pi Watermelon",
    "Buho del Cielo",
    "Chocco Bunny",
    "Puffaball",
    "Sigma Girl",
    "Sealo Regalo",
    "Buho de Fogo",
    "Electro Quacko",
    "Seraphino Gruyero",
]

mythic = [
    "Bloquinho Mítico",
    "Frigo Camelo",
    "Orangutini Ananassini",
    "Rinoceronte Tostadorino",
    "Bombardiro Crocodilo",
    "Bombombini Gusini",
    "Cavallo Virtuoso",
    "Gorillo Melancia-drilho",
    "Lerulerulerule",
    "Te Te Te Sahur",
    "Tracoducotulu Delapeladustuz",
    "Cachorrinho Melonito",
    "Toiletto Focaccino",
    "Brutto Gialutto",
    "Spioniro Golubiro",
    "Zibra Zubra Zibralini",
    "Tigrilini Watermelini",
    "Avocadorilla",
    "Gorillo Subwoofero",
    "Stoppo Luminino",
    "Ganganzelli Trulala",
    "Helicóptero Rhino",
    "Magi Ribbitini",
    "Jingle Jingle Sahur",
    "Los Noobinis",
    "Spongini Quackini",
    "Carloo",
    "Bee Loco",
    "Harpuccino",
    "Cocoteddy",
    "Carrotini Brainini",
    "Centrucci Nuclucci",
    "Jacko Spaventosa",
    "Bananito Bandito",
    "Tree Tree Tree Sahur",
    "Fizzy Soda",
    "Berenjello Angello",
    "Bucketoro",
    "Orbi Mochi",
]

brainrot_god = [
    "Brainrot God Lucky Block",
    "Cocofanto Elefanto",
    "Girafa Celestre",
    "Tralalero Tralala",
    "Odin Din Din Dun",
    "Tralalita Tralala",
    "Trenostruzzo Turbo 3000",
    "Trippi Troppi Troppa Trippa",
    "Ballerino Lololo",
    "Pakrahmatmamat",
    "Piccione Macchina",
    "Tractoro Dinosauro",
    "Cacasito Satalito",
    "Aquanaut",
    "Appelini",
    "Gattatino Nyanino",
    "Chihuanini Taconini",
    "Matteo",
    "Los Crocodilitos",
    "Tigroligre Frutonni",
    "Money Money Man",
    "Espresso Signora",
    "Tipi Topi Taco",
    "Unclito Samito",
    "Alessio",
    "Tukanno Bananno",
    "Orcalero Orcala",
    "Extinct Ballerina",
    "Vampira Cappucina",
    "Jacko Jack Jack",
    "Urubini Flamenguini",
    "Capi Taco",
    "Divino Platypio",
    "Los Chihuaninis",
    "Gattito Tacoto",
    "Sundrilla Sundae",
    "Las Capuchinas",
    "Pineaplino",
    "Bulbito Bandito Traktorito",
    "Los Tungtungtungcitos",
    "Ballerina Peppermintina",
    "Brr es Teh Patipum",
    "Pakrahmatmatina",
    "Los Bombinitos",
    "Los Orcalitos",
    "Orcalita Orcala",
    "Corn Corn Corn Sahur",
    "Mummy Ambalabu",
    "Snailenzo",
    "Squalanana",
    "Tartaruga Cisterna",
    "Trenotubo Axolotrico 9000",
    "Pato Preguiçoso",
    "Gengibre Globo",
    "Yeti Claus",
    "Crabbo Limonetta",
    "Granchiello Spiritell",
    "Tootini Shrimpini",
    "Los Tipi Tacos",
    "Frio Ninja",
    "Lumaca Maléfica",
    "Coruja de Noelo",
    "Pombinha Máquina",
    "Boba Panda",
    "Coelho Tralala",
    "Mastodôntico Telepiedone",
    "Os Gatinhos",
    "Bambu Bambu Sahur",
    "Cola Cat",
    "Chrismasmamat",
    "Anpali Babel",
    "Astrolero Cervalero",
    "Luv Luv Luv",
    "Cappuccino Clownino",
    "Bombardini Tortinii",
    "Brasilini Berimbini",
    "Patteo",
    "Belula Beluga",
    "Krupuk Pagi Pagi",
    "Skull Skull Skull",
    "Cocoa Assassino",
    "Tentáculo Técnico",
    "Ginger Cisterna",
    "Pandanini Frostini",
    "Dolphini Jetskini",
    "Pop Pop Sahur",
    "Noo La Polizia",
    "Karkerheart Luvkur",
    "Tenini Ballini",
    "Clovkur Kurkur",
    "Eggdin Egg Egg Dun",
    "Dumborino Miracello",
    "Robo Grafito",
    "Tortuginni Sandcastlini",
    "Pretzo Robo",
]

secret = [
    "Bloquinho Secreto da Sorte",
    "La Vacca Saturno Saturnita",
    "Los Tralaleritos",
    "Las Tralaleritas",
    "Job Job Job Sahur",
    "Fishboard",
    "Graipuss Medussi",
    "Berryno",
    "To to to Sahur",
    "Chicleteira Bicicleteira",
    "Chicleteirina Bicicleteirina",
    "Strawberrita",
    "La Grande Combinasion",
    "Bananito",
    "Dinossauro Nuclear",
    "DJ Panda",
    "Dinheiro Dinheiro Puggy",
    "Tang Tang Keletang",
    "Ketupat Kepat",
    "Tictac Sahur",
    "Ketchuru e Musturu",
    "Lavadorito Spinito",
    "Garama e Madundung",
    "Ventoliero Pavonero",
    "Dinheiro ou Cartão",
    "Burguro e Fryuro",
    "Capitano Moby",
    "Cerberus",
    "Dragon Cannelloni",
    "Bunito Bunito Spinito",
    "Cupid Cupid Sahur",
    "Ho Ho Ho Sahur",
    "Mi Gatito",
    "Octoball",
    "Quesadillo Vampiro",
    "Brunito Marsito",
    "Cupid Hotspot",
    "Eid Eid Eid Sahur",
    "Luck Luck Luck Sahur",
    "Flancito",
    "Burrito Bandito",
    "Chill Puppy",
    "Granny",
    "Los Bunitos",
    "Futbolini Skatini",
    "Los Quesadillas",
    "Noo meu Candy",
    "Arcadopus",
    "Los Nooo Meus Hotspotsitos",
    "Serafinna Medussi",
    "Flipa Sandala",
    "Rang Ring Bus",
    "Noo meu Presente",
    "Ombrello Topolino",
    "Los Meus Gatitos",
    "Não, meus Ovos",
    "As Chicleteiras",
    "67",
    "Donkeyturbo Express",
    "John Doe",
    "Sushi Inu",
    "Os Burritos",
    "Os 25",
    "Tacorillo Crocodilo",
    "Mariachi Corazoni",
    "Swag Soda",
    "Não meu Coração",
    "Não meu Ouro",
    "Chimnino",
    "Los Combinasionas",
    "Chicleteira Noelteira",
    "Baskito",
    "Tacorita Bicicleta",
    "Los Sweethearts",
    "Câmera Ramena",
    "Spinny Hammy",
    "Las Sis",
    "Chicleteira Cupideira",
    "Girafini Raftini",
    "Los Planitos",
    "Snailo Clover",
    "Los Hotspotsitos",
    "Frullato Framingo",
    "As Combinações Spooky",
    "As Combinações Jolly",
    "Cigno Fulgoro",
    "Churrito Bunnito",
    "Os Mobilis",
    "Capitano Gullini",
    "Celularcini Viciosini",
    "Os 67",
    "Os Candies",
    "As Frutas",
    "A Extinct Grande",
    "Os Bros",
    "Bacuru e Egguru",
    "A Spooky Grande",
    "Chipso e Queso",
    "Chillin Chili",
    "Money Money Reindeer",
    "Mieteteira Bicicleteira",
    "Tuff Tucano",
    "Gobblino Uniciclino",
    "Tralaledon",
    "Globa Steppa",
    "Esok Sekolah",
    "Los Cupids",
    "Los Puggies",
    "Sand Sand Sand",
    "W ou L",
    "Los Mariachis",
    "A Jolly Grande",
    "Os Primos",
    "Eviledon",
    "Os Tacoritas",
    "Lovin Rose",
    "Fragola La La La",
    "Abyssaloco",
    "Coco e Manga",
    "Dug Dug Dug",
    "A Combinação Taco",
    "Orcaledon",
    "Swaggy Bros",
    "La Lucky Grande",
    "La Romantic Grande",
    "Tirilikalika Tirilikalako",
    "Rico Dinero",
    "Gym Bros",
    "Jolly Jolly Sahur",
    "Gold Gold Gold",
    "Fishino Clownino",
    "Money Money Bros",
    "La Anniversary Grande",
    "Rosetti Tualetti",
    "Nacho Spyder",
    "La Easter Grande",
    "Hopilikalika Hopilikalako",
    "Steakini Fattini",
    "Caylusaurus",
    "Cloverat Clapat",
    "Spaghetti Tualetti",
    "Quackini Snackini",
    "Guest 666",
    "Festive 67",
    "Los Spaghettis",
    "Sammyni Fattini",
    "Rubrikiko",
    "Bearito Cabinito",
    "Los Chillis",
    "Ginger Gerat",
    "Los Hackers",
    "La Ginger Sekolah",
    "Spooky and Pumpky",
    "Boppin Bunny",
    "Sammyni Cakini",
    "Duggy Bros",
    "La Food Combinasion",
    "Fragrama and Chocrama",
    "A Casa Boo",
    "Os Sekolahs",
    "Lanterna Foxini",
    "Irmãos Kalika",
    "Panqueca e Xarope",
    "A Combinação Secreta",
    "Antonio",
    "Os Amigos",
    "Fortunu e Cashuru",
    "Reinito Sleighito",
    "Ketupat Bros",
    "Arcadragon",
    "Cooki e Milki",
    "Rosey e Teddy",
    "Popcuru e Fizzuru",
    "Bunny e Eggy",
    "Pegasus Celestial",
    "Venuspino",
    "Jelly Moby",
    "Elefanto Frigo",
    "Hidra Coelho",
    "Kraken",
    "A Combinação Suprema",
    "Digi Narval",
    "Urso Amor Amor",
    "Senhor Carapaça",
    "Hidra Dragão Caneloni",
    "Dragão Gingerini",
    "Dragão Aquanini",
    "Griffin",
    "Elefante Spyder",
]

og = [
    "Skibidi Toilet",
    "John Pork",
    "Cavaleiro Sem Cabeça",
    "Meowl",
    "Elefante Morango",
    "Expectativa vs. Realidade",
    "Somebody toucha my spaghet",
    "Big Chungus",
    "Kilroy was here",
    "Spider-Man Pointing at Spider-Man",
    "Creepy Wonka",
]


# ============================================
# ORGANIZAÇÃO
# ============================================

categories = {
    "common": common,
    "rare": rare,
    "epic": epic,
    "legendary": legendary,
    "mythic": mythic,
    "brainrot_god": brainrot_god,
    "secret": secret,
    "og": og,
}


# ============================================
# LISTA ÚNICA SEM DUPLICADOS
# ============================================

brainrots = list(dict.fromkeys(
    item
    for lista in categories.values()
    for item in lista
))


# ============================================
# API - TODOS OS BRAINROTS
# ============================================

@app.route("/api/brainrots", methods=["GET"])
def get_brainrots():

    return jsonify({
        "total": len(brainrots),
        "brainrots": brainrots
    })


# ============================================
# API - BRAINROTS POR CATEGORIA
# ============================================

@app.route("/api/brainrots/<category>", methods=["GET"])
def get_category(category):

    if category not in categories:

        return jsonify({
            "error": "Categoria não encontrada",
            "categories": list(categories.keys())
        }), 404

    lista = categories[category]

    return jsonify({
        "category": category,
        "total": len(lista),
        "brainrots": lista
    })


# ============================================
# API - PESQUISA
# ============================================

@app.route("/api/search", methods=["GET"])
def search():

    query = request.args.get("q", "").lower().strip()

    if not query:

        return jsonify({
            "error": "Informe uma busca. Exemplo: /api/search?q=trala"
        }), 400

    resultados = [
        nome
        for nome in brainrots
        if query in nome.lower()
    ]

    return jsonify({
        "query": query,
        "total": len(resultados),
        "results": resultados
    })


# ============================================
# SERVIR O HTML
# ============================================

@app.route("/")
def home():

    return send_from_directory(".", "index.html")


# ============================================
# GRAVAR DADOS DO CLIENTE
# ============================================

@app.route("/api/gravar", methods=["POST"])
def gravar_dados():

    # Captura os dados enviados pelo JavaScript
    dados_recebidos = request.get_json()

    # Verifica se recebeu alguma informação
    if not dados_recebidos:

        return jsonify({
            "error": "Nenhum dado enviado"
        }), 400

    try:

        # ========================================
        # PEGAR O IP DO VISITANTE
        # ========================================

        ip = request.headers.get("CF-Connecting-IP")

        # Caso não esteja usando Cloudflare
        if not ip:
            ip = request.headers.get("X-Forwarded-For")

        # Caso ainda não tenha encontrado
        if ip:
            ip = ip.split(",")[0].strip()
        else:
            ip = request.remote_addr

        # ========================================
        # HORÁRIO
        # ========================================

        from datetime import datetime
        from zoneinfo import ZoneInfo

        horario = datetime.now(
            ZoneInfo("America/Sao_Paulo")
        ).strftime("%d/%m/%Y %H:%M:%S")

        # ========================================
        # MONTAR OS DADOS
        # ========================================

        registro = {
            "nome": dados_recebidos.get("nome", ""),
            "ip": ip,
            "pesquisa": dados_recebidos.get("pesquisa", ""),
            "brainrot_clicado": dados_recebidos.get(
                "brainrot_clicado",
                ""
            ),
            "horario": horario
        }

        # ========================================
        # GRAVAR NO ARQUIVO
        # ========================================

        with open(
            "dados_cliente.json",
            "a",
            encoding="utf-8"
        ) as arquivo:

            linha_json = json.dumps(
                registro,
                ensure_ascii=False
            )

            arquivo.write(linha_json + "\n")

        # ========================================
        # RESPOSTA
        # ========================================

        return jsonify({
            "message": "Dados gravados com sucesso!",
            "dados": registro
        }), 201

    except Exception as e:

        return jsonify({
            "error": f"Falha ao salvar os dados: {str(e)}"
        }), 500

# ============================================
# CRIAR JSON AUTOMATICAMENTE
# ============================================

import os

if not os.path.exists("dados_cliente.json"):

    with open(
        "dados_cliente.json",
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write("")


# ============================================
# INICIAR SERVIDOR
# ============================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )