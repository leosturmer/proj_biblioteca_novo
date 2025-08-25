from textual.app import (App, SystemCommand, ComposeResult)
from textual.widgets import (
    Static,  Header, Footer, Button, TabbedContent, TabPane, Input, Label)
from textual.binding import Binding
from textual.screen import Screen
from textual.containers import (
    Container,  HorizontalGroup, VerticalGroup, ScrollableContainer, Grid)

from model import biblioteca


class TelaInicial(Screen):
    def compose(self):
        yield Static("📚 Biblioteca 📚", id="titulo_inicial")

        with VerticalGroup(id="grupo_botoes_inicial"):
            yield Button("Livros", id="bt_livros", classes="botoes_inicial", variant="primary")
            yield Button("Leitores", id="bt_leitores", classes="botoes_inicial", variant="success")
            yield Button("Empréstimos", id="bt_emprestimos", classes="botoes_inicial", variant="warning")
            yield Button("Sair", id="bt_sair", classes="botoes_inicial")

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "bt_livros":
                self.app.switch_screen("tela_livros")
            case "bt_leitores":
                self.app.switch_screen("tela_leitores")
            case "bt_emprestimos":
                self.app.switch_screen("tela_emprestimos")
            case "bt_sair":
                self.app.exit()


class TelaLivros(Screen):

    def compose(self):
        with HorizontalGroup(id="container_botao"):
            yield Button("Início", variant="primary", id="bt_tela_inicial")

        yield Static("📖  Livros da biblioteca  📖", id="st_header_livros", classes="stt_header_telas")

        with TabbedContent(initial="tab_cadastrar"):

            with TabPane("Cadastrar livro", id="tab_cadastrar"):

                with HorizontalGroup():
                    yield Label("Título do livro:")
                    yield Input(placeholder="digite aqui...", id="ip_cadastro_titulo")
                with HorizontalGroup():
                    yield Label("Código do livro:")
                    yield Input(placeholder="digite aqui...", id="ip_cadastro_codigo")
                with HorizontalGroup():
                    yield Button("Cadastrar", id="bt_cadastro_livro")

            with TabPane("Atualizar livro", id="tab_atualizar"):
                with HorizontalGroup():
                    yield Label("Título do livro:")
                    yield Input(placeholder="digite aqui...", id="ip_atualizar_titulo")
                with HorizontalGroup():
                    yield Label("Código do livro:")
                    yield Input(placeholder="digite aqui...", id="ip_atualizar_codigo")
                with HorizontalGroup():
                    yield Button("Atualizar", id="bt_atualizar_livro")

            with TabPane("Pesquisar livro", id="tab_pesquisar"):
                with HorizontalGroup():
                    yield Label("Código do livro:")
                    yield Input(placeholder="digite aqui...", id="ip_pesquisa_codigo")

                yield Static(f"Situação do livro", id="stt_situacao")

                with HorizontalGroup():
                    yield Button("Pesquisar", id="bt_consultar_livro", classes="grupo_botoes_pesquisa")
                    yield Button("Excluir", id="bt_excluir_livro", classes="grupo_botoes_pesquisa")

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "bt_tela_inicial":
                self.app.switch_screen("tela_inicial")

            case "bt_cadastro_livro":
                titulo = self.query_one("#ip_cadastro_titulo", Input).value
                cod = self.query_one("#ip_cadastro_codigo", Input).value

                if titulo == "" or cod == "":
                    self.notify("Insira os dados do livro!")
                elif biblioteca.cadastrar_livro(cod, titulo) == True:
                    self.notify(
                        f"{biblioteca.livros[cod].titulo} cadastrado com sucesso!")
                elif biblioteca.cadastrar_livro(cod, titulo) == False:
                    self.notify(f"{cod} já cadastrado!")

            case "bt_atualizar_livro":
                titulo = self.query_one("#ip_atualizar_titulo", Input).value
                cod = self.query_one("#ip_atualizar_codigo", Input).value

                if titulo == "" or cod == "":
                    self.notify("Insira os dados do livro!")
                else:
                    if biblioteca.atualizar_livro(cod, titulo) == False:
                        self.notify(
                            f"{biblioteca.livros[cod].titulo} atualizado com sucesso!")
                    elif biblioteca.atualizar_livro(cod, titulo) == True:
                        self.notify(f"[i]{biblioteca.livros[cod].cod}[/] não cadastrado")
                        

            case "bt_consultar_livro":
                cod = self.query_one("#ip_pesquisa_codigo", Input).value
                livro = biblioteca.consultar_livro(cod)
                stt_situacao = self.query_one("#stt_situacao", Static)

                if cod == "":
                    self.notify("Insira o código do livro!")
                elif livro:
                    stt_situacao.update(
                        f"Livro cadastrado: [i]{livro.titulo}[/], código {livro.cod}")
                else:
                    stt_situacao.update(f"Código não cadastrado")

            case "bt_excluir_livro":
                cod = self.query_one("#ip_pesquisa_codigo", Input).value
                livro = biblioteca.consultar_livro(cod)

                if cod == "":
                    self.notify("Insira o código do livro!")
                elif livro:
                    cod = self.query_one("#ip_pesquisa_codigo", Input).value
                    biblioteca.excluir_livro(cod)
                    self.notify("Livro excluído!")
                else:
                    self.notify("Livro não encontrado!")


