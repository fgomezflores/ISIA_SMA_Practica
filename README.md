# Propuesta de trabajo práctico para el desarrollo de un sistema multiagente para la simulación del tráfico aéreo
## 1. Introducción
Esta propuesta se enmarca como trabajo práctico de la asignatura “Sistemas Multiagente” del Máster Universitario en Ingeniería del Software e Inteligencia Artificial de la Universidad de Málaga, en su convocatoria de septiembre. A continuación, se expone, entre otros asuntos el objetivo, plazo de realización, las características generales del sistema y la bibliografía que se utilizará en su realización. 

## 2. Objetivos 

El principal objetivo de este trabajo es el desarrollo de un modelo, a través de un sistema multiagente (SMA), que permita simular el comportamiento del tráfico de aéreo de pasajeros de vuelos comerciales bajo diferentes escenarios.

Adicionalmente, el trabajo tiene como objetivo complementario la aplicación práctica de los conocimientos teóricos adquiridos en la asignatura y la utilización de herramientas específicas para la implantación de sistemas multiagente. 

## 3. Plazo de realización y equipo de trabajo 

El plazo para la realización del modelo es hasta el 15 de septiembre de 2023. El trabajo se realizará de forma individual. 

## 4. Entregable 

El entregable de la presente propuesta será el código fuente de la aplicación y un breve resumen (alrededor de una página) explicando su funcionamiento, agentes que lo componen, etc. Además, este se presentará al equipo docente de forma práctica. 

## 5. Descripción de las características generales del sistema 

### 5.1 Entorno tecnológico y recursos software 

Respecto a la tecnología que se empleará para la implementación de este sistema se opta por el marco de modelado **Mesa** (v.2.1.1) para lenguaje **Python** (v.3.11). En los últimos años el citado lenguaje de programación ha adquirido gran popularidad [1] para modelos basados en agentes debido a su facilidad de uso, flexibilidad y amplio ecosistema de bibliotecas. Una de esas bibliotecas es Mesa, que  ofrece un amplio conjunto de herramientas y características para crear, simular y analizar SMA, lo que lo convierte en un recurso valioso para investigadores y profesionales interesados en modelar sistemas complejos.

![image](https://github.com/fgomezflores/ISIA_SMA_Practica/assets/122975434/f7db729b-4e12-4651-80a4-262f55103969)

Como IDE de programación se utiliza **PyCharm** 2023.1.2 (Community Edition).

El código está disponible en **GitHub** a través de la dirección [****](https://github.com/fgomezflores/ISIA_SMA_Practica). En esta plataforma se aloja el proyecto y se centralizan los cambios realizados.

Por último, respecto a los **recursos hardware**, el equipo en el que se ejecuta dicha herramienta es un ordenador portátil AMD FX-7600P Radeon R7, 12 Compute Cores 4C+8G 2.70 GHz con plataforma Windows 10 Home versión 21H2. 

### 5.2 Estructura del modelo 

El modelo se basa en sistema de coordenadas cartesianas, donde se ubicarán los agentes que se indican a continuación.


### 5.3 Tipología de agentes 

Se contemplan dos tipos de agentes: 

1) Aeropuertos, son el origen y destino de cada vuelo. 

2) Aviones, cada avión cubrirá siempre la misma ruta entre los aeropuertos de salida y llegada. Así, una vez que el avión llegue a su destino, transcurrido un determinado tiempo, realizará la ruta de vuelta y así sucesivamente durante toda la simulación 

