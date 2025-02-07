import sys
import time
import pwmio
import digitalio
import busio
import board
#import adafruit_ssd1306
vel_ini_derecha=85;
vel_ini_izquierda=85;

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
pwm1 = pwmio.PWMOut(board.GP18,frequency=100000, duty_cycle=0)
pwm2 = pwmio.PWMOut(board.GP19,frequency=100000, duty_cycle=0)

pwm1.duty_cycle = 0
pwm2.duty_cycle = 0

pin_pmwDer =board.GP27
pin_pmwIzq=board.GP17
pin_ledblanco=board.GP22
# Configurar el pin como salida
motor_d = digitalio.DigitalInOut(pin_pmwDer)
motor_d.direction = digitalio.Direction.OUTPUT

# Establecer el pin en alto
motor_d.value = True

# Configurar el pin como salida
motor_i = digitalio.DigitalInOut(pin_pmwIzq)
motor_i.direction = digitalio.Direction.OUTPUT

# Establecer el pin en alto
motor_i.value = True

luz = digitalio.DigitalInOut(pin_ledblanco)
luz.direction = digitalio.Direction.OUTPUT
luz = True

# Establecer el pin en alto
motor_d.value = True


from adafruit_ov7670 import (  # pylint: disable=unused-import
    OV7670,
    OV7670_SIZE_DIV16,
    OV7670_COLOR_YUV,
    OV7670_TEST_PATTERN_COLOR_BAR_FADE,
)


cam_bus = busio.I2C(board.GP21, board.GP20)

cam = OV7670(
    cam_bus,
    data_pins=[
        board.GP0,
        board.GP1,
        board.GP2,
        board.GP3,
        board.GP4,
        board.GP5,
        board.GP6,
        board.GP7,
    ],
    clock=board.GP8,
    vsync=board.GP13,
    href=board.GP12,
    mclk=board.GP9,
    shutdown=board.GP15,
    reset=board.GP14,
)

cam.size = OV7670_SIZE_DIV16
cam.colorspace = OV7670_COLOR_YUV
cam.flip_y = True

#print(cam.width, cam.height)##40*30

# Dimensiones de la imagen
width = cam.width
height = cam.height

# Buffer para almacenar píxeles
pixels = bytearray(2 * width * height)

rect1 = 0
centro = 0
abajo = 0
curvDer=0
curvDerC=0

#BUCLE PRINCIPAL
while True:
    rect1 = 0
    centro = 0
    abajo = 0
    curvDer=0
    curvDerC=0

        
    # Capturar la imagen en el buffer
    cam.capture(pixels)
    # Lista para almacenar todas las filas
    all_rows = []

    # Procesar píxeles por fila
    for j in range(height):
        row_start = j * width * 2
        row_end = row_start + width * 2
        row_pixels = pixels[row_start:row_end]

        # Aquí puedes trabajar con los píxeles de la fila, por ejemplo, convertir a lista
        row_list = list(row_pixels)

        # Imprimir la lista de píxeles de la fila
        #print(row_list)
        
        
        # Agregar la lista de la fila a la lista de todas las filas
        all_rows.append(row_list)
        

    # Obtener la última lista de la lista de filas
    ultima_lista = all_rows[-1]
    central_lista = all_rows[-13]
    primera_lista = all_rows[-24]
    
    # Imprimir la última lista
    #print("Última lista:", ultima_lista)
    #print("Central lista:", central_lista)
    
    
    UltimaImpar= ultima_lista [::2] # Son los 40 datos Px Arriba de la CAM
    CentralImpar= central_lista [::2] # Son los 40 datos
    PrimeraImpar= primera_lista [::2] # Son los 40 datos Px ABAJO de la CAM
    PrimeraImpar1 = [1 if dato < 100 else 0 for dato in PrimeraImpar]
    CentralImpar1= [1 if dato < 100 else 0 for dato in CentralImpar]
    UltimaImpar1= [1 if dato < 100 else 0 for dato in UltimaImpar]
    #print("Arri lis:", UltimaImpar1)
    #print("Cent lis:", CentralImpar1)
    #print("Abajo:", PrimeraImpar1)
    
    centro=UltimaImpar1[18:22] #pequeño es negro 8 DATOS Px Arriba de la CAM
    #print("arriba:", centro)
    CenPro = sum(centro) / len(centro)
    #print("Promedio del centro:", CenPro)
    der = UltimaImpar1[13:18]
    DerProm = sum(der) / len(der)
    #print("Promedio del derecha:", DerProm)
    izq = UltimaImpar1[22:27]  # Tomar los últimos 5 datos
    #print("izquierda:", izq )
    IzqProm = sum(izq) / len(izq)
    #print("Promedio del izquierda:", IzqProm )
    
    
    
    
    centro2=CentralImpar1[11:29] #6datos
    #print("centro2:", centro2)
    CenPro2 = sum(centro2) / len(centro2)
    der2 = CentralImpar1[0:11]  # Tomar los últimos 15 datos
    DerProm2 = sum(der2) / len(der2)
    izq2 = CentralImpar1[29:39]
    IzqProm2 = sum(izq2) / len(izq2)
    
    
    centro3=PrimeraImpar1[13:25]#18datos PX ABAJO DE LA CAM
    print("abajo:", centro3)
    CenPro3 = sum(centro3) / len(centro3)
    der3 = PrimeraImpar1[0:12]  # Tomar los últimos 15 datos
    DerProm3 = sum(der3) / len(der3)
    izq3 = PrimeraImpar1[26:39]
    IzqProm3 = sum(izq3) / len(izq3)
    
    print("Izq:", IzqProm2, end="  ")
    print("Centro:", CenPro2, end="  ")
    print("Der:", DerProm2)
    
    if CenPro3<1 and DerProm3>0:#Px ABAJO de la CAM para siempre seguir la LINEA
        pwm1.duty_cycle = 20000#60000 #activa motor derecho para centrarse
        pwm2.duty_cycle =10000 #50000
        time.sleep(0.014)
