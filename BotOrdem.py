from datetime import datetime, timezone
from typing import List, Optional
import discord
from discord.components import SelectOption
import pyodbc
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.message_content = True

bot = discord.Client(intents=intents)

# Conectar ao banco de dados SQL Server
connection = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=WK-161;"
    "Database=Administrativo_4R;"
    "Trusted_Connection=yes;"
)

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(value="OS0", label="OS's Autorizadas Para Você", emoji= "🚀" ),
            discord.SelectOption(value="OS1", label="OS's Atribuídas Para Você", emoji="👨🏻‍💻"),
            discord.SelectOption(value="OS2", label="OS's em BackLog", emoji="📌"),
            discord.SelectOption(value="OS3", label="OS's em Análise Técnica", emoji="📝"),
            discord.SelectOption(value="OS4", label="OS's com Não Conformidade", emoji="🐛"),
        ]
        super().__init__(
            placeholder="Selecione a opção desejada...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "OS0":
            # Defina sua consulta SQL
            sql_query = "Select OrdemServicoUsuarioDescricao, OrdemServicoObservacoesTexto From OrdemServico Where OrdemServicoSequencia = 44501"
            
            #Mostra a mensagem para o usuario
            await interaction.response.send_message("O usuário escolheu Visualizar Autorizadas para ele.")
            
            # Execute a consulta SQL e recupere os resultados
            cursor = connection.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchall()
            # Feche a conexão com o banco de dados
            connection.close()

            # Crie um arquivo PDF e insira os dados
            pdf_filename = "dados.pdf"
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            y = 750  # Posição vertical inicial para os dados no PDF

            # Cabeçalho do PDF
            c.drawString(100, y, "Desc")
            c.drawString(200, y, "Texto")
            y -= 20

            # Inserir os dados no PDF
            for row in result:
                id, nome = row
                c.drawString(100, y, str(id))
                c.drawString(200, y, nome)
                y -= 20

            # Salvar o arquivo PDF
            c.save()

        elif self.values[0] == "OS1":
            await interaction.response.send_message("")
        elif self.values[0] == "OS2":
            await interaction.response.send_message("")
        elif self.values[0] == "OS3":
            await interaction.response.send_message("")
        elif self.values[0] == "OS4":
            await interaction.response.send_message("")

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        dropdown_instance = Dropdown()  
        self.add_item(dropdown_instance)  

@bot.event
async def on_ready():
    print('Bot está pronto para uso.')

    # Substitua 'SEU_CANAL_ID' pelo ID do canal onde você deseja que o dropdown apareça
    channel = bot.get_channel(1156262631418638398)
    if channel:
        dropdown_view = DropdownView()

        embed = discord.Embed(
            title="Consulta de Ordens de Serviço - SETOR TRIBUTÁRIO", 
            url="https://www.4rtecnologia.com.br/", 
            description="Nessa seção, você pode realizar consultas das ordens de serviços autorizadas para você, atribuídas para você, em BackLog, em Análise Técnica e com Não Conformidade. \n\n Selecione a opção correta e evite transtornos. Caso necessite de ajuda, não exite em nos contatar.",
            colour= discord.Color.blurple(),
            timestamp = datetime.now()
        )
        
        embed.set_author(
            name="4R Tecnologia", 
            icon_url="https://i.postimg.cc/ncmZmnr7/4-RTecnologia.jpg"
        )
        
        embed.set_image(
            url="https://i.postimg.cc/MTf2X47t/4RLogoOG.jpg"
        )

        embed.set_footer(
            text = "4R Tecnologia © Todos os direitos reservados",
            icon_url ="https://i.postimg.cc/ncmZmnr7/4-RTecnologia.jpg"
        )

        await channel.send(view=dropdown_view, embed=embed)
    else:
        print("Canal não encontrado.")

bot.run('MTEyODczMzg2Njg5OTgxNjQ2OA.GVKJu_.jubjnbsI-xovHslfoaGe8VLhGhXHA6UB7UlBmY')

