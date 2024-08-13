# Algebra Linear - APS 1

## Integrantes do Grupo
- [Ian Cordibello Desponds](https://github.com/iancdesponds)
- [Gustavo Barroso Cruz](https://github.com/Gubscruz)

## Requisitos:
1. Clone o repositório no seu computador
2. Execute o comando 'pip3 install -r requirements.txt' para instalar as dependências necessárias
3. Execute o arquivo 'game.py'

## Descrição:
O jogo, inspirado no filme "O Retorno do Jedi", consiste em uma nave espacial X-Wing que atira lasers na direção que o mouse aponta na hora do clique. A missão é destruir a Estrela da Morte. Os planetas espalhados pelo mapa exercem uma força gravitacional sobre os projéteis, podendo desviar sua trajetória se passarem muito perto. Além disso, os planetas são habitados e, portanto, se mais de dois projéteis atingirem planetas a missão será falha.

## O modelo físico:
Atirar: No momento em que o mouse é clicado para atirar, o programa calcula as distâncias (dx e dy) nos eixos X e Y entre a posição da nave e a posição do mouse. Na função get_angle_and_magnitude usamos $\arctan{dy/dx}$ para encontrar o ângulo de lançamento do projétil e $\sqrt{dx^2 + dy^2}$ para encontrar o módulo do vetor direção do projétil. Na função shoot, multiplicamos o módulo do vetor direção por uma constante para melhorar a jogabilidade e, em seguida, para encontrar as componentes $V_x$ e $V_y$ da velocidade inicial do projétil, multiplicamos o resultado pelo cosseno (para $V_x$) e seno (para $V_y$). Por fim, adicionamos cada componente do vetor direção encontrado à posição do projétil para atualizar sua posição a cada frame, gerando um movimento retilíneo uniforme, já que os incrementos da posição (ou seja, velocidade) são constantes. Como o módulo do vetor direção depende da distância entre a nave e o mouse, a velocidade do projétil também é controlada por essa distância.

Gravidade: Para o cálculo da força gravitacional, primeiro encontramos a distância entre o projétil e o planeta em cada eixo. Em seguida, fazemos a normalização do vetor direção entre o projétil e o planeta usando a fórmula $\hat{d_x} = \frac{dx}{|d|}$ e $\hat{d_y} = \frac{dy}{|d|}$, onde |d| é igual à distancia entre os dois corpos (encontrada pelo teorema de pitágoras $\sqrt{d_x^2 + d_y^2}$), que, nesse caso, é o módulo do vetor direção. Para encontrar a magnitude da força, usamos a fórmula $F = \frac{G}{d^2}$, onde $G$ é uma constante (no nosso caso 6900) e $d$ é a distância entre os corpos (similar à da mecânica newtoniana ($F = \frac{Gm_1m_2}{d^2}$) mas sem incluir a massa dos objetos). Para a aceleração gerada pela gravidade no projétil, lembramos da Segunda Lei de Newton: $F = ma$; como a massa não é considerada no nosso sistema, a aceleração nada mais é do que a própria força gravitacional. Para achar as componentes da aceleração, multiplicamos o valor que encontramos para a aceleração pelo vetor direção normalizado (unitário) em cada eixo: $a_x = F_x = \frac{G}{d^2} \cdot \hat{d_x}$ e $a_y = F_y = \frac{G}{d^2} \cdot \hat{d_y}$. Nossa lógica funciona para mais de um planeta ao mesmo tempo pois rodamos um for que percorre todos os planetas do mapa e adicionamos a força exercida pelo planeta à aceleração, portanto, a aceleração que é adicionada à velocidade atual do projétil (o que só ocorre após o for termina, pois o for percorre todos os planetas a cada frame) é a soma vetorial de todas das forças gravitacionais exercidas pelos planetas (lembrando que aqui força é igual a aceleração), o que obedece o principio da superposição de forças.

Colisões: Para detectar colisões com os planetas, usamos a fórmula da distância entre dois pontos no plano cartesiano: d = $\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$. Se a distância entre o projétil e o planeta for menor que a soma dos raios dos dois corpos (assumindo que ambos são círculos), significa que houve uma colisão.

<img src="./src/gif/Gameplay.gif">