import re
import math

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.spinner import Spinner


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
# FUNÇÕES AUXILIARES
# ============================================================

def formatar_numero(valor):

    valor = float(valor)

    if valor.is_integer():
        return str(int(valor))

    return f"{valor:.8f}".rstrip("0").rstrip(".")


# ============================================================
# EQUAÇÕES
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

    if coeficiente == 0:

        if termo_independente == 0:
            return "Infinitas soluções broh", ""

        return "Sem solução broh", ""

    x = termo_independente / coeficiente

    calculo = ""

    if c == 0:

        calculo += (
            f"{formatar_numero(a)}x + "
            f"{formatar_numero(b)} = "
            f"{formatar_numero(d)}\n"
        )

    else:

        calculo += (
            f"{formatar_numero(a)}x + "
            f"{formatar_numero(b)} = "
            f"{formatar_numero(c)}x + "
            f"{formatar_numero(d)}\n"
        )

    if c != 0:

        calculo += (
            f"{formatar_numero(a - c)}x = "
            f"{formatar_numero(d - b)}\n"
        )

    else:

        calculo += (
            f"{formatar_numero(a)}x = "
            f"{formatar_numero(d - b)}\n"
        )

    calculo += (
        f"x = {formatar_numero(d - b)} / "
        f"{formatar_numero(a - c)}\n"
    )

    calculo += f"x = {formatar_numero(x)}"

    return f"x = {formatar_numero(x)} broh", calculo


# ============================================================
# ÂNGULOS
# ============================================================

def resolver_angulo(angulo1, angulo2):

    angulo1 = float(
        angulo1.replace("°", "").replace(",", ".").strip()
    )

    angulo2 = float(
        angulo2.replace("°", "").replace(",", ".").strip()
    )

    if angulo1 <= 0 or angulo2 <= 0:
        raise ValueError

    if angulo1 >= 180 or angulo2 >= 180:
        raise ValueError

    terceiro = 180 - angulo1 - angulo2

    if terceiro <= 0:
        raise ValueError

    calculo = (
        "A soma dos ângulos de um triângulo é 180°\n\n"
        f"x = 180° - {formatar_numero(angulo1)}° - "
        f"{formatar_numero(angulo2)}°\n"
        f"x = {formatar_numero(terceiro)}°"
    )

    resultado = f"x = {formatar_numero(terceiro)}° broh"

    return resultado, calculo


# ============================================================
# ÁREAS
# ============================================================

def calcular_area(figura, valores):

    if figura == "Quadrado":

        lado = float(valores[0])

        if lado <= 0:
            raise ValueError

        area = lado ** 2

        calculo = (
            "Fórmula:\n"
            "A = lado²\n\n"
            f"A = {formatar_numero(lado)}²\n"
            f"A = {formatar_numero(area)}"
        )

    elif figura == "Retângulo":

        base = float(valores[0])
        altura = float(valores[1])

        if base <= 0 or altura <= 0:
            raise ValueError

        area = base * altura

        calculo = (
            "Fórmula:\n"
            "A = base × altura\n\n"
            f"A = {formatar_numero(base)} × "
            f"{formatar_numero(altura)}\n"
            f"A = {formatar_numero(area)}"
        )

    elif figura == "Triângulo":

        base = float(valores[0])
        altura = float(valores[1])

        if base <= 0 or altura <= 0:
            raise ValueError

        area = (base * altura) / 2

        calculo = (
            "Fórmula:\n"
            "A = (base × altura) / 2\n\n"
            f"A = ({formatar_numero(base)} × "
            f"{formatar_numero(altura)}) / 2\n"
            f"A = {formatar_numero(base * altura)} / 2\n"
            f"A = {formatar_numero(area)}"
        )

    elif figura == "Círculo":

        raio = float(valores[0])

        if raio <= 0:
            raise ValueError

        area = math.pi * raio ** 2

        calculo = (
            "Fórmula:\n"
            "A = π × r²\n\n"
            f"A = π × {formatar_numero(raio)}²\n"
            f"A = π × {formatar_numero(raio ** 2)}\n"
            f"A ≈ {formatar_numero(area)}"
        )

    elif figura == "Paralelogramo":

        base = float(valores[0])
        altura = float(valores[1])

        if base <= 0 or altura <= 0:
            raise ValueError

        area = base * altura

        calculo = (
            "Fórmula:\n"
            "A = base × altura\n\n"
            f"A = {formatar_numero(base)} × "
            f"{formatar_numero(altura)}\n"
            f"A = {formatar_numero(area)}"
        )

    elif figura == "Trapézio":

        base_maior = float(valores[0])
        base_menor = float(valores[1])
        altura = float(valores[2])

        if base_maior <= 0 or base_menor <= 0 or altura <= 0:
            raise ValueError

        area = ((base_maior + base_menor) * altura) / 2

        calculo = (
            "Fórmula:\n"
            "A = ((B + b) × h) / 2\n\n"
            f"A = (({formatar_numero(base_maior)} + "
            f"{formatar_numero(base_menor)}) × "
            f"{formatar_numero(altura)}) / 2\n"
            f"A = ({formatar_numero(base_maior + base_menor)} × "
            f"{formatar_numero(altura)}) / 2\n"
            f"A = {formatar_numero(area)}"
        )

    else:
        raise ValueError

    return f"Área = {formatar_numero(area)} broh", calculo


