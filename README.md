# Propuesta de trabajo práctico para el desarrollo de un sistema multiagente para la simulación de XXXXX

## 1. Introducción
Esta propuesta se enmarca como trabajo práctico de la asignatura “Sistemas Multiagente” del Máster Universitario en Ingeniería del Software e Inteligencia Artificial de la Universidad de Málaga, en su convocatoria de septiembre. A continuación, se expone, entre otros asuntos el objetivo, plazo de realización, las características generales del sistema y la bibliografía que se utilizará en su realización. 

## 2. Objetivos 

El principal objetivo de este trabajo es el desarrollo de un modelo, a través de un sistema multiagente (SMA), que permita simular el comportamiento del tráfico de vehículos en un entorno urbano bajo diferentes escenarios. 

Adicionalmente, el trabajo tiene como objetivo complementario la aplicación práctica de los conocimientos teóricos adquiridos en la asignatura y la utilización de herramientas específicas para la implantación de sistemas multiagente. 

## 3. Plazo de realización y equipo de trabajo 

El plazo para la realización del modelo es hasta el XX de septiembre de 2023. El trabajo se realizará de forma individual. 

## 4. Entregable 

El entregable de la presente propuesta será el código de implementación del sistema multiagente para la simulación del tráfico urbano. Además, este se presentará al equipo docente de forma práctica. 

## 5. Descripción de las características generales del sistema 

### 5.1 Entorno tecnológico y recursos software 

Respecto a la tecnología que se empleará para la implementación de este sistema se opta por Netlogo ya que presenta una curva de aprendizaje rápido y mantiene un equilibrio entre el esfuerzo requerido para el desarrollo del modelo y su nivel de escalabilidad [1] que permita cumplir los objetivos en los plazos establecidos. 

Respecto a los recursos software y hardware, el equipo en el que se ejecuta dicha herramienta es un ordenador portátil AMD FX-7600P Radeon R7, 12 Compute Cores 4C+8G 2.70 GHz con plataforma Windows 10 Home versión 21H2. 

### 5.2 Estructura del modelo 

El modelo se basa en una matriz compuesta por celdas de dimensión n filas por m columnas. Cada celda será transitable (o no), y en caso de serlo, tendrá una única dirección que facilitará la movilidad. 

### 5.3 Tipología de agentes 

Se contemplan dos tipos de agentes: 

Vehículos, responsable de la creación e identificación de los coches que se desplazan por la cuadrícula. 

Semáforos, responsable de los semáforos, donde, según su comportamiento binario permitirán el movimiento en una de las dos direcciones. 

 

Interfaz de usuario gráfica, Texto, Aplicación, Chat o mensaje de texto

Descripción generada automáticamente 

### 5.4 Comportamiento básico de los agentes 

Vehículo. Se puede definir el comportamiento de un vehículo con el siguiente diagrama de estados: 

![image](https://github.com/fgomezflores/ISIA_SMA_Practica/assets/122975434/03e3b023-da35-41b2-a702-7c605b1a9bb8)

