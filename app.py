from flask import Flask, jsonify, send_from_directory, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import json
import os
import re
import secrets
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

# ============================================
# CHAVE SECRETA (necessária para usar sessões)
# ============================================
# Em produção, defina a variável de ambiente SECRET_KEY.
# Se não existir, geramos uma aleatória (mas os logins somem
# a cada reinício do servidor).

app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

# Sessão dura enquanto o navegador estiver aberto (cookie de sessão).
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


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
# ARQUIVO DE USUÁRIOS (LOGIN)
# ============================================

ARQUIVO_USUARIOS = "usuarios.json"

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def criar_arquivo_usuarios():
    """Cria o arquivo de usuários caso ainda não exista."""

    if not os.path.exists(ARQUIVO_USUARIOS):
        with open(
            ARQUIVO_USUARIOS,
            "w",
            encoding="utf-8"
        ) as arquivo:
            json.dump({}, arquivo, ensure_ascii=False, indent=4)


def carregar_usuarios():
    """Carrega o dicionário de usuários {username: {...}}."""

    criar_arquivo_usuarios()

    try:
        with open(
            ARQUIVO_USUARIOS,
            "r",
            encoding="utf-8"
        ) as arquivo:
            return json.load(arquivo)

    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def salvar_usuarios(usuarios):
    """Salva o dicionário de usuários no arquivo."""

    with open(
        ARQUIVO_USUARIOS,
        "w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            usuarios,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def login_required(f):
    """Decorator que bloqueia o acesso a rotas sem login ativo."""

    @wraps(f)
    def decorated(*args, **kwargs):

        if not session.get("email"):

            return jsonify({
                "error": "Você precisa fazer login."
            }), 401

        return f(*args, **kwargs)

    return decorated


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
    "Noobini Santanini",
    "Raccooni Jandelini",
    "Tartaragno",
    "Pipi Kiwi",
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
    "Pipi Avocado",
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
    "Malame Amarele",
    "Ti Ti Ti Sahur",
    "Mangolini Parrocini",
    "Frogato Pirato",
    "Gato Celesto",
    "Doi Doi Do",
    "Penguin Tree",
    "Penguino Cocosino",
    "Mummio Rappitto",
]

legendary = [
    "Burbaloni Loliloli",
    "Chimpanzini Bananini",
    "Ballerina Cappuccina",
    "Chef Crabracadabra",
    "Lionel Cactuseli",
    "Glorbo Fruttodrillo",
    "Quivioli Ameleonni",
    "Bandito Axolito",
    "Clickerino Crabo",
    "Blueberrinni Octopusini",
    "Caramello Filtrello",
    "Pipi Potato",
    "Strawberrelli Flamingelli",
    "Cocosini Mama",
    "Pandaccini Bananini",
    "Quackula",
    "Pi Pi Watermelon",
    "Buho del Cielo",
    "Sigma Boy",
    "Chocco Bunny",
    "Puffaball",
    "Sigma Girl",
    "Sealo Regalo",
    "Buho de Fuego",
    "Seraphino Gruyero",
]

mythic = [
    "Avocadorilla",
    "Bananito Bandito",
    "Bee Loco",
    "Berenjello Angello",
    "Bombardiro Crocodilo",
    "Bombombini Gusini",
    "Brutto Gialutto",
    "Bucketoro",
    "Cachorrito Melonito",
    "Carloo",
    "Carrotini Brainini",
    "Cavallo Virtuoso",
    "Centrucci Nuclucci",
    "Cocoteddy",
    "Fizzy Soda",
    "Frigo Camelo",
    "Ganganzelli Trulala",
    "Gorillo Subwoofero",
    "Gorillo Watermelondrillo",
    "Harpuccino",
    "Jacko Spaventosa",
    "Jingle Jingle Sahur",
    "Lerulerulerule",
    "Los Noobinis",
    "Magi Ribbitini",
    "Orangutini Ananassini",
    "Orbi Mochi",
    "Rhino Helicopterino",
    "Rhino Toasterino",
    "Spioniro Golubiro",
    "Spongini Quackini",
    "Stoppo Luminino",
    "Te Te Te Sahur",
    "Tigrilini Watermelini",
    "Toiletto Focaccino",
    "Tracoducotulu Delapeladustuz",
    "Tree Tree Tree Sahur",
    "Zibra Zubra Zibralini",
]

