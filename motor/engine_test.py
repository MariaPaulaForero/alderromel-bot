import RPi.GPIO as GPIO
from time import sleep
#import keyboard

# TODO: Dividir en funciones para avanzar,
# retroceder, girar y detenerse
# TODO: Regular velocidad
# TODO: Funcion de hacer trompito
# TODO: Escuchar desde las peticiones de un socket
# con los movimientos que ejecutaran las funciones
# Puede ser via memoria compartida, sockets etc [Sockets de preferencia]

# Include the motor control pins
# Motor A LADO IZQUIERDO
ENA = 17
IN1 = 27
IN2 = 22
# Motor B LADO DERECHO
ENB = 11
IN3 = 10
IN4 = 9

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Disable warnings
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Configuración del PWM para cada motor
pwm_A = GPIO.PWM(ENA, 100)  # Frecuencia de 100 Hz para el motor A
pwm_B = GPIO.PWM(ENB, 100)  # Frecuencia de 100 Hz para el motor B
pwm_A.start(0)  # Iniciar el PWM del motor A con velocidad 0%
pwm_B.start(0)  # Iniciar el PWM del motor B con velocidad 0%

speed_A = 100
speed_B = 100

pwm_A.ChangeDutyCycle(speed_A)
pwm_B.ChangeDutyCycle(speed_B)

def forward():
    """Set motors to move forward."""
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def backward():
    """Set motors to move backward."""
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def stop():
    """Stop the motors."""
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    
def turn_left():
	GPIO.output(IN1, GPIO.LOW)
	GPIO.output(IN2, GPIO.HIGH)
	GPIO.output(IN3, GPIO.HIGH)
	GPIO.output(IN4, GPIO.LOW)

def turn_right():
	GPIO.output(IN1, GPIO.HIGH)
	GPIO.output(IN2, GPIO.LOW)
	GPIO.output(IN3, GPIO.HIGH)
	GPIO.output(IN4, GPIO.LOW)

print("FIUMMMMMMMMMMMMMMMMMMBA")

if __name__ == "__main__":
    try:
        #print("Usa las flechas del teclado para controlar el robot. Presiona 'q' para salir.")
        while True:
            '''if keyboard.is_pressed('up'):
                forward(50, 50)
            elif keyboard.is_pressed('down'):
                backward(50, 50)
            elif keyboard.is_pressed('left'):
                turn_left(50, 50)
            elif keyboard.is_pressed('right'):
                turn_right(50, 50)
            elif keyboard.is_pressed('q'):
                break
            else:
                stop()
            sleep(0.1)  # Pequeña pausa para evitar sobrecargar la CPU'''
            forward(100, 100)


    except KeyboardInterrupt:
        pass  # Allow exit with Ctrl+C
    finally:
        GPIO.cleanup()  # Clean up GPIO settings
