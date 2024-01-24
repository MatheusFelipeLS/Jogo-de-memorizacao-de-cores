from flet import *
from flet import colors
from random import randint
from time import sleep

botao = [
    {'num': '0', 'cor': colors.ORANGE},
    {'num': '1', 'cor': colors.BLUE},
    {'num': '2', 'cor': colors.RED},
    {'num': '3', 'cor': colors.PURPLE}
]

ordemGame = []
ordemGame.append(randint(0, 3))
ordemClicada = -1

pos = -1

def main(page: Page):
    page.window_width = 250
    page.window_height = 250
    page.title = 'Jogo da memória'
    page.window_always_on_top = True
    
    def mostrarOrdem(e=0):
        i = 0
        btn[0].disabled = btn[1].disabled = btn[2].disabled = btn[3].disabled = True 
        keyboard.update()
        while(i < len(ordemGame)):
            corOriginal = btn[ordemGame[i]].bgcolor
            if(ordemGame[i] == 0):
                btn[ordemGame[i]].bgcolor = colors.ORANGE_900
                btn[ordemGame[i]].content.color = colors.ORANGE_900
            elif(ordemGame[i] == 1):
                btn[ordemGame[i]].bgcolor = colors.BLUE_900 
                btn[ordemGame[i]].content.color = colors.BLUE_900 
            elif(ordemGame[i] == 2):
                btn[ordemGame[i]].bgcolor = colors.RED_900 
                btn[ordemGame[i]].content.color = colors.RED_900
            elif(ordemGame[i] == 3):
                btn[ordemGame[i]].bgcolor = colors.PURPLE_900
                btn[ordemGame[i]].content.color = colors.PURPLE_900
            

            if(i > 0):
                if(btn[ordemGame[i]] == btn[ordemGame[i-1]]):
                    sleep(0.4)
                    
            btn[ordemGame[i]].update()
            sleep(0.4)
            
            btn[ordemGame[i]].bgcolor = corOriginal
            btn[ordemGame[i]].content.color = corOriginal
                
            btn[ordemGame[i]].update()
            
            i += 1
            
        btn[0].disabled = btn[1].disabled = btn[2].disabled = btn[3].disabled = False
        keyboard.update()
            
    
    def select(e):
        global pos
        corOriginal = e.control.bgcolor
        clicado = e.control.content.value
        if(clicado == '0'):
            e.control.bgcolor = colors.ORANGE_900
            e.control.content.color = colors.ORANGE_900
        elif(clicado == '1'):
            e.control.bgcolor = colors.BLUE_900 
            e.control.content.color = colors.BLUE_900 
        elif(clicado == '2'):
            e.control.bgcolor = colors.RED_900 
            e.control.content.color = colors.RED_900
        elif(clicado == '3'):
            e.control.bgcolor = colors.PURPLE_900
            e.control.content.color = colors.PURPLE_900
        

        e.control.update()
        sleep(0.2)
        
        e.control.bgcolor = corOriginal
        e.control.content.color = corOriginal
        
        pos += 1
        print(f"j: {e.control.content.value}")
        print(f'pos: {pos}')
        if(int(clicado) != ordemGame[pos]):
            print('a')
            page.go("/over")
        else:
            if(pos == len(ordemGame)-1):
                ordemGame.append(randint(0,3))
                e.control.update()
                print(f'{ordemGame}')
                box.content.value = f'Pontuação: {pos+1}'
                box.update() 
                sleep(1.5)
                mostrarOrdem()
                pos = -1
                
            e.control.update()
        
    
    def prepararGame(e=0):
        page.go("/jogo")
        global pos
        pos = -1
        ordemGame.clear()
        ordemGame.append(randint(0,3))
        box.content.value = f'Pontuação: {0}'
        box.update() 
        pass
    
    btn = [Container(
        content=Text(value=btn['num'], color=btn['cor']),
        width=100,
        height=100,
        border_radius=20,
        bgcolor=btn['cor'],
        on_click=select
    ) for btn in botao]
    
    
    keyboard = Row(
        width=250, 
        wrap=True,
        controls=btn, 
        alignment='end'
    )
    
    box = Container(
        content=Text(value=f'Pontuação: {pos+1}', color="white"),
        width=250,
        height=40,
        bgcolor="green"
    )
    
    start = ElevatedButton("Start", on_click=mostrarOrdem)
    
    def route_change(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Pagina Inicial"), bgcolor=colors.SURFACE_VARIANT),
                    ElevatedButton("JOGAR", on_click=prepararGame),
                    ElevatedButton("CONFIGURAÇÕES", on_click=lambda _: page.go("/config"))
                ],
            )
        )
        if page.route == "/jogo":
            page.views.append(
                View(
                    "/jogo",
                    [
                        AppBar(title=Text("Jogo de memorização"), bgcolor=colors.SURFACE_VARIANT),
                        keyboard,
                        start,
                        box
                    ],
                )
            )
        if page.route == "/config":
            page.views.append(
                View(
                    "/config",
                    [
                        AppBar(title=Text("Configurações"), bgcolor=colors.SURFACE_VARIANT),
                        # ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        if page.route == "/over":
            page.views.append(
                View(
                    "/over", 
                    [
                    AppBar(title=Text("Game over"), bgcolor=colors.SURFACE_VARIANT),
                    ElevatedButton("INÍCIO", on_click=lambda _: page.go("/")),
                    ElevatedButton("JOGAR NOVAMENTE", on_click=prepararGame)
                    ],
                )
            )
            
        page.update()
    
    
    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)
    
    
app(target = main)