#         pwm1.duty_cycle = 0
#         pwm2.duty_cycle =0
        print("Activa mot derecha")
        #pwmInf.duty_cycle= 0#imprimeLCD
    if CenPro3<1 and IzqProm3>0:
        pwm2.duty_cycle = 20000#65000 #activa motor izquierdo para centrarse
        pwm1.duty_cycle = 10000#50000
        time.sleep(0.014)
#         pwm1.duty_cycle = 0
#         pwm2.duty_cycle =0
        print("Activa mot izquierda")
        #pwmInf.duty_cycle= 35000#imprimeLCD
    if CenPro3>0.75 and (DerProm3<0.3 or IzqProm3<0.3):
        abajo=1
        pwm1.duty_cycle = 55500  # Ajusta el valor max2 vel2
        pwm2.duty_cycle = 55500  # Ajusta el valor max2 vel2
        time.sleep(0.0145)
#         pwm1.duty_cycle = 0
#         pwm2.duty_cycle =0
        print("Activa 2 mot")
        #pwmInf.duty_cycle= 65000#imprimeLCD
 
    if CenPro2<1 and DerProm2>0:#Px CENTRO de la CAM 
        print("CENTRO a la derecha")
        pwm1.duty_cycle = 65500#20000 #activa motor derecho para centrarse
        pwm2.duty_cycle =50000 #10000
        time.sleep(0.0066)
#         pwm1.duty_cycle = 0
#         pwm2.duty_cycle =0
    if CenPro2<1 and IzqProm2>0:
        print("CENTRO a la izquierda")
        curvDerC=1
        pwm2.duty_cycle = 65500#20000 #activa motor izquierdo para centrarse
        pwm1.duty_cycle = 50000#10000
        time.sleep(0.0066)
#         pwm1.duty_cycle = 0
#         pwm2.duty_cycle =0
    if CenPro2>0.8 and (DerProm2<0.3 or IzqProm2<0.3):
        print("CENTRO Centrado")
        centro=1
        pwm1.duty_cycle = 65000  # Ajusta el valor max2 vel2
        pwm2.duty_cycle = 65000  # Ajusta el valor max2 vel2
        time.sleep(0.006)
#         pwm1.duty_cycle = 0
#         pwm2.duty_cycle =0
      
    #identificar RECTA para MAXIMA VELOCIDAD
    #cuando arriba se desvia a la izquierda es curva a la derecha
    
    if centro==1 and abajo==1: ##mueve los 2 motores al tiempo
        print("Recta Max Vel")
        pwm1.duty_cycle = 63000  # Ajusta el valor max2 vel2
        pwm2.duty_cycle = 63000  # Ajusta el valor max2 vel2
        time.sleep(0.005)
#         pwm1.duty_cycle = 0
#         pwm2.duty_cycle =0
        if rect1==1:
            print("Recta Max Vel2")
            pwm1.duty_cycle = 65000  # Ajusta el valor max vel
            pwm2.duty_cycle = 65000  # Ajusta el valor max vel
            time.sleep(0.0065)
#             pwm1.duty_cycle = 0
#             pwm2.duty_cycle =0
        

    if CenPro>100 and DerProm<110: #Px Arriba de la CAM       
        print("Arriba a la derecha")
        pwm1.duty_cycle = 63000#20000 #activa motor derecho para centrarse
        pwm2.duty_cycle =53000 #10000
        time.sleep(0.006)
#         pwm1.duty_cycle = 0
#         pwm2.duty_cycle =0
    if CenPro>100 and IzqProm<110:
        print("Arriba a la Izquierda")
        curvDer=1
        pwm2.duty_cycle = 63000#20000 #activa motor izquierdo para centrarse
        pwm1.duty_cycle = 53000#10000
        time.sleep(0.006)
#         pwm1.duty_cycle = 0
#         pwm2.duty_cycle =0
    if CenPro<100 and DerProm>110 and IzqProm>110:
        print("Arriba Centrado")
        rect1=1  
        
    if curvDer==1 and centro==1 and abajo==1:#solo identifica MOSTRAR EN PANTALLA
        print("--Aprox curva a la der--")
        ##mostrar_mensaje("Aprox curva der")
        
    if curvDerC==1 and abajo==1:
        print("--Tomando curva a la der--")#solo identifica MOSTRAR EN PANTALLA
        
 
######### AGENTE Q LEARNING
#  # Obtener la nueva recompensa y el próximo estado
#     reward = +1  
#     new_state = agent.get_state(pixels)
#     
#     # Actualizar el agente Q-learning
#     agent.update(state, action, reward, new_state)
# 
# 
# 
# ##################################################
#     # Verificar si el botón está presionado para entrenar el perceptrón
#     if not button.value:
#         train_perceptron()
#         print ("pwm calculado",pwm_value)
    
    time.sleep(0.066)  # Esperar antes de la próxima captura desactivar cuando se termine
    pwm1.duty_cycle = 1000
    pwm2.duty_cycle = 1000