![image](https://github.com/fgomezflores/ISIA_SMA_Practica/assets/122975434/03e3b023-da35-41b2-a702-7c605b1a9bb8)

### 5.4 Comportamiento básico de los agentes 

Vehículo. Se puede definir el comportamiento de un vehículo con el siguiente diagrama de estados: 

[DIAGRAMA]

Leyenda: 

tsem	=	tiempo de espera del semáforo. 

tdesp	=	tiempo de espera cuando se llega a casilla sin origen. 

tret	=	tiempo de espera cuando hay retención. 

 

Semáforo: 

[DIAGRAMA]
 
Leyenda: 

tsem	=	tiempo de espera del semáforo (en rojo). 

tver	=	tiempo donde el semáforo está en verde. 

 

### 5.5 Interacciones entre agentes 

Un SMA resulta de la ejecución concurrente de los comportamientos de los agentes que lo componen. Para el presente trabajo se distinguen varios modelos de interacciones: 

Interacciones entre vehículos donde se aplican tres modelos: 

Un modelo de seguimiento de automóviles (que describe las reacciones del vehículo entre otros vehículos). 

Un modelo que describe las reglas a seguir en las intersecciones. 

Interacciones entre vehículos y semáforos. 

Interacciones entre vehículos y zonas no transitables. Si un vehículo llega a una zona donde ya no puede avanzar, esperará 3 segundos y desaparecerá del grid. 

Interacción entre observadores de estado de simulación y agentes de simulación. Esto es necesario para obtener las medidas de rendimiento del sistema simulado, y que se requieren como resultado del trabajo. 

### 5.6 Diagrama 

Se propone el siguiente diagrama de flujo para la simulación del sistema, tomado de [7]:  

[DIAGRAMA]

Leyenda: 

#V	=	número de vehículos. 

Gs	=	tamaño de la cuadrícula o grid. 

tesp	=	tiempo de espera (segundos) del vehículo. 

tsem	=	tiempo de espera del semáforo. 

tret	=	tiempo de espera cuando el vehículo tiene otro delante parado. 

tdesp	=	tiempo de espera cuando se llega a casilla sin salida. 

t	=	tiempo instantáneo de la simulación. 

tsim	=	tiempo total de la simulación 

totalesp	=	suma total del número de segundos de espera de cada vehículo 

### 5.7. Estructura del programa en Python


![image](https://github.com/fgomezflores/ISIA_SMA_Practica/assets/122975434/af04e24e-0021-482c-9f8f-f34e7aa74a9a)

![image](https://github.com/fgomezflores/ISIA_SMA_Practica/assets/122975434/87b0c8a0-73bd-4e7e-b22c-3455271571fe)


## 6. Resultados  

El resultado del sistema que se debe obtener será, para cada simulación, la suma total del número de segundos de espera de cada vehículo durante la simulación. Es decir, el debido a otros coches y el debido a los semáforos.  

No se tendrá en cuenta el tiempo de espera cuando llega a una casilla sin salida porque se entiende que aparca. 

**Recursos** 

Para la elaboración de este trabajo se utilizará, además de los medios tecnológicos indicados, el catálogo Jábega de la Biblioteca de la Universidad de Málaga, para la obtención de información y documentación sobre proyectos similares, y búsquedas puntuales en Internet, preferentemente mediante Google Scholar.  

## 7. Referencias 

Se relaciona bibliografía que se usará para el desarrollo de este trabajo: 

Abar, S., Theodoropoulos, G. K., Lemarinier, P., & O’Hare, G. M. (2017). Agent Based Modelling and Simulation tools: A review of the state-of-art software. Computer Science Review, 24, 13-33. 

Kazil, J., Masad, D., & Crooks, A. (2020). Utilizing python for agent-based modeling: The mesa framework. In Social, Cultural, and Behavioral Modeling: 13th International Conference, SBP-BRiMS 2020, Washington, DC, USA, October 18–21, 2020, Proceedings 13 (pp. 308-317). Springer International Publishing.

Masad, D., & Kazil, J. (2015, July). MESA: an agent-based modeling framework. In 14th PYTHON in Science Conference (Vol. 2015, pp. 53-60).

Wai Foong, Ng (Nov 1, 2019). Introduction to Mesa: Agent-based Modeling in Python. Towards Data Science. [
](https://towardsdatascience.com/introduction-to-mesa-agent-based-modeling-in-python-bcb0596e1c9a)https://towardsdatascience.com/introduction-to-mesa-agent-based-modeling-in-python-bcb0596e1c9a

Mesa: Agent-based modeling in Python 3+. https://mesa.readthedocs.io/en/stable/ ​

Github – Project Mesa. https://github.com/projectmesa/mesa 
