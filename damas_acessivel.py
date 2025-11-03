import pygame
import sys
import math
import pyttsx3

# =====================
# Inicialização Pygame
# =====================
pygame.init()
SOM_HABILITADO_PADRAO = True
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=1)
except Exception as e:
    print(f"[AVISO] Falha ao iniciar mixer de áudio: {e}. O jogo rodará sem som.")
    SOM_HABILITADO_PADRAO = False

# =====================
# Janela / UI
# =====================
LARGURA, ALTURA = 900, 700
TAMANHO_CASA = 60
MARGEM = 50

# Cores
PRETO   = (0, 0, 0)
BRANCO  = (255, 255, 255)
CINZA   = (200, 200, 200)
VERMELHO= (255, 0, 0)
VERDE   = (0, 255, 0)
AZUL    = (0, 0, 255)
AMARELO = (255, 255, 0)
MARROM  = (139, 69, 19)
ROXO    = (128, 0, 128)

# Fontes
fonte = pygame.font.SysFont('Arial', 16)
fonte_grande = pygame.font.SysFont('Arial', 20)
fonte_titulo = pygame.font.SysFont('Arial', 24, bold=True)

# =====================
# Áudio procedural
# =====================
def gerar_som(frequencia, duracao, tipo='seno'):
    sample_rate = 44100
    amplitude = 4096
    frames = int(duracao * sample_rate)
    buffer = bytearray()
    for i in range(frames):
        t = i / sample_rate
        if tipo == 'seno':
            valor = int(amplitude * math.sin(2 * math.pi * frequencia * t))
        elif tipo == 'quadrado':
            valor = amplitude if math.sin(2 * math.pi * frequencia * t) >= 0 else -amplitude
        else:
            frac = (frequencia * t) % 1.0
            valor = int(amplitude * (2 * frac - 1))
        buffer.extend((valor & 0xFF, (valor >> 8) & 0xFF))
    try:
        return pygame.mixer.Sound(buffer=bytes(buffer))
    except:
        return None

som_movimento = gerar_som(440, 0.10, 'seno')
som_captura   = gerar_som(660, 0.20, 'quadrado')
som_selecao   = gerar_som(330, 0.15, 'seno')
som_erro      = gerar_som(220, 0.30, 'serra')
som_vitoria   = gerar_som(880, 0.50, 'seno')
som_menu      = gerar_som(523, 0.10, 'seno')

# =====================
# Voz
# =====================

def falar(texto):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    print(f"[VOZ] {texto}")
    engine.say(texto)
    engine.runAndWait()

