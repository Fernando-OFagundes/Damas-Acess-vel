# Damas Acessível

Jogo de Damas desenvolvido na disciplina de Processos Inclusivos do curso de Licenciatura em Computação. 

## Objetivo
Criar jogos simples e acessíveis para pessoas com deficiência visual, proporcionando uma experiência inclusiva através de feedback auditivo e navegação por teclado.

## Características de Acessibilidade

- **Navegação por teclado**: Use as setas para mover o cursor pelo tabuleiro
- **Feedback de voz**: O jogo anuncia a posição atual e o conteúdo de cada casa
- **Sons procedurais**: Diferentes tons sonoros para ações específicas (movimento, captura, seleção)
- **Notação verbal**: Sistema de coordenadas em formato de xadrez (A1, B2, C3, etc.)
- **Instruções por voz**: Tutorial completo acessível via teclado

## Tecnologias Utilizadas

- Python 3.x
- Pygame
- pyttsx3 (síntese de voz)

## Como Executar

1. Certifique-se de ter Python instalado
2. Instale as dependências:
   ```terminal
   pip install pygame pyttsx3
   ```
3. Execute o jogo:
   ```terminal
   python damas_acessivel.py
   ```

## Controles

- **Setas**: Navegar pelo tabuleiro
- **Espaço**: Selecionar peça
- **Enter**: Mover peça selecionada
- **S**: Ligar/Desligar som
- **I**: Instruções completas
- **ESC**: Sair do jogo

## Funcionalidades

- Tabuleiro 8x8 tradicional
- Movimentação diagonal de peças
- Sistema de captura obrigatória
- Detecção automática de vitória
- Feedback auditivo para todas as ações
- Mensagens textuais e por voz
- Interface colorida e de alto contraste

## Estrutura do Projeto

O código está organizado em:
- Inicialização e configuração
- Geração procedural de sons
- Sistema de voz
- Lógica do jogo de damas
- Interface gráfica acessível
- Loop principal de execução

## Desenvolvido por

Fernando O. Fagundes; Lucas P. Klering - Estudantes de Licenciatura em Computação  
Disciplina: Processos Inclusivos: Fundamentos e Práticas
Instituição: Instituto Federal de Educação, Ciência E Tecnologia Farroupilha - Campus Santo Ângelo

*Projeto educacional com foco em acessibilidade digital e inclusão de pessoas com deficiência visual no mundo dos jogos.*
