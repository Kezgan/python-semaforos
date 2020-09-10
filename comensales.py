import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

mutexCocinero = threading.Semaphore(0)
mutexComensal = threading.Semaphore(1)

cantidadPlatos = 3

class Cocinero(threading.Thread):
  def __init__(self):
    super().__init__()
    self.name = 'Cocinero'

  def run(self):
    global platosDisponibles
    while (True):
      mutexCocinero.acquire()
      try:
        logging.info('Reponiendo los platos...')
        platosDisponibles = cantidadPlatos
      finally:
        mutexComensal.release()

class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'

  def run(self):
    global platosDisponibles

    mutexComensal.acquire()
    try:
      while platosDisponibles == 0:
        mutexCocinero.release()
        mutexComensal.acquire()
      platosDisponibles -= 1
      logging.info(f'¡Qué rico! Quedan {platosDisponibles} platos')
    finally:
      mutexComensal.release()

platosDisponibles = cantidadPlatos

Cocinero().start()

for i in range(5):
  Comensal(i).start()