# =====================
# Classe do Jogo
# =====================
class JogoDamasAcessivel:
    def __init__(self):
        # Regras
        self.tamanho_tabuleiro = 8
        self.tabuleiro = self.criar_tabuleiro_vazio()
        self.cursor_pos = [0, 0]
        self.jogador_atual = 1
        self.peca_selecionada = None
        self.movimentos_validos = []
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Damas Acessível com Sons - Pressione I para instruções")
        self.mensagens = []
        self.som_habilitado = SOM_HABILITADO_PADRAO
        self.volume = 0.5
        self.configurar_sons()
        self.inicializar_tabuleiro()
        self.adicionar_mensagem("Jogo de Damas Acessível iniciado!")
        self.adicionar_mensagem("Jogador 1: Vermelho | Jogador 2: Preto")
        self.adicionar_mensagem("Use as setas para navegar")
        self.tocar_som(som_menu)

    def configurar_sons(self):
        for s in (som_movimento, som_captura, som_selecao, som_erro, som_vitoria, som_menu):
            if s: s.set_volume(self.volume)

    def tocar_som(self, som):
        if self.som_habilitado and som:
            try: som.play()
            except: pass

    def criar_tabuleiro_vazio(self):
        return [[0]*self.tamanho_tabuleiro for _ in range(self.tamanho_tabuleiro)]

    def inicializar_tabuleiro(self):
        for i in range(self.tamanho_tabuleiro):
            for j in range(self.tamanho_tabuleiro):
                if (i+j)%2==1:
                    if i<3: self.tabuleiro[i][j] = 1
                    elif i>4: self.tabuleiro[i][j] = 2

    def adicionar_mensagem(self, mensagem):
        self.mensagens.append(mensagem)
        if len(self.mensagens) > 10: self.mensagens.pop(0)
        print(mensagem)

    def coordenadas_para_notacao(self, linha, coluna):
        return f"{chr(65+coluna)}{self.tamanho_tabuleiro - linha}"

    def anunciar_posicao(self):
        linha, coluna = self.cursor_pos
        conteudo = self.tabuleiro[linha][coluna]
        if conteudo==0:
            mensagem = f"Casa {self.coordenadas_para_notacao(linha, coluna)}, vazia"
        elif conteudo==1:
            mensagem = f"Casa {self.coordenadas_para_notacao(linha, coluna)}, peça vermelha"
        else:
            mensagem = f"Casa {self.coordenadas_para_notacao(linha, coluna)}, peça preta"
        self.adicionar_mensagem(mensagem)
        falar(mensagem)

    # =====================
    # Desenho do tabuleiro
    # =====================
    def desenhar_tabuleiro(self):
        self.janela.fill(CINZA)
        titulo = fonte_titulo.render("JOGO DE DAMAS ACESSÍVEL", True, ROXO)
        self.janela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 10))
        status_som = fonte.render(f"SOM: {'LIGADO' if self.som_habilitado else 'DESLIGADO'}", True, VERDE if self.som_habilitado else VERMELHO)
        self.janela.blit(status_som, (LARGURA - 150, 15))
        for i in range(self.tamanho_tabuleiro):
            for j in range(self.tamanho_tabuleiro):
                x = MARGEM + j*TAMANHO_CASA
                y = MARGEM + 40 + i*TAMANHO_CASA
                cor = MARROM if (i+j)%2==0 else BRANCO
                pygame.draw.rect(self.janela, cor, (x, y, TAMANHO_CASA, TAMANHO_CASA))
                pygame.draw.rect(self.janela, PRETO, (x, y, TAMANHO_CASA, TAMANHO_CASA), 1)
                if [i,j]==self.cursor_pos: pygame.draw.rect(self.janela, AMARELO, (x,y,TAMANHO_CASA,TAMANHO_CASA),4)
                if self.peca_selecionada and [i,j]==self.peca_selecionada: pygame.draw.rect(self.janela, AZUL, (x,y,TAMANHO_CASA,TAMANHO_CASA),4)
                if [i,j] in self.movimentos_validos: pygame.draw.rect(self.janela, VERDE, (x,y,TAMANHO_CASA,TAMANHO_CASA),3)
                if self.tabuleiro[i][j]==1:
                    pygame.draw.circle(self.janela, VERMELHO, (x+TAMANHO_CASA//2, y+TAMANHO_CASA//2), TAMANHO_CASA//2-5)
                    pygame.draw.circle(self.janela, PRETO,    (x+TAMANHO_CASA//2, y+TAMANHO_CASA//2), TAMANHO_CASA//2-5,2)
                elif self.tabuleiro[i][j]==2:
                    pygame.draw.circle(self.janela, PRETO,    (x+TAMANHO_CASA//2, y+TAMANHO_CASA//2), TAMANHO_CASA//2-5)
                    pygame.draw.circle(self.janela, BRANCO,   (x+TAMANHO_CASA//2, y+TAMANHO_CASA//2), TAMANHO_CASA//2-7,2)

    # =====================
    # Movimentos e capturas
    # =====================
    def mover_cursor(self, direcao):
        if direcao=='cima' and self.cursor_pos[0]>0: self.cursor_pos[0]-=1
        elif direcao=='baixo' and self.cursor_pos[0]<self.tamanho_tabuleiro-1: self.cursor_pos[0]+=1
        elif direcao=='esquerda' and self.cursor_pos[1]>0: self.cursor_pos[1]-=1
        elif direcao=='direita' and self.cursor_pos[1]<self.tamanho_tabuleiro-1: self.cursor_pos[1]+=1
        self.anunciar_posicao()
        self.tocar_som(som_menu)

    def encontrar_movimentos_validos(self, linha, coluna):
        movimentos=[]
        jogador=self.tabuleiro[linha][coluna]
        if jogador==0: return movimentos
        if jogador==1: direcoes=[(1,-1),(1,1)]
        else: direcoes=[(-1,-1),(-1,1)]
        oponente=2 if jogador==1 else 1
        for d_l,d_c in direcoes:
            nl,nc=linha+d_l,coluna+d_c
            if 0<=nl<8 and 0<=nc<8 and self.tabuleiro[nl][nc]==0:
                movimentos.append((nl,nc))
        for d_l,d_c in direcoes:
            l_meio,c_meio=linha+d_l,coluna+d_c
            l_dest,c_dest=linha+2*d_l,coluna+2*d_c
            if 0<=l_dest<8 and 0<=c_dest<8 and self.tabuleiro[l_meio][c_meio]==oponente and self.tabuleiro[l_dest][c_dest]==0:
                movimentos.append((l_dest,c_dest))
        capturas=[m for m in movimentos if abs(m[0]-linha)==2]
        return capturas if capturas else movimentos

    def selecionar_peca(self):
        linha,coluna=self.cursor_pos
        if self.tabuleiro[linha][coluna]==self.jogador_atual:
            self.peca_selecionada=self.cursor_pos.copy()
            self.movimentos_validos=self.encontrar_movimentos_validos(linha,coluna)
            if self.movimentos_validos:
                msg="Peça selecionada. Movimentos válidos destacados."
                self.adicionar_mensagem(msg); falar(msg)
                self.tocar_som(som_selecao)
            else:
                msg="Nenhum movimento válido para esta peça."
                self.adicionar_mensagem(msg); falar(msg)
                self.peca_selecionada=None
                self.movimentos_validos=[]
                self.tocar_som(som_erro)
        else:
            msg="Não há peça sua nesta casa."
            self.adicionar_mensagem(msg); falar(msg)
            self.tocar_som(som_erro)

    def mover_peca(self):
        if not self.peca_selecionada:
            msg="Nenhuma peça selecionada."
            self.adicionar_mensagem(msg); falar(msg)
            self.tocar_som(som_erro)
            return
        lo,co=self.peca_selecionada
        ld,cd=self.cursor_pos
        if (ld,cd) not in self.movimentos_validos:
            msg="Movimento inválido!"
            self.adicionar_mensagem(msg); falar(msg)
            self.tocar_som(som_erro)
            return
        self.tabuleiro[ld][cd]=self.tabuleiro[lo][co]
        self.tabuleiro[lo][co]=0
        # Captura
        if abs(ld-lo)==2:
            l_cap=(lo+ld)//2
            c_cap=(co+cd)//2
            self.tabuleiro[l_cap][c_cap]=0
            msg=f"Peça capturada em {self.coordenadas_para_notacao(l_cap,c_cap)}!"
            self.adicionar_mensagem(msg); falar(msg)
            self.tocar_som(som_captura)
        else:
            self.tocar_som(som_movimento)
        # Mensagem movimento
        msg=f"Movimento para {self.coordenadas_para_notacao(ld,cd)}"
        self.adicionar_mensagem(msg); falar(msg)
        # Troca jogador
        self.jogador_atual=3-self.jogador_atual
        # Vitória
        if self.verificar_vitoria():
            msg=f"Jogador {3-self.jogador_atual} venceu!"
            self.adicionar_mensagem(msg); falar(msg)
            self.tocar_som(som_vitoria)
        # Reset
        self.peca_selecionada=None
        self.movimentos_validos=[]

    def verificar_vitoria(self):
        pecas1=sum(1 for i in range(8) for j in range(8) if self.tabuleiro[i][j]==1)
        pecas2=sum(1 for i in range(8) for j in range(8) if self.tabuleiro[i][j]==2)
        return pecas1==0 or pecas2==0

    def toggle_som(self):
        self.som_habilitado=not self.som_habilitado
        status="LIGADO" if self.som_habilitado else "DESLIGADO"
        msg=f"Som {status}"
        self.adicionar_mensagem(msg); falar(msg)
        if self.som_habilitado: self.tocar_som(som_menu)

    def mostrar_instrucoes_completas(self):
        instrucoes=[
            "OBJETIVO: Capturar todas as peças do adversário",
            "JOGADOR 1: Vermelho move para BAIXO",
            "JOGADOR 2: Preto move para CIMA",
            "Movimentos: diagonal, 1 casa ou salto 2 para capturar",
            "Captura obrigatória quando disponível"
        ]
        for instrucao in instrucoes: self.adicionar_mensagem(instrucao); falar(instrucao)
        self.tocar_som(som_menu)

    # =====================
    # Loop principal
    # =====================
    def executar(self):
        clock=pygame.time.Clock()
        executando=True
        while executando:
            for e in pygame.event.get():
                if e.type==pygame.QUIT: executando=False
                elif e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_UP: self.mover_cursor('cima')
                    elif e.key==pygame.K_DOWN: self.mover_cursor('baixo')
                    elif e.key==pygame.K_LEFT: self.mover_cursor('esquerda')
                    elif e.key==pygame.K_RIGHT: self.mover_cursor('direita')
                    elif e.key==pygame.K_SPACE: self.selecionar_peca()
                    elif e.key==pygame.K_RETURN: self.mover_peca()
                    elif e.key==pygame.K_s: self.toggle_som()
                    elif e.key==pygame.K_i: self.mostrar_instrucoes_completas()
                    elif e.key==pygame.K_ESCAPE: executando=False
            self.desenhar_tabuleiro()
            pygame.display.flip()
            clock.tick(30)
        pygame.quit()
        sys.exit()

# =====================
# Início do jogo
# =====================
if __name__=="__main__":
    try:
        jogo=JogoDamasAcessivel()
        jogo.executar()
    except Exception as e:
        print(f"Erro: {e}")
        input("Pressione Enter para sair...")