# ============================================================
# PAINEL
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
# CAMPO
# ============================================================

class Campo(TextInput):

    def __init__(self, hint="", **kwargs):

        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_active = ""
        self.background_color = CAMPO

        self.foreground_color = BRANCO
        self.cursor_color = BRANCO

        self.selection_color = (
            0.55,
            0.56,
            0.60,
            0.25
        )

        self.font_size = sp(18)

        self.multiline = False
        self.halign = "center"

        self.padding = [
            dp(10),
            dp(10),
            dp(10),
            dp(10)
        ]

        self.hint_text = hint
        self.hint_text_color = CINZA


# ============================================================
# BOTÃO PRINCIPAL
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
# BOTÃO CÁLCULO
# ============================================================

class BotaoCalculo(Button):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""

        self.background_color = PAINEL_2

        self.color = CLARO

        self.font_size = sp(12)
        self.bold = True

        self.bind(
            state=self.mudar_estado
        )

    def mudar_estado(self, instance, estado):

        if estado == "down":
            self.background_color = CINZA_ESCURO
        else:
            self.background_color = PAINEL_2


# ============================================================
# BOTÃO CALCULADORA
# ============================================================

class BotaoCalculadora(Button):

    def __init__(self, tipo="numero", **kwargs):

        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""

        self.tipo = tipo

        if tipo == "igual":

            self.background_color = DESTAQUE
            self.color = (0.02, 0.02, 0.025, 1)

        elif tipo == "operador":

            self.background_color = PAINEL_2
            self.color = DESTAQUE

        elif tipo == "funcao":

            self.background_color = PAINEL_2
            self.color = CLARO

        else:

            self.background_color = CAMPO
            self.color = BRANCO

        self.font_size = sp(25)
        self.bold = True

        self.bind(
            state=self.mudar_estado
        )

    def mudar_estado(self, instance, estado):

        if estado == "down":

            if self.tipo == "igual":
                self.background_color = DESTAQUE_DOWN
            else:
                self.background_color = CINZA_ESCURO

        else:

            if self.tipo == "igual":
                self.background_color = DESTAQUE

            elif self.tipo == "operador":
                self.background_color = PAINEL_2

            elif self.tipo == "funcao":
                self.background_color = PAINEL_2

            else:
                self.background_color = CAMPO


# ============================================================
# BOTÃO EXEMPLO
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
# LINHA
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
# CALCULADORA COMUM
# ============================================================

