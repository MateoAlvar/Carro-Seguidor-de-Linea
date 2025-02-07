# Carro-Seguidor-de-Linea

Proyecto desarrollado por Mateo Alvarado Malaver-20201005092 y Sebastian Aldana 20202005048.
malvaradom@udistrital.edu.co, saaldanal@udistrital.edu.co
Tutor: Gerardo A. Muñoz.
Facultad de Ingeniería, Universidad Distrital Francisco José de Caldas.

#Resumen
Este proyecto consiste en el diseño y construcción de un carro seguidor de línea, 
cuyo funcionamiento se basa en un microcontrolador Raspberry Pi Pico W. 
El carro detecta y sigue una línea negra en el suelo mediante una cámara OV7670,
procesando la imagen capturada para determinar la posición de la línea. 
La dirección del carro se ajusta mediante el control de dos motores,
gestionados a través de un módulo puente H. Este sistema de control
permite al carro seguir la línea de forma autónoma, mejorando su precisión y 
rendimiento al ajustar la velocidad y el giro en tiempo real.

#Materiales
Los materiales necesarios para la realización de este proyecto son:
-Cámara OV7670
-Puente H doble L298
-Raspberry Pi Pico W
-Batería
-Chasis para carro

#Conexiones
En la primera parte del código se definen los pines que van del puente H hacia la Raspberry
y por consiguiente se definen los pines de la cámara, estos pines se pueden acomodar a beneficio
de cada montaje. Además, se debe asegurar el voltaje de la Raspberry y sobretodo del puente H
puesto que sin el suficiente voltaje los motores no trabajaran óptimamente.

#Código
El lenguaje implementado fue Circuitphyton, se debe tener en cuenta a la hora de 
correr el código la implementación de las librerias necesarias, de lo contrario el 
código generará errores al no poder importar dichas librerías.
