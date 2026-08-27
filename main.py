import re

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


# ============================================================
# CORES
# ============================================================

FUNDO = (0.025, 0.027, 0.032, 1)

PAINEL = (0.060, 0.063, 0.070, 1)
PAINEL_2 = (0.075, 0.078, 0.087, 1)
CAMPO = (0.035, 0.037, 0.043, 1)

BRANCO = (0.95, 0.955, 0.97, 1)
CLARO = (0.78, 0.79, 0.82, 1)
CINZA = (0.52, 0.53, 0.57, 1)
CINZA_ESCURO = (0.18, 0.19, 0.21, 1)

DESTAQUE = (0.88, 0.89, 0.92, 1)
DESTAQUE_DOWN = (0.70, 0.72, 0.76, 1)

VERDE = (0.30, 0.86, 0.48, 1)
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


def formatar_numero(valor):

    valor = float(valor)

    if valor.is_integer():
        return str(int(valor))

    return f"{valor:.8f}".rstrip("0").rstrip(".")


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

    return f"x = {formatar_numero(x)} broh"


# ============================================================
# PAINEL ARREDONDADO
# ============================================================

class Painel(BoxLayout):

    def __init__(
        self,
        cor=PAINEL,
        borda=CINZA_ESCURO,
        raio=24,
        **kwargs
    ):

        super().__init__(**kwargs)

        with self.canvas.before:

            Color(*cor)

            self.fundo = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(raio)]
            )

            Color(*borda)

            self.contorno = Line(
                rounded_rectangle=(
                    self.x,
                    self.y,
                    self.width,
                    self.height,
                    dp(raio)
                ),
                width=0.8
            )

        self.bind(
            pos=self.atualizar,
            size=self.atualizar
        )

    def atualizar(self, *args):

        self.fundo.pos = self.pos
        self.fundo.size = self.size

        self.contorno.rounded_rectangle = (
            self.x,
            self.y,
            self.width,
            self.height,
            dp(24)
        )


# ============================================================
# CAMPO DE EQUAÇÃO
# ============================================================

class CampoEquacao(TextInput):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_active = ""
        self.background_color = (0, 0, 0, 0)

        self.foreground_color = BRANCO
        self.cursor_color = BRANCO

        self.selection_color = (
            0.55,
            0.56,
            0.60,
            0.25
        )

        self.font_size = sp(25)

        self.multiline = False
        self.halign = "center"

        self.padding = [
            dp(15),
            dp(13),
            dp(15),
            dp(13)
        ]

        self.hint_text = "2x + 6 = 14"
        self.hint_text_color = CINZA

        self.write_tab = False


# ============================================================
# BOTÃO RESOLVER
# ============================================================

class BotaoResolver(Button):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""

        self.background_color = DESTAQUE

        self.color = (
            0.02,
            0.02,
            0.025,
            1
        )

        self.font_size = sp(18)
        self.bold = True

        self.bind(
            state=self.mudar_estado
        )

    def mudar_estado(self, instance, estado):

        if estado == "down":

            self.background_color = DESTAQUE_DOWN

        else:

            self.background_color = DESTAQUE


# ============================================================
# BOTÃO DE EXEMPLO
# ============================================================

class BotaoExemplo(Button):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""

        self.background_color = PAINEL_2

        self.color = CLARO

        self.font_size = sp(11)

        self.bind(
            state=self.mudar_estado
        )

    def mudar_estado(self, instance, estado):

        if estado == "down":

            self.background_color = CINZA_ESCURO

        else:

            self.background_color = PAINEL_2


# ============================================================
# LINHA DECORATIVA
# ============================================================

class LinhaDecorativa(Widget):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        with self.canvas:

            Color(
                0.50,
                0.51,
                0.54,
                0.35
            )

            self.linha = Line(
                points=[
                    0,
                    dp(1),
                    dp(95),
                    dp(1)
                ],
                width=1.2
            )

        self.bind(
            pos=self.atualizar,
            size=self.atualizar
        )

    def atualizar(self, *args):

        tamanho = min(
            dp(110),
            self.width * 0.28
        )

        self.linha.points = [
            self.x,
            self.y + dp(1),
            self.x + tamanho,
            self.y + dp(1)
        ]


# ============================================================
# INTERFACE
# ============================================================