class CalculadoraComum(BoxLayout):

    def __init__(self, voltar_callback=None, **kwargs):

        super().__init__(
            orientation="vertical",
            spacing=dp(8),
            padding=[
                dp(12),
                dp(10),
                dp(12),
                dp(10)
            ],
            **kwargs
        )

        self.voltar_callback = voltar_callback

        self.expressao = ""
        self.resultado = ""

        # ====================================================
        # CABEÇALHO
        # ====================================================

        topo = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(42),
            spacing=dp(8)
        )

        botao_voltar = Button(
            text="‹",
            size_hint_x=None,
            width=dp(48),
            background_normal="",
            background_down="",
            background_color=PAINEL_2,
            color=BRANCO,
            font_size=sp(28)
        )

        botao_voltar.bind(
            on_release=self.voltar
        )

        topo.add_widget(botao_voltar)

        titulo = Label(
            text="CALCULADORA",
            font_size=sp(21),
            bold=True,
            color=BRANCO,
            halign="left",
            valign="middle"
        )

        titulo.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        topo.add_widget(titulo)

        self.add_widget(topo)

        # ====================================================
        # DISPLAY
        # ====================================================

        self.display = Label(
            text="0",
            font_size=sp(42),
            bold=True,
            color=BRANCO,
            halign="right",
            valign="bottom",
            size_hint_y=None,
            height=dp(115)
        )

        self.display.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        self.add_widget(self.display)

        # ====================================================
        # LINHA DE BOTÕES
        # ====================================================

        botoes = [
            [
                ("AC", "funcao"),
                ("⌫", "funcao"),
                ("%", "operador"),
                ("÷", "operador")
            ],
            [
                ("7", "numero"),
                ("8", "numero"),
                ("9", "numero"),
                ("×", "operador")
            ],
            [
                ("4", "numero"),
                ("5", "numero"),
                ("6", "numero"),
                ("−", "operador")
            ],
            [
                ("1", "numero"),
                ("2", "numero"),
                ("3", "numero"),
                ("+", "operador")
            ],
            [
                ("0", "numero"),
                (".", "numero"),
                ("=", "igual"),
            ]
        ]

        self.grade = BoxLayout(
            orientation="vertical",
            spacing=dp(7)
        )

        for linha in botoes:

            linha_layout = BoxLayout(
                orientation="horizontal",
                spacing=dp(7)
            )

            for texto, tipo in linha:

                botao = BotaoCalculadora(
                    text=texto,
                    tipo=tipo
                )

                if texto == "0":

                    botao.size_hint_x = 2

                else:

                    botao.size_hint_x = 1

                botao.bind(
                    on_release=self.pressionar
                )

                linha_layout.add_widget(botao)

            self.grade.add_widget(linha_layout)

        self.add_widget(self.grade)

    # ========================================================
    # VOLTAR
    # ========================================================

    def voltar(self, instance):

        if self.voltar_callback:
            self.voltar_callback()

    # ========================================================
    # PRESSIONAR
    # ========================================================

    def pressionar(self, botao):

        valor = botao.text

        if valor == "AC":

            self.expressao = ""
            self.resultado = ""
            self.display.text = "0"
            return

        if valor == "⌫":

            self.expressao = self.expressao[:-1]

            if self.expressao:
                self.display.text = self.expressao
            else:
                self.display.text = "0"

            return

        if valor == "=":

            self.calcular()
            return

        if valor == "×":

            valor = "*"

        elif valor == "÷":

            valor = "/"

        elif valor == "−":

            valor = "-"

        elif valor == "%":

            valor = "/100"

        self.expressao += valor

        self.display.text = self.expressao

    # ========================================================
    # CALCULAR
    # ========================================================

    def calcular(self):

        if not self.expressao:
            return

        try:

            expressao = self.expressao

            if not re.fullmatch(
                r"[0-9+\-*/(). ]+",
                expressao
            ):
                raise ValueError

            resultado = eval(
                expressao,
                {
                    "__builtins__": {}
                },
                {}
            )

            if not math.isfinite(float(resultado)):
                raise ValueError

            self.resultado = formatar_numero(resultado)

            self.display.text = self.resultado

            self.expressao = self.resultado

        except Exception:

            self.display.text = "Erro"
            self.expressao = ""


# ============================================================
# INTERFACE PRINCIPAL
# ============================================================

