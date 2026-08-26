import re

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


# ============================================================
# CORES
# ============================================================

FUNDO = (0.055, 0.065, 0.09, 1)
PAINEL = (0.10, 0.115, 0.15, 1)
CAMPO = (0.14, 0.155, 0.20, 1)

BOTAO = (0.20, 0.55, 0.95, 1)
BOTAO_PRESSIONADO = (0.15, 0.45, 0.85, 1)

BRANCO = (0.95, 0.96, 0.98, 1)
CINZA = (0.65, 0.68, 0.74, 1)

VERDE = (0.25, 0.85, 0.45, 1)
VERMELHO = (0.95, 0.30, 0.30, 1)


# ============================================================
# RESOLVER EQUAÇÃO
# ============================================================

def separar_lado(lado):

    if not lado:
        raise ValueError

    if lado[0] not in "+-":
        lado = "+" + lado

    termos = re.findall(r"[+-][^+-]+", lado)

    coef_x = 0
    constante = 0

    for termo in termos:

        if "x" in termo:

            coef = termo.replace("x", "")

            if coef in ("+", ""):
                coef = 1

            elif coef == "-":
                coef = -1

            else:
                coef = float(coef)

            coef_x += coef

        else:

            constante += float(termo)

    return coef_x, constante


def resolver_equacao(equacao):

    equacao = equacao.replace(" ", "").lower()

    if "=" not in equacao:
        raise ValueError

    partes = equacao.split("=")

    if len(partes) != 2:
        raise ValueError

    esquerda = partes[0]
    direita = partes[1]

    a, b = separar_lado(esquerda)
    c, d = separar_lado(direita)

    coeficiente = a - c
    termo_independente = d - b

    # 0x = 0
    if coeficiente == 0:

        if termo_independente == 0:
            return "Infinitas soluções broh"

        return "Sem solução broh"

    x = termo_independente / coeficiente

    if x.is_integer():
        x = int(x)

    return f"x = {x} broh"


# ============================================================
# PAINEL ARREDONDADO
# ============================================================

class PainelArredondado(BoxLayout):

    def __init__(self, cor=PAINEL, raio=20, **kwargs):

        super().__init__(**kwargs)

        with self.canvas.before:

            Color(*cor)

            self.fundo = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(raio)]
            )

        self.bind(
            pos=self.atualizar_fundo,
            size=self.atualizar_fundo
        )

    def atualizar_fundo(self, *args):

        self.fundo.pos = self.pos
        self.fundo.size = self.size


# ============================================================
# CAMPO DE EQUAÇÃO
# ============================================================

class CampoEquacao(TextInput):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.background_color = CAMPO
        self.foreground_color = BRANCO

        self.cursor_color = BOTAO

        self.font_size = sp(25)

        self.multiline = False

        self.padding = [
            dp(20),
            dp(18),
            dp(20),
            dp(18)
        ]

        self.halign = "center"

        self.hint_text = "Ex: 2x + 6 = 14"

        self.hint_text_color = CINZA

        self.write_tab = False


# ============================================================
# BOTÃO
# ============================================================

class BotaoResolver(Button):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""

        self.background_color = BOTAO

        self.color = BRANCO

        self.font_size = sp(20)

        self.bold = True

        self.bind(
            state=self.mudar_cor
        )

    def mudar_cor(self, instance, valor):

        if valor == "down":

            self.background_color = BOTAO_PRESSIONADO

        else:

            self.background_color = BOTAO


# ============================================================
# INTERFACE
# ============================================================