brainrot_god = [
    "Cocofanto Elefanto",
    "Girafa Celestre",
    "Gattatino Nyanino",
    "Chihuanini Taconini",
    "Tralalero Tralala",
    "Matteo",
    "Los Crocodillitos",
    "Tigroligre Fruttoni",
    "Money Money Man",
    "Espresso Signora",
    "Tipi Topi Taco",
    "Unclito Samito",
    "Antonio",
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
    "Pakrahmatmamat",
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
    "Ginger Globo",
    "Yeti Claus",
    "Crabbo Limonetta",
    "Granchiello Spiritell",
    "Tootini Shrimpini",
    "Los Tipi Tacos",
    "Frio Ninja",
    "Lumaca Malefica",
    "Buho de Noelo",
    "Pombinha Macchina",
    "Boba Panda",
    "Bunny Tralala",
    "Mastodontico Telepiedone",
    "Los Gattitos",
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
    "Tentacolo Tecnico",
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
    "Gelatina Volatina",
    "Yess my Resume",
    "Noo my Resume",
    "Los Secret Combinasionas",
    "Noo my Examen",
    "Examen Bros",
    "Chicleteira Champeona",
    "Toro Españolo",
    "Pizza and Ranch",
    "Yess my Examine",
    "Grabatron",
    "Rubiko and Kubiko",
    "Cangurato Gelato",
    "Noodle Noodle Poodle",
    "Los Admins",
    "Los Tictacs",
    "Los Tangcitos",
    "Los Cornis",
    "Los Sigmas",
    "Moby Bros",
    "Capitano Americano",
    "Bufalino Boomberino",
    "Esok Goala",
    "4th Bros",
    "Var Var Var",
    "Ref Ref Ref Sahur",
    "Hippo Golazo",
    "Chicleteira Surfeiteira",
    "Aquarino",
    "Gelato Lumacho",
    "Venuspino",
    "Sand Sand Sand",
    "Bearito Cabinito",
    "Los Fruits",
    "Frullato Framingo",
    "Sushi Inu",
    "Girafini Raftini",
    "Octoball",
    "Rocketini Frostini",
    "Craburger",
    "Kraken",
    "Caylusaurus",
    "Steakini Fattini",
    "Dragon Aquanini",
    "Coco and Mango",
    "Capitano Gullini",
    "Ombrello Topolino",
    "Bombardiro Vaccariro",
    "Aqua Dragon",
    "Digi Narwhal",
    "Hydra Bunny",
    "Pancake and Syrup",
    "Arcadragon",
    "Kalika Bros",
    "Duggy Bros",
    "Los Chillis",
    "Los Hackers",
    "Quackini Snackini",
    "Rubrikiko",
    "Hopilikalika Hopilikalako",
    "Money Money Bros",
    "La Easter Grande",
    "Gym Bros",
    "Rico Dinero",
    "Los Mariachis",
    "Abyssaloco",
    "Globa Steppa",
    "Churrito Bunnito",
    "Baskito",
    "Camera Ramena",
    "Flipa Sandala",
    "John Doe",
    "Los Bunitos",
    "Futbolini Skatini",
    "Buho de Volto",
    "Glaciator",
    "Easter Easter Easter Sahur",
    "Cash or Card",
    "Bananito",
    "Strawberrita",
    "Berryno",
    "Jelly Moby",
    "Sammyni Cakini",
    "Flancito",
    "La Anniversary Grande",
    "Bunny and Eggy",
    "Boppin Bunny",
    "Hydra Dragon Cannelloni",
    "Rosey and Teddy",
    "La Supreme Combinasion",
    "Griffin",
    "Popcuru and Fizzuru",
    "Dragon Gingerini",
    "Celestial Pegasus",
    "Love Love Bear",
    "Los Amigos",
    "Ketupat Bros",
    "La Secret Combinasion",
    "La Casa Boo",
    "Cooki and Milki",
    "Fortunu and Cashuru",
    "Foxini Lanternini",
    "Los Sekolahs",
    "Reinito Sleighito",
    "Signore Carapace",
    "Sammyni Fattini",
    "La Food Combinasion",
    "La Ginger Sekolah",
    "Spaghetti Tualetti",
    "Spooky and Pumpky",
    "Fragrama and Chocrama",
    "Festive 67",
    "Los Spaghettis",
    "Elefanto Frigo",
    "Ginger Gerat",
    "Tirilikalika Tirilikalako",
    "Cloverat Clapat",
    "Swaggy Bros",
    "Nacho Spyder",
    "Gold Gold Gold",
    "La Lucky Grande",
    "Rosetti Tualetti",
    "Antonio",
    "Jolly Jolly Sahur",
    "La Romantic Grande",
    "Orcaledon",
    "Los Primos",
    "Lovin Rose",
    "Los Puggies",
    "La Jolly Grande",
    "W or L",
    "Dug dug dug",
    "La Taco Combinasion",
    "Los Tacoritas",
    "Eviledon",
    "La Spooky Grande",
    "Los Cupids",
    "Tralaledon",
    "Chillin Chili",
    "Money Money Reindeer",
    "Chipso and Queso",
    "Tuff Toucan",
    "Gobblino Uniciclino",
    "Esok Sekolah",
    "Mieteteira Bicicleteira",
    "Los 67",
    "Los Spooky Combinasionas",
    "Los Candies",
    "La Extinct Grande",
    "Los Mobilis",
    "Bacuru and Egguru",
    "Celularcini Viciosini",
    "Los Jolly Combinasionas",
    "Los Bros",
    "Cigno Fulgoro",
    "Fishino Clownino",
    "Tacorita Bicicleta",
    "Chicleteira Cupideira",
    "Spinny Hammy",
    "Los Planitos",
    "Snailo Clovero",
    "Las Sis",
    "Los Hotspotsitos",
    "Chicleteira Noelteira",
    "Los Sweethearts",
    "Los Burritos",
    "Swag Soda",
    "Tacorillo Crocodillo",
    "Noo my Gold",
    "Los Combinasionas",
    "Noo my Heart",
    "Chimnino",
    "Donkeyturbo Express",
    "Los 25",
    "Mariachi Corazoni",
    "Arcadopus",
    "Los Nooo My Hotspotsitos",
    "Los Mi Gatitos",
    "Rang Ring Bus",
    "Noo my Eggs",
    "Guest 666",
    "67",
    "Noo my Present",
    "Los Chicleteiras",
    "Serafinna Medusella",
    "Granny",
    "Cupid Hotspot",
    "Brunito Marsito",
    "Eid Eid Eid Sahur",
    "Burrito Bandito",
    "Noo my Candy",
    "Quesadillo Vampiro",
    "Los Quesadillas",
    "Luck Luck Luck Sahur",
    "Chill Puppy",
    "Mi Gatito",
    "Horegini Boom",
    "Pot Pumpkin",
    "Santa Hotspot",
    "Naughty Naughty",
    "Telemorte",
    "Bunito Bunito Spinito",
    "Ho Ho Ho Sahur",
    "Quesadilla Crocodila",
    "Cupid Cupid Sahur",
    "25",
    "Noo my examine",
    "Los Jobcitos",
    "Pot Hotspot",
    "List List List Sahur",
    "Bunny Bunny Bunny Sahur",
    "Bunnyman",
    "Nooo My Hotspot",
    "Pirulitoita Bicicleteira",
    "La Sahur Combinasion",
    "Coffin Tung Tung Tung Sahur",
    "La Vacca Lepre Lepreino",
    "Please my Present",
    "Cuadramat and Pakrahmatmamat",
    "Tung Tung Tung Sahur",
    "Los Cucarachas",
    "Love Love Love Sahur",
    "Perrito Burrito",
    "1x1x1x1",
    "Giftini Spyderini",
    "Paradiso Axolottino",
    "Las Vaquitas Saturnitas",
    "Karker Sahur",
    "Triplito Tralaleritos",
    "Buntteo",
    "Santteo",
    "Los Karkeritos",
    "Los Trios",
    "Trickolino",
    "La Vacca Jacko Linterino",
    "Dul Dul Dul",
    "La Karkerkar Combinasion",
    "Rocco Disco",
    "Zombie Tralala",
    "Frankentteo",
    "La Vacca Prese Presente",
    "Reindeer Tralala",
    "Yess my examine",
    "Pumpkini Spyderini",
    "Extinct Matteo",
    "Boatito Auratito",
    "Fragola La La La",
    "Los Spyderinis",
    "Los Tortus",
    "Trenostruzzo Turbo 4000",
    "Guerriro Digitale",
    "La Cucaracha",
    "Extinct Tralalero",
    "Vulturino Skeletono",
    "Torrtuginni Dragonfrutini",
    "Bisonte Giuppitere",
    "Los Matteos",
    "Jackorilla",
    "Chachechi",
    "Sammyni Spyderini",
    "Blackhole Goat",
    "Cerberus",
    "Karkerkar Kurkur",
    "Agarrini la Palini",
    "Tang Tang Keletang",
    "Ketupat Kepat",
    "Burguro And Fryuro",
    "Ventoliero Pavonero",
    "Garama and Madundung",
    "Tictac Sahur",
    "Capitano Moby",
    "Ketchuru and Musturu",
    "Lavadorito Spinito",
    "Money Money Puggy",
    "Graipuss Medussi",
    "To to to Sahur",
    "DJ Panda",
    "La Grande Combinasion",
    "Job Job Job Sahur",
    "Fishboard",
    "Chicleteira Bicicleteira",
    "Chicleteirina Bicicleteirina",
    "Nuclearo Dinossauro",
    "GOAT",
    "Los Tralaleritos",
    "Las Tralaleritas",
    "La Vacca Saturno Saturnita",
    "Spyder Elephant",
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
# API - CADASTRO
# ============================================

@app.route("/api/register", methods=["POST"])
def register():

    dados = request.get_json(silent=True) or {}

    email = (dados.get("email") or "").strip()
    password = dados.get("password") or ""

    if not email or not password:

        return jsonify({
            "error": "Informe e-mail e senha."
        }), 400

    if not EMAIL_REGEX.match(email):

        return jsonify({
            "error": "Informe um e-mail válido."
        }), 400

    if len(password) < 6:

        return jsonify({
            "error": "A senha precisa ter pelo menos 6 caracteres."
        }), 400

    usuarios = carregar_usuarios()

    chave = email.lower()

    if chave in usuarios:

        return jsonify({
            "error": "Já existe uma conta com esse e-mail."
        }), 409

    usuarios[chave] = {
        "email": email,
        "password_hash": generate_password_hash(password),
        "criado_em": datetime.now(
            ZoneInfo("America/Sao_Paulo")
        ).strftime("%d/%m/%Y %H:%M:%S")
    }

    salvar_usuarios(usuarios)

    # Login automático após o cadastro
    session["email"] = email

    return jsonify({
        "message": "Cadastro realizado com sucesso!",
        "email": email
    }), 201


# ============================================
# API - LOGIN
# ============================================

@app.route("/api/login", methods=["POST"])
def login():

    dados = request.get_json(silent=True) or {}

    email = (dados.get("email") or "").strip()
    password = dados.get("password") or ""

    if not email or not password:

        return jsonify({
            "error": "Informe e-mail e senha."
        }), 400

    usuarios = carregar_usuarios()

    usuario = usuarios.get(email.lower())

    if not usuario or not check_password_hash(
        usuario["password_hash"], password
    ):

        return jsonify({
            "error": "E-mail ou senha inválidos."
        }), 401

    session["email"] = usuario["email"]

    return jsonify({
        "message": "Login realizado com sucesso!",
        "email": usuario["email"]
    })


# ============================================
# API - LOGOUT
# ============================================

@app.route("/api/logout", methods=["POST"])
def logout():

    session.pop("email", None)

    return jsonify({
        "message": "Logout realizado com sucesso!"
    })


# ============================================
# API - VERIFICAR SESSÃO
# ============================================

@app.route("/api/session", methods=["GET"])
def get_session():

    email = session.get("email")

    return jsonify({
        "logged_in": bool(email),
        "email": email
    })


# ============================================
# API - TODOS OS BRAINROTS
# ============================================

@app.route("/api/brainrots", methods=["GET"])
@login_required
def get_brainrots():

    return jsonify({
        "total": len(brainrots),
        "brainrots": brainrots
    })


# ============================================
# API - BRAINROTS POR CATEGORIA
# ============================================

@app.route("/api/brainrots/<category>", methods=["GET"])
@login_required
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
@login_required
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
@login_required
def gravar_dados():

    # Captura os dados enviados pelo JavaScript
    dados_recebidos = request.get_json(silent=True) or {}

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

        horario = datetime.now(
            ZoneInfo("America/Sao_Paulo")
        ).strftime("%d/%m/%Y %H:%M:%S")

        # ========================================
        # MONTAR OS DADOS
        # ========================================
        # O nome vem da sessão (usuário logado), não do
        # que o cliente envia — assim não dá para forjar.

        registro = {
            "usuario": session.get("email"),
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
# CRIAR ARQUIVOS AUTOMATICAMENTE
# ============================================

criar_arquivo_dados()
criar_arquivo_usuarios()


# ============================================
# INICIAR SERVIDOR
# ============================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )