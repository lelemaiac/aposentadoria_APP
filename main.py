import flet as ft
from flet import AppBar, Text, ElevatedButton, View, Margin, Dropdown
from flet.core.colors import  Colors
from flet.core.dropdown import Option
from flet.core.types import MainAxisAlignment, CrossAxisAlignment
from datetime import datetime


def main(page: ft.Page):
    #Configuração das páginas
    page.title = "Minha Aplicação Flet"
    page.theme_mode = ft.ThemeMode.LIGHT #ou ft.ThemeMode.FFDF9B
    page.window.width = 375
    page.window.height = 667

    def gerenciar_rotas(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                (
                    ft.Container(
                        ft.Image(src="INSS.png"),
                        margin=30,
                    ),

                    ElevatedButton(text="Simular",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: page.go("/simular"),
                                       bgcolor=Colors.BLACK),

                    ElevatedButton(
                        text="Ver regras",
                        color=ft.Colors.BLACK,
                        on_click=lambda _: page.go("/regras"),
                        bgcolor=Colors.WHITE,
                    ),

                ),
                bgcolor='#FFDF9B',
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        )

        if page.route == "/simular":
            page.views.append(
                View(
                    "/simular",
                    [
                        AppBar(title=Text("Simular"), bgcolor="#FFDF9B"),
                        input_idade,
                        genero,
                        input_contribuicao,
                        input_salarial,
                        categoria,
                        ElevatedButton(text="Enviar",
                                       color=ft.Colors.WHITE,
                                       on_click=lambda _: calcular(e),
                                       bgcolor=Colors.BLACK),

                    ],
                    bgcolor = '#FFDF9B',
                    horizontal_alignment=CrossAxisAlignment.CENTER,

                )
            )

        elif page.route == "/regras":
            page.views.append(
                View(
                    "/regras",
                    [
                        AppBar(title=Text("Regras"), bgcolor="#FFDF9B"),
                        Text("2.1. Aposentadoria por Idade:\n2.1.1. Homens: 65"
                             " anos de idade e pelo menos 15 anos de contribuição.\n "
                             "2.1.2. Mulheres: 62 anos de idade e pelo menos 15 anos"
                             " de contribuição."),
                        Text("2.2. Aposentadoria por Tempo de Contribuição:\n"
                             "  2.2.1. Homens: 35 anos de contribuição.\n"
                             " 2.2.2. Mulheres: 30 anos de contribuição. "),
                        Text("2.3. Valor Estimado do Benefício: O valor da aposentadoria\n"
                             " será uma média de 60% da média salarial informada, acrescido\n"
                             " de 2% por ano que exceder o tempo mínimo de contribuição")

                    ],
                    bgcolor = '#FFDF9B',
                )
            )

        elif page.route == "/resultado":
            page.views.append(
                View(
                    "/resultado",
                    [

                        AppBar(title=Text("Resultado"), bgcolor="#FFDF9B"),
                        txt_data,
                        txt_valor,
                    ],
                    bgcolor = '#FFDF9B',
                )
            )
        page.update()


    page.on_route_change = gerenciar_rotas
    page.go(page.route)


    input_idade = ft.TextField(label="Idade Atual", hint_text="Digite sua idade", bgcolor=Colors.WHITE)
    input_contribuicao = ft.TextField(label="Tempo de Contribuição", hint_text="Digite o tempo de contribuição", bgcolor=Colors.WHITE)
    input_salarial = ft.TextField(label="Média Salarial", hint_text="Digite a média salarial", bgcolor=Colors.WHITE)
    categoria = ft.Dropdown(label="Categoria da aposentadoria", bgcolor=Colors.WHITE,
                        options=[Option(key="idade", text="Aposentadoria por idade"),
                                 Option(key="tempo", text="Aposentadoria por tempo de contribuição")])
    genero = ft.Dropdown(label="Genero", width=page.window.width,
                            options=[Option(key="masc", text="Masculino"),
                                     Option(key="fem", text="Feminino")])
    txt_resultado = ft.Text(value="")
    txt_data = ft.Text(value="")
    txt_valor = ft.Text(value="")


    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = gerenciar_rotas
    page.on_view_pop = voltar

    def conta(e):
        try:
            valor_contri = int(input_contribuicao.value)
            valor_salario = int(input_salarial.value)
            media = (valor_salario * 60)/100
            print(media)
            if valor_contri > 15:
                diferenca = (valor_contri - 15) * 2
                acrescentado = (valor_salario * diferenca) / 100
                resultado = (acrescentado + media)
                return resultado
            else:
                return media

        except Exception as e:
            txt_resultado.value = "As informações devem ser números inteiros."
        except TypeError:
            txt_resultado.value = "fffffffffffff"


    def calcular(e):
        try:
            valor_idade = int(input_idade.value)
            valor_contribuicao = int(input_contribuicao.value)
            valor_salario = int(input_salarial.value)
            resultado_conta = conta(e)

            if genero.value == "masc" and categoria.value == "idade":
                if valor_idade >= 65 and valor_contribuicao >= 15:
                    txt_valor.value = f'O valor estimado é R$ {resultado_conta}'

                else:
                    diferenca_idade = abs(valor_idade - 65)
                    diferenca_contribuicao = abs(valor_contribuicao - 15)
                    ano_atual = datetime.today().year
                    data_prevista = abs(ano_atual + diferenca_idade) or abs(ano_atual + diferenca_contribuicao)
                    txt_data.value = f'A data estimada para a aposentadoria é {data_prevista}'

            elif genero.value == "fem" and categoria.value == "idade":
                if valor_idade >= 62 and valor_contribuicao >= 15:
                    txt_valor.value = f'O valor estimado é R$ {resultado_conta}'
                else:
                    diferenca_idade = abs(valor_idade - 62)
                    diferenca_contribuicao = abs(valor_contribuicao - 15)
                    ano_atual = datetime.today().year
                    data_prevista = abs(ano_atual + diferenca_idade) or abs(ano_atual + diferenca_contribuicao)
                    txt_data.value = f'A data estimada para a aposentadoria é {data_prevista}'

            if genero.value == "fem" and categoria.value == "tempo":
                if valor_contribuicao >= 30:
                    media = (valor_salario * 60)/100
                    if valor_contribuicao > 30:
                        diferenca = (valor_contribuicao - 30) * 2
                        acrescentado = media * diferenca
                        txt_valor.value = f'O valor estimado é R$ {acrescentado}'
                else:
                    diferenca_contribuicao = abs(valor_contribuicao - 15)
                    ano_atual = datetime.today().year
                    data_prevista = abs(ano_atual + diferenca_contribuicao)
                    txt_data.value = f'A data estimada para a aposentadoria é {data_prevista}'


            if genero.value == "masc" and categoria.value == "tempo":
                if valor_contribuicao >= 35:
                    media = (valor_salario * 60)/100
                    if valor_contribuicao > 35:
                        diferenca = (valor_contribuicao - 35) * 2
                        acrescentado = media * diferenca
                        txt_valor.value = f'O valor estimado é R$ {acrescentado}'
                else:
                    diferenca_contribuicao = abs(valor_contribuicao - 15)
                    ano_atual = datetime.today().year
                    data_prevista = abs(ano_atual + diferenca_contribuicao)
                    txt_data.value = f'A data estimada para a aposentadoria é {data_prevista}'

        except Exception as e:
            txt_resultado.value = "Os valores estão incorretos, tente novamente, lembrando que tem que ser números inteiros."
        except TypeError:
            txt_resultado.value = "hhhhhhhh"

        page.go("/resultado")

ft.app(main)