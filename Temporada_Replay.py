from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
import json

hub = PrimeHub()

# Define as portas dos motores e variaveis globais
# Motores Grandes
motor_esquerdo = Motor("F")
motor_direito = Motor("B")
motores = MotorPair("B", "F")

# Motores médios
motor_garra_esquerdo = Motor("A")
motor_garra_direito = Motor("D")

# Sensores
sensor_cor_esquerdo = ColorSensor("E")
sensor_cor_direito = ColorSensor("C")

# Reseta a leitura dos motores e sensores
motor_esquerdo.set_degrees_counted(0)
motor_direito.set_degrees_counted(0)
hub.motion_sensor.reset_yaw_angle()

# Desliga os sensores que não estão sendo utilizados
sensor_cor_esquerdo.light_up_all(0)
sensor_cor_direito.light_up_all(0)

# Funções para movimentação do robô
def curva(angulo, velocidade):
    ''' Este bloco esta destinado a realizar curvas com osensor girosópio ecom desaceleração no final da curva melhorar a
    precisão
    '''

    # Reseta o sensor de rotação dos motores e sensores
    motor_esquerdo.set_degrees_counted(0)
    motor_direito.set_degrees_counted(0)
    hub.motion_sensor.reset_yaw_angle()

    angle = (angulo / 4) * 3 # Define a curva primaria

    # Fator de coreção do robô
    if angulo >= 0:
        angulo = angulo - 2.45

    else:
        angulo = angulo + 2.45

# Inicia o loop e encerra quando a varriavel loop for False

    loop = True
    while loop:
        # Realiza a curva para a direita
        if angulo >= 0:
            if hub.motion_sensor.get_yaw_angle() <= angle:
                motor_esquerdo.start(velocidade * -1)

            else:
                if hub.motion_sensor.get_yaw_angle() <= angulo:
                    motor_esquerdo.start(-10)

                else:
                    motores.stop()
                    loop = False

        # Realiza a curva para esquerda
        else:
            if hub.motion_sensor.get_yaw_angle() >= angle:
                motor_direito.start(velocidade)

            else:
                if hub.motion_sensor.get_yaw_angle() >= angulo:
                    motor_direito.start(10)

                else:
                    motores.stop()
                    loop = False

def mover(distancia, velocidade):
    ''' Este bloco esta destinado a realizar o movimento do robô com correção do backlash utilizando o sensor de movimento e
    se move utilizando a transformação em centimetros
    '''
    # Reseta a leitura dos motores e sensores
    motor_esquerdo.set_degrees_counted(0)
    motor_direito.set_degrees_counted(0)
    hub.motion_sensor.reset_yaw_angle()

    # Converções necessarias para o bom funcionamento do código
    graus = (distancia/(6.1 * 3.14159265) * 360)
    velocidade = velocidade * -1
    loop = True

    while loop:
        if velocidade <= 0:
            if motor_direito.get_degrees_counted() <= graus:
                # Correção do backlash com o sensor de movimento
                backlash = hub.motion_sensor.get_yaw_angle() + 0

                motores.start(backlash, velocidade) # Liga os motores para frente

            else:
                '''Para os motores e espera 20 milésimos de segundos com o motor desligado para garantir que o robô esteja
                parado ao final do ciclo, e fecha o loop
                '''
                motores.stop()
                wait_for_seconds(0.2)
                loop = False # Variavel responsavel por fechar o loop

        else:
            if motor_esquerdo.get_degrees_counted() <= graus:
                # Correção do backlash
                backlash = 0 - hub.motion_sensor.get_yaw_angle()

                motores.start(backlash, velocidade) # Liga os motores para trás

            else:
                '''Para os motores e espera 20 milésimos de segundos com o motor desligado para garantir que o robô esteja
                parado ao final do ciclo, e fecha o loop
                '''
                motores.stop()
                wait_for_seconds(0.2)
                loop = False # Variavel responsavel por fechar o loop

# Funções correspondentes a cada saida do robô
def primeira_saida():
    ''' A primeira saida se desloca para a missão do banco em linha reta
    e volta a base
    '''
    # Mover até a missão
    mover(37, 40)
    mover(7, 10)

    # Volta a area de inspeção
    wait_for_seconds(0.25)
    mover(37, -100)

def segunda_saida():
    ''' A segunda saida realiza a missão do escorregador e volta a
    area de inspeção
    '''
    # Mover até a missão
    mover(60, 50)
    wait_for_seconds(0.2)

    # Volta a area de inspeção
    mover(15, -10)
    mover(66, -100)

def terceira_saida():
    ''' Esta saida realiza a missão compartilhada e do basquetebol
    e volta a base
    '''
    # Reseta os motores
    motor_garra_esquerdo.set_degrees_counted(0)
    motor_garra_direito.set_degrees_counted(0)

    # Mover até a missão do basketeball
    curva(20, 20)
    mover(75, 50)
    curva(-66, 40)
    mover(11.3, 20)
    wait_for_seconds(0.5)
    motor_garra_esquerdo.run_for_degrees(2850, -100)

    # Mover até a missão compartilhada
    mover(15, -50)
    curva(34, 40)
    mover(7, 10)

    # Volta a area de inspeção
    mover(30, -50)
    curva(30, 40)
    mover(105, -100)

def quarta_saida():
    ''' Esta saida realiza a missão do contador de passos e da
    esteira
    '''
    mover(110.5, 50)
    wait_for_seconds(0.2)

    mover(20, -40)
    curva(-92.7, 40)
    mover(19, -50)
    mover(10, -100)
    wait_for_seconds(0.5)

    mover(15.35, 40)
    curva(-90.4, 20)
    mover(97.5, -50)
    wait_for_seconds(0.5)

    motor_esquerdo.set_degrees_counted(0)
    motor_esquerdo.run_for_degrees(1800)
    mover(20, 50)
    curva(-6, 30)
    mover(170, 100)

def quinta_saida():
    ''' Realiza a missão da bocha e depois permanece até o final
    do round na missão da dança
    '''
    mover(15, 20)
    curva(88.5, 50)
    mover(61, 50)

    curva(-90, 50)
    mover(50, 50)
    curva(-10, 20)
    mover(5, 30)

    mover(16, -30)
    curva(-30, 30)
    mover(25, 50)

    loop = True
    while loop:
        mover(10, 30)
        mover(10, -30)

# Maquina de estado
def maquina_estado():
    contador = 1

    motor_esquerdo.set_degrees_counted(0)
    motor_direito.set_degrees_counted(0)

    loop = True
    while loop:

        # Controle
        if hub.left_button.was_pressed():
            contador = contador - 1
        
        if hub.right_button.was_pressed():
            contador = contador + 1
        
        # Organiza as saidas
        if contador == 1:
            primeira_saida()
        
        elif contador == 2:
            segunda_saida()

        elif contador == 3:
            terceira_saida()

        elif contador == 4:
            quarta_saida()

        elif contador == 5:
            quinta_saida()
            loop = False

hub.close()