class CalculadoraEquacoes(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(
            orientation="vertical",

            spacing=dp(18),

            padding=[
                dp(22),
                dp(30),
                dp(22),
                dp(25)
            ],

            **kwargs
        )

        # ====================================================
        # TÍTULO
        # ====================================================

        titulo = Label(
            text="CALCULADORA broh",

            font_size=sp(31),

            bold=True,

            color=BRANCO,

            size_hint_y=None,

            height=dp(45)
        )

        self.add_widget(titulo)


        subtitulo = Label(
            text="DE EQUAÇÕES broh",

            font_size=sp(22),

            bold=True,

            color=BOTAO,

            size_hint_y=None,

            height=dp(35)
        )

        self.add_widget(subtitulo)


        # ====================================================
        # INSTRUÇÃO
        # ====================================================

        instrucao = Label(
            text="Resolva equações do 1º grau broh",

            font_size=sp(17),

            color=CINZA,

            size_hint_y=None,

            height=dp(40)
        )

        self.add_widget(instrucao)


        # ====================================================
        # ESPAÇO
        # ====================================================

        self.add_widget(
            Label(
                size_hint_y=None,
                height=dp(5)
            )
        )


        # ====================================================
        # PAINEL DA EQUAÇÃO
        # ====================================================

        painel = PainelArredondado(

            orientation="vertical",

            padding=[
                dp(15),
                dp(15),
                dp(15),
                dp(15)
            ],

            spacing=dp(10),

            size_hint_y=None,

            height=dp(120)
        )

        texto = Label(

            text="DIGITE A EQUAÇÃO broh",

            font_size=sp(14),

            bold=True,

            color=CINZA,

            size_hint_y=None,

            height=dp(30)
        )

        painel.add_widget(texto)


        self.entrada = CampoEquacao(

            text="2x + 6 = 14",

            size_hint_y=None,

            height=dp(62)
        )

        painel.add_widget(self.entrada)

        self.add_widget(painel)


        # ====================================================
        # ESPAÇO
        # ====================================================

        self.add_widget(
            Label(
                size_hint_y=None,
                height=dp(5)
            )
        )


        # ====================================================
        # BOTÃO
        # ====================================================

        self.botao = BotaoResolver(

            text="RESOLVER broh",

            size_hint_y=None,

            height=dp(65)
        )

        self.botao.bind(
            on_press=self.resolver
        )

        self.add_widget(self.botao)


        # ====================================================
        # RESULTADO
        # ====================================================

        self.resultado_painel = PainelArredondado(

            orientation="vertical",

            padding=dp(15),

            size_hint_y=None,

            height=dp(130),

            cor=PAINEL
        )


        resultado_titulo = Label(

            text="RESULTADO broh",

            font_size=sp(14),

            bold=True,

            color=CINZA,

            size_hint_y=None,

            height=dp(30)
        )

        self.resultado_painel.add_widget(
            resultado_titulo
        )


        self.resultado = Label(

            text="Digite uma equação acima broh",

            font_size=sp(25),

            bold=True,

            color=CINZA
        )

        self.resultado_painel.add_widget(
            self.resultado
        )

        self.add_widget(
            self.resultado_painel
        )


        # ====================================================
        # RODAPÉ
        # ====================================================

        self.add_widget(

            Label(

                text="Equações do 1º grau • Projeto em Python broh",

                font_size=sp(12),

                color=CINZA,

                size_hint_y=None,

                height=dp(30)
            )
        )


    # ========================================================
    # BOTÃO RESOLVER
    # ========================================================

    def resolver(self, instance):

        equacao = self.entrada.text

        try:

            resultado = resolver_equacao(equacao)

            self.resultado.text = resultado

            if resultado in (
                "Sem solução broh",
                "Infinitas soluções broh"
            ):

                self.resultado.color = BOTAO

            else:

                self.resultado.color = VERDE

        except Exception:

            self.resultado.text = "Equação inválida broh"

            self.resultado.color = VERMELHO


# ============================================================
# APP
# ============================================================

class AppEquacoes(App):

    def build(self):

        Window.clearcolor = FUNDO

        # Faz a interface subir quando o teclado virtual aparecer
        Window.softinput_mode = "pan"

        return CalculadoraEquacoes()


# ============================================================
# INICIAR
# ============================================================

if __name__ == "__main__":

    AppEquacoes().run()