class TelaLeitores(Screen):
    def compose(self):
        with HorizontalGroup(id="container_botao"):
            yield Button("Início", variant="success", id="bt_tela_inicial")

        yield Static("🙇‍♂️🙋  Leitores da biblioteca  🧏‍♀️💁‍♂️", id="st_header_emprestimos", classes="stt_header_telas")

        with TabbedContent(initial="tab_cadastrar"):

            with TabPane("Cadastrar leitor", id="tab_cadastrar"):
                with HorizontalGroup():
                    yield Label("Nome:")
                    yield Input(placeholder="digite aqui...", id="ip_cadastro_nome")
                with HorizontalGroup():
                    yield Label("CPF:")
                    yield Input(placeholder="digite aqui...", id="ip_cadastro_cpf")
                with HorizontalGroup():
                    yield Button("Cadastrar", id="bt_cadastro_leitor")

            with TabPane("Atualizar leitor", id="tab_atualizar"):
                with HorizontalGroup():
                    yield Label("Nome:")
                    yield Input(placeholder="digite aqui...", id="ip_atualizar_nome")
                with HorizontalGroup():
                    yield Label("CPF:")
                    yield Input(placeholder="digite aqui...", id="ip_atualizar_cpf")
                with HorizontalGroup():
                    yield Button("Atualizar", id="bt_atualizar_leitor")

            with TabPane("Pesquisar leitor", id="tab_pesquisar"):
                with HorizontalGroup():
                    yield Label("CPF:")
                    yield Input(placeholder="digite aqui...", id="ip_pesquisa_cpf")

                yield Static(f"Situação do leitor", id="stt_situacao")

                with HorizontalGroup():
                    yield Button("Pesquisar", id="bt_consultar_leitor", classes="grupo_botoes_pesquisa")
                    yield Button("Excluir", id="bt_excluir_leitor", classes="grupo_botoes_pesquisa")

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "bt_tela_inicial":
                self.app.switch_screen("tela_inicial")

            case "bt_cadastro_leitor":
                nome = self.query_one("#ip_cadastro_nome", Input).value
                cpf = self.query_one("#ip_cadastro_cpf", Input).value

                if nome == "" or cpf == "":
                    self.notify("Insira os dados do leitor!")
                elif biblioteca.cadastrar_leitor(cpf, nome) == True:
                    self.notify(
                        f"{biblioteca.leitores[cpf].nome} cadastrado com sucesso!")
                elif biblioteca.cadastrar_leitor(cpf, nome) == False:
                    self.notify(f"{cpf} já cadastrado!")

            case "bt_atualizar_leitor":
                nome = self.query_one("#ip_atualizar_nome", Input).value
                cpf = self.query_one("#ip_atualizar_cpf", Input).value

                if nome == "" or cpf == "":
                    self.notify("Insira os dados do leitor!")
                else:
                    if biblioteca.atualizar_leitor(cpf, nome) == False:
                        self.notify(
                            f"{biblioteca.leitores[cpf].nome} atualizado com sucesso!")
                    elif biblioteca.atualizar_livro(cpf, nome) == True:
                        self.notify(f"[i]{biblioteca.leitores[cpf].cpf}[/] não cadastrado")

            case "bt_consultar_leitor":
                cpf = self.query_one("#ip_pesquisa_cpf", Input).value
                leitor = biblioteca.consultar_leitor(cpf)
                stt_situacao = self.query_one("#stt_situacao", Static)

                if cpf == "":
                    self.notify("Insira o CPF do leitor!")
                elif leitor:
                    stt_situacao.update(
                        f"Leitor cadastrado: [i]{leitor.nome}[/], CPF {leitor.cpf}")
                else:
                    stt_situacao.update(f"CPF não cadastrado")

            case "bt_excluir_leitor":
                cpf = self.query_one("#ip_pesquisa_cpf", Input).value
                leitor = biblioteca.consultar_leitor(cpf)

                if cpf == "":
                    self.notify("Insira o CPF do leitor!")
                elif leitor:
                    cpf = self.query_one("#ip_pesquisa_cpf", Input).value
                    biblioteca.excluir_leitor(cpf)
                    self.notify("Leitor excluído!")
                else:
                    self.notify("Leitor não encontrado!")


class TelaEmprestimos(Screen):
    def compose(self):
        with HorizontalGroup(id="container_botao"):
            yield Button("Início", variant="warning", id="bt_tela_inicial")

        yield Static("🔄📗  Empréstimos da biblioteca  📗🔄", id="st_header_emprestimos", classes="stt_header_telas")

        with TabbedContent(initial="tab_emprestimos"):
            with TabPane("Visualizar empréstimos", id="tab_emprestimos"):
                with HorizontalGroup():
                    yield Label("CPF do leitor:")
                    yield Input(placeholder="digite aqui...")

                with HorizontalGroup():
                    yield Label("Código do livro:")
                    yield Input(placeholder="digite aqui...")

                yield Static(f"""
Nome do leitor: 
Título do livro: 
Situação: 
""", 
id="stt_situacao")

                with HorizontalGroup():
                    yield Button("Emprestar", id="bt_emprestar", classes="grupo_botoes_pesquisa")
                    yield Button("Devolver", id="bt_devolver", classes="grupo_botoes_pesquisa")


    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "bt_emprestar":
                pass 

            case "bt_devolver":
                pass