class CalculadoraEquacoes(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(
            orientation="vertical",

            spacing=dp(12),

            padding=[
                dp(20),
                dp(22),
                dp(20),
                dp(10)
            ],

            **kwargs
        )

        # ====================================================
        # CABEÇALHO
        # ====================================================

        titulo = Label(

            text="CALCULADORA broh",

            font_size=sp(29),

            bold=True,

            color=BRANCO,

            size_hint_y=None,

            height=dp(40),

            halign="left",

            valign="middle"
        )

        titulo.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        self.add_widget(titulo)


        subtitulo = Label(

            text="equações do 1º grau",

            font_size=sp(14),

            color=CINZA,

            size_hint_y=None,

            height=dp(25),

            halign="left",

            valign="middle"
        )

        subtitulo.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        self.add_widget(subtitulo)


        self.add_widget(

            LinhaDecorativa(

                size_hint_y=None,

                height=dp(8)
            )
        )


        # ====================================================
        # PAINEL DA EQUAÇÃO
        # ====================================================

        painel = Painel(

            orientation="vertical",

            padding=[
                dp(17),
                dp(15),
                dp(17),
                dp(15)
            ],

            spacing=dp(7),

            size_hint_y=None,

            height=dp(142)
        )

        self.add_widget(painel)


        label_equacao = Label(

            text="DIGITE A EQUAÇÃO broh",

            font_size=sp(11),

            bold=True,

            color=CINZA,

            size_hint_y=None,

            height=dp(22),

            halign="left",

            valign="middle"
        )

        label_equacao.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        painel.add_widget(label_equacao)


        # ====================================================
        # CAMPO INTERNO
        # ====================================================

        campo_card = BoxLayout(

            padding=[
                dp(4),
                dp(3),
                dp(4),
                dp(3)
            ],

            size_hint_y=None,

            height=dp(72)
        )

        with campo_card.canvas.before:

            Color(*CAMPO)

            self.campo_fundo = RoundedRectangle(

                pos=campo_card.pos,

                size=campo_card.size,

                radius=[dp(20)]
            )

            Color(
                0.16,
                0.17,
                0.19,
                1
            )

            self.campo_contorno = Line(

                rounded_rectangle=(
                    campo_card.x,
                    campo_card.y,
                    campo_card.width,
                    campo_card.height,
                    dp(20)
                ),

                width=0.8
            )

        campo_card.bind(
            pos=self.atualizar_campo,
            size=self.atualizar_campo
        )


        self.entrada = CampoEquacao(

            text="2x + 6 = 14"
        )

        campo_card.add_widget(
            self.entrada
        )

        painel.add_widget(
            campo_card
        )


        # ====================================================
        # EXEMPLOS
        # ====================================================

        exemplos_titulo = Label(

            text="EXEMPLOS",

            font_size=sp(10),

            color=CINZA,

            size_hint_y=None,

            height=dp(18),

            halign="left",

            valign="middle"
        )

        exemplos_titulo.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        self.add_widget(
            exemplos_titulo
        )


        exemplos = BoxLayout(

            spacing=dp(8),

            size_hint_y=None,

            height=dp(34)
        )


        exemplo1 = BotaoExemplo(
            text="2x + 6 = 14"
        )

        exemplo2 = BotaoExemplo(
            text="3x - 9 = 0"
        )


        exemplo1.bind(
            on_release=self.usar_exemplo
        )

        exemplo2.bind(
            on_release=self.usar_exemplo
        )


        exemplos.add_widget(
            exemplo1
        )

        exemplos.add_widget(
            exemplo2
        )


        self.add_widget(
            exemplos
        )


        # ====================================================
        # BOTÃO PRINCIPAL
        # ====================================================

        self.botao = BotaoResolver(

            text="RESOLVER   →   broh",

            size_hint_y=None,

            height=dp(62)
        )

        self.botao.bind(
            on_release=self.resolver
        )

        self.add_widget(
            self.botao
        )


        # ====================================================
        # RESULTADO
        # ====================================================

        self.resultado_painel = Painel(

            orientation="vertical",

            padding=[
                dp(18),
                dp(14),
                dp(18),
                dp(14)
            ],

            spacing=dp(3),

            size_hint_y=None,

            height=dp(158),

            cor=PAINEL_2
        )

        self.add_widget(
            self.resultado_painel
        )


        topo = BoxLayout(

            orientation="horizontal",

            size_hint_y=None,

            height=dp(22)
        )


        resultado_titulo = Label(

            text="RESULTADO",

            font_size=sp(11),

            bold=True,

            color=CINZA,

            halign="left",

            valign="middle"
        )

        resultado_titulo.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        topo.add_widget(
            resultado_titulo
        )


        self.status = Label(

            text="PRONTO broh",

            font_size=sp(10),

            color=CINZA,

            size_hint_x=None,

            width=dp(82),

            halign="right",

            valign="middle"
        )

        self.status.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        topo.add_widget(
            self.status
        )


        self.resultado_painel.add_widget(
            topo
        )


        self.resultado = Label(

            text="Digite uma equação broh",

            font_size=sp(31),

            bold=True,

            color=CLARO,

            halign="center",

            valign="middle"
        )

        self.resultado.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        self.resultado_painel.add_widget(
            self.resultado
        )


        detalhe = Label(

            text="A resposta aparecerá aqui broh",

            font_size=sp(10),

            color=CINZA,

            size_hint_y=None,

            height=dp(21),

            halign="center",

            valign="middle"
        )

        detalhe.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        self.resultado_painel.add_widget(
            detalhe
        )


        # ====================================================
        # MARCA D'ÁGUA
        # ====================================================

        marca = Label(

            text="Produzido por Arthur Fefeira",

            font_size=sp(9),

            color=(
                0.30,
                0.31,
                0.34,
                0.75
            ),

            size_hint_y=None,

            height=dp(22),

            halign="center",

            valign="middle"
        )

        marca.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        self.add_widget(
            marca
        )


        # ====================================================
        # RODAPÉ
        # ====================================================

        rodape = Label(

            text="1º GRAU  •  PYTHON + KIVY  •  broh",

            font_size=sp(8),

            color=(
                0.22,
                0.23,
                0.26,
                1
            ),

            size_hint_y=None,

            height=dp(16),

            halign="center",

            valign="middle"
        )

        rodape.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        self.add_widget(
            rodape
        )


    # ========================================================
    # ATUALIZAR CAMPO
    # ========================================================

    def atualizar_campo(self, instance, *args):

        self.campo_fundo.pos = instance.pos

        self.campo_fundo.size = instance.size

        self.campo_contorno.rounded_rectangle = (

            instance.x,

            instance.y,

            instance.width,

            instance.height,

            dp(20)
        )


    # ========================================================
    # USAR EXEMPLO
    # ========================================================

    def usar_exemplo(self, button):

        self.entrada.text = button.text

        self.resultado.text = "Pronto broh"

        self.resultado.color = CLARO

        self.status.text = "EXEMPLO broh"


    # ========================================================
    # RESOLVER
    # ========================================================

    def resolver(self, instance):

        equacao = self.entrada.text.strip()


        # ====================================================
        # EASTER EGG 👀
        # ====================================================

        if equacao.lower() == "broh":

            self.resultado.text = "Arthur broh supremo"

            self.resultado.color = DESTAQUE

            self.status.text = "EASTER EGG broh"

            return


        # ====================================================
        # RESOLUÇÃO NORMAL
        # ====================================================

        equacao_limpa = equacao.replace(
            "broh",
            ""
        ).strip()


        try:

            resultado = resolver_equacao(
                equacao_limpa
            )

            self.resultado.text = resultado


            if resultado in (

                "Sem solução broh",

                "Infinitas soluções broh"
            ):

                self.resultado.color = DESTAQUE

                self.status.text = "ATENÇÃO broh"


            else:

                self.resultado.color = VERDE

                self.status.text = "RESOLVIDO broh"


        except Exception:

            self.resultado.text = "Equação inválida broh"

            self.resultado.color = VERMELHO

            self.status.text = "ERRO broh"


# ============================================================
# APP
# ============================================================

class AppEquacoes(App):

    def build(self):

        Window.clearcolor = FUNDO

        Window.softinput_mode = "pan"

        return CalculadoraEquacoes()


# ============================================================
# INICIAR
# ============================================================

if __name__ == "__main__":

    AppEquacoes().run()