class CalculadoraEquacoes(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(
            orientation="vertical",

            spacing=dp(10),

            padding=[
                dp(20),
                dp(18),
                dp(20),
                dp(8)
            ],

            **kwargs
        )

        self.calculo_texto = ""
        self.calculo_visivel = False

        # ====================================================
        # TÍTULO
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
            text="matemática simplificada",
            font_size=sp(14),
            color=CINZA,
            size_hint_y=None,
            height=dp(24),
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
        # SELETOR
        # ====================================================

        self.seletor = Spinner(
            text="EQUAÇÃO",

            values=[
                "EQUAÇÃO",
                "ÂNGULO",
                "ÁREA",
                "CALCULADORA"
            ],

            size_hint_y=None,
            height=dp(45),

            background_normal="",
            background_color=PAINEL_2,

            color=BRANCO,

            font_size=sp(14)
        )

        self.seletor.bind(
            text=self.mudar_modulo
        )

        self.add_widget(
            self.seletor
        )

        # ====================================================
        # ÁREA PRINCIPAL
        # ====================================================

        self.conteudo = BoxLayout(
            orientation="vertical",
            spacing=dp(10)
        )

        self.add_widget(
            self.conteudo
        )

        self.criar_interface_normal()

    # ========================================================
    # INTERFACE NORMAL
    # ========================================================

    def criar_interface_normal(self):

        self.conteudo.clear_widgets()

        # ====================================================
        # PAINEL DE ENTRADA
        # ====================================================

        self.entrada_painel = Painel(
            orientation="vertical",

            padding=[
                dp(15),
                dp(12),
                dp(15),
                dp(12)
            ],

            spacing=dp(7),

            size_hint_y=None,
            height=dp(185)
        )

        self.conteudo.add_widget(
            self.entrada_painel
        )

        self.titulo_entrada = Label(
            text="DIGITE A EQUAÇÃO",
            font_size=sp(11),
            bold=True,
            color=CINZA,
            size_hint_y=None,
            height=dp(22),
            halign="left",
            valign="middle"
        )

        self.titulo_entrada.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        self.entrada_painel.add_widget(
            self.titulo_entrada
        )

        self.campos = BoxLayout(
            orientation="vertical",
            spacing=dp(7)
        )

        self.entrada_painel.add_widget(
            self.campos
        )

        self.criar_modo_equacao()

        # ====================================================
        # BOTÃO RESOLVER
        # ====================================================

        self.botao = BotaoResolver(
            text="RESOLVER   →   broh",
            size_hint_y=None,
            height=dp(58)
        )

        self.botao.bind(
            on_release=self.resolver
        )

        self.conteudo.add_widget(
            self.botao
        )

        # ====================================================
        # BOTÃO CÁLCULO
        # ====================================================

        self.botao_calculo = BotaoCalculo(
            text="MOSTRAR CÁLCULO",

            size_hint_y=None,

            height=dp(40),

            opacity=0,

            disabled=True
        )

        self.botao_calculo.bind(
            on_release=self.mostrar_calculo
        )

        self.conteudo.add_widget(
            self.botao_calculo
        )

        # ====================================================
        # RESULTADO
        # ====================================================

        self.resultado_painel = Painel(
            orientation="vertical",

            padding=[
                dp(18),
                dp(12),
                dp(18),
                dp(12)
            ],

            spacing=dp(3),

            size_hint_y=None,

            height=dp(145),

            cor=PAINEL_2
        )

        self.conteudo.add_widget(
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

            width=dp(105),

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
            text="Digite uma operação broh",

            font_size=sp(27),

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

            height=dp(20),

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
        # PAINEL CÁLCULO
        # ====================================================

        self.calculo_painel = Painel(
            orientation="vertical",

            padding=[
                dp(18),
                dp(12),
                dp(18),
                dp(12)
            ],

            spacing=dp(5),

            size_hint_y=None,

            height=dp(0),

            opacity=0,

            cor=PAINEL
        )

        calculo_titulo = Label(
            text="CÁLCULO",

            font_size=sp(11),

            bold=True,

            color=CINZA,

            size_hint_y=None,

            height=dp(22),

            halign="left",

            valign="middle"
        )

        calculo_titulo.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        self.calculo_painel.add_widget(
            calculo_titulo
        )

        self.calculo_label = Label(
            text="",

            font_size=sp(15),

            color=CLARO,

            halign="left",

            valign="middle"
        )

        self.calculo_label.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        self.calculo_painel.add_widget(
            self.calculo_label
        )

        self.conteudo.add_widget(
            self.calculo_painel
        )

    # ========================================================
    # CALCULADORA COMUM
    # ========================================================

    def criar_calculadora(self):

        self.conteudo.clear_widgets()

        calculadora = CalculadoraComum(
            voltar_callback=self.voltar_da_calculadora
        )

        self.conteudo.add_widget(
            calculadora
        )

    def voltar_da_calculadora(self):

        self.seletor.text = "EQUAÇÃO"

    # ========================================================
    # LIMPAR CAMPOS
    # ========================================================

    def limpar_campos(self):

        self.campos.clear_widgets()

    # ========================================================
    # EQUAÇÃO
    # ========================================================

    def criar_modo_equacao(self):

        self.limpar_campos()

        self.titulo_entrada.text = "DIGITE A EQUAÇÃO"

        self.entrada = Campo(
            hint="2x + 6 = 14",
            text="2x + 6 = 14"
        )

        self.campos.add_widget(
            self.entrada
        )

        exemplo = Label(
            text="Exemplo: 2x + 6 = 14",
            font_size=sp(10),
            color=CINZA,
            size_hint_y=None,
            height=dp(20)
        )

        self.campos.add_widget(
            exemplo
        )

        self.entrada_painel.height = dp(135)

    # ========================================================
    # ÂNGULO
    # ========================================================

    def criar_modo_angulo(self):

        self.limpar_campos()

        self.titulo_entrada.text = (
            "INFORME OS DOIS ÂNGULOS CONHECIDOS"
        )

        linha = BoxLayout(
            spacing=dp(8)
        )

        self.angulo1 = Campo(
            hint="50°"
        )

        self.angulo2 = Campo(
            hint="70°"
        )

        linha.add_widget(
            self.angulo1
        )

        linha.add_widget(
            self.angulo2
        )

        self.campos.add_widget(
            linha
        )

        info = Label(
            text="O app descobrirá o terceiro ângulo do triângulo.",
            font_size=sp(10),
            color=CINZA,
            size_hint_y=None,
            height=dp(25),
            halign="center",
            valign="middle"
        )

        info.bind(
            size=lambda obj, value:
            setattr(obj, "text_size", value)
        )

        self.campos.add_widget(
            info
        )

        self.entrada_painel.height = dp(135)

    # ========================================================
    # ÁREA
    # ========================================================

    def criar_modo_area(self):

        self.limpar_campos()

        self.titulo_entrada.text = "ESCOLHA A FIGURA"

        self.figura = Spinner(
            text="Quadrado",

            values=[
                "Quadrado",
                "Retângulo",
                "Triângulo",
                "Círculo",
                "Paralelogramo",
                "Trapézio"
            ],

            size_hint_y=None,

            height=dp(42),

            background_normal="",

            background_color=CAMPO,

            color=BRANCO,

            font_size=sp(14)
        )

        self.figura.bind(
            text=self.mudar_figura
        )

        self.campos.add_widget(
            self.figura
        )

        self.area_campos = BoxLayout(
            orientation="vertical",
            spacing=dp(6)
        )

        self.campos.add_widget(
            self.area_campos
        )

        self.criar_campos_area("Quadrado")

        self.entrada_painel.height = dp(190)

    # ========================================================
    # CAMPOS ÁREA
    # ========================================================

    def criar_campos_area(self, figura):

        self.area_campos.clear_widgets()

        if figura == "Quadrado":

            self.area_lado = Campo(
                hint="Lado"
            )

            self.area_campos.add_widget(
                self.area_lado
            )

        elif figura == "Retângulo":

            self.area_base = Campo(
                hint="Base"
            )

            self.area_altura = Campo(
                hint="Altura"
            )

            self.area_campos.add_widget(
                self.area_base
            )

            self.area_campos.add_widget(
                self.area_altura
            )

        elif figura == "Triângulo":

            self.area_base = Campo(
                hint="Base"
            )

            self.area_altura = Campo(
                hint="Altura"
            )

            self.area_campos.add_widget(
                self.area_base
            )

            self.area_campos.add_widget(
                self.area_altura
            )

        elif figura == "Círculo":

            self.area_raio = Campo(
                hint="Raio"
            )

            self.area_campos.add_widget(
                self.area_raio
            )

        elif figura == "Paralelogramo":

            self.area_base = Campo(
                hint="Base"
            )

            self.area_altura = Campo(
                hint="Altura"
            )

            self.area_campos.add_widget(
                self.area_base
            )

            self.area_campos.add_widget(
                self.area_altura
            )

        elif figura == "Trapézio":

            self.area_base_maior = Campo(
                hint="Base maior"
            )

            self.area_base_menor = Campo(
                hint="Base menor"
            )

            self.area_altura = Campo(
                hint="Altura"
            )

            self.area_campos.add_widget(
                self.area_base_maior
            )

            self.area_campos.add_widget(
                self.area_base_menor
            )

            self.area_campos.add_widget(
                self.area_altura
            )

    # ========================================================
    # MUDAR FIGURA
    # ========================================================

    def mudar_figura(self, spinner, figura):

        self.criar_campos_area(figura)

        self.esconder_calculo()

    # ========================================================
    # MUDAR MÓDULO
    # ========================================================

    def mudar_modulo(self, spinner, modulo):

        if modulo == "CALCULADORA":

            self.criar_calculadora()
            return

        self.criar_interface_normal()

        self.esconder_calculo()

        self.resultado.text = "Digite os valores broh"

        self.resultado.color = CLARO

        self.status.text = "PRONTO broh"

        if modulo == "EQUAÇÃO":

            self.criar_modo_equacao()

        elif modulo == "ÂNGULO":

            self.criar_modo_angulo()

        elif modulo == "ÁREA":

            self.criar_modo_area()

    # ========================================================
    # MOSTRAR CÁLCULO
    # ========================================================

    def mostrar_calculo(self, instance):

        if not self.calculo_texto:
            return

        self.calculo_visivel = not self.calculo_visivel

        if self.calculo_visivel:

            self.calculo_label.text = self.calculo_texto

            linhas = self.calculo_texto.count("\n") + 1

            altura = max(
                dp(130),
                dp(30) * linhas + dp(45)
            )

            self.calculo_painel.height = altura

            self.calculo_painel.opacity = 1

            self.botao_calculo.text = "OCULTAR CÁLCULO"

        else:

            self.calculo_painel.height = dp(0)

            self.calculo_painel.opacity = 0

            self.botao_calculo.text = "MOSTRAR CÁLCULO"

    # ========================================================
    # ESCONDER CÁLCULO
    # ========================================================

    def esconder_calculo(self):

        self.calculo_texto = ""
        self.calculo_visivel = False

        if hasattr(self, "calculo_label"):

            self.calculo_label.text = ""

            self.calculo_painel.height = dp(0)
            self.calculo_painel.opacity = 0

            self.botao_calculo.text = "MOSTRAR CÁLCULO"

            self.botao_calculo.opacity = 0
            self.botao_calculo.disabled = True

    # ========================================================
    # RESOLVER
    # ========================================================

    def resolver(self, instance):

        self.esconder_calculo()

        # ====================================================
        # EQUAÇÃO
        # ====================================================

        if self.seletor.text == "EQUAÇÃO":

            equacao = self.entrada.text.strip()

            if equacao.lower() == "broh":

                self.resultado.text = "Arthur broh supremo"

                self.resultado.color = DESTAQUE

                self.status.text = "EASTER EGG broh"

                return

            equacao_limpa = equacao.replace(
                "broh",
                ""
            ).strip()

            try:

                resultado, calculo = resolver_equacao(
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

                    self.calculo_texto = calculo

                    self.botao_calculo.opacity = 1
                    self.botao_calculo.disabled = False

            except Exception:

                self.resultado.text = "Equação inválida broh"

                self.resultado.color = VERMELHO

                self.status.text = "ERRO broh"

        # ====================================================
        # ÂNGULO
        # ====================================================

        elif self.seletor.text == "ÂNGULO":

            try:

                resultado, calculo = resolver_angulo(
                    self.angulo1.text,
                    self.angulo2.text
                )

                self.resultado.text = resultado

                self.resultado.color = VERDE

                self.status.text = "RESOLVIDO broh"

                self.calculo_texto = calculo

                self.botao_calculo.opacity = 1
                self.botao_calculo.disabled = False

            except Exception:

                self.resultado.text = "Ângulos inválidos broh"

                self.resultado.color = VERMELHO

                self.status.text = "ERRO broh"

        # ====================================================
        # ÁREA
        # ====================================================

        elif self.seletor.text == "ÁREA":

            try:

                figura = self.figura.text

                valores = []

                if figura == "Quadrado":

                    valores = [
                        self.area_lado.text
                    ]

                elif figura in (
                    "Retângulo",
                    "Triângulo",
                    "Paralelogramo"
                ):

                    valores = [
                        self.area_base.text,
                        self.area_altura.text
                    ]

                elif figura == "Círculo":

                    valores = [
                        self.area_raio.text
                    ]

                elif figura == "Trapézio":

                    valores = [
                        self.area_base_maior.text,
                        self.area_base_menor.text,
                        self.area_altura.text
                    ]

                valores = [
                    valor.replace(",", ".")
                    for valor in valores
                ]

                resultado, calculo = calcular_area(
                    figura,
                    valores
                )

                self.resultado.text = resultado

                self.resultado.color = VERDE

                self.status.text = "RESOLVIDO broh"

                self.calculo_texto = calculo

                self.botao_calculo.opacity = 1
                self.botao_calculo.disabled = False

            except Exception:

                self.resultado.text = "Valores inválidos broh"

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
