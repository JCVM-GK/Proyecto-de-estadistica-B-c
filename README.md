# 🃏 High or Low - Statistical Simulator v1.2

Este proyecto es un simulador interactivo del juego de cartas "Mayor o Menor", diseñado para demostrar conceptos de **Probabilidad Condicional** y **Frecuencia Observada** mediante el uso de un mazo finito de 52 cartas.

## 🎯 Objetivo del Proyecto
El objetivo es proporcionar una herramienta visual donde el usuario pueda tomar decisiones informadas basadas en el cálculo en tiempo real de las probabilidades de éxito, en lugar de depender únicamente del azar.

## 📊 Fundamentos Estadísticos Aplicados

### 1. Probabilidad Condicional (Mazo Finito)
A diferencia de un juego con reemplazo, este simulador utiliza un mazo de 52 cartas real. Cada carta extraída se elimina del espacio muestral ($n$), afectando directamente las probabilidades del siguiente evento.

La probabilidad de que la siguiente carta ($C_{next}$) sea mayor que la actual ($C_{curr}$) se calcula como:

$$P(Higher) = \frac{\text{Cartas restantes con valor } > C_{curr}}{\text{Total de cartas restantes en el mazo}}$$

### 2. Sistema de Score Ponderado por Riesgo
Para incentivar el análisis estadístico, el puntaje no es lineal. Se otorga una recompensa mayor por aciertos en eventos de baja probabilidad:
- **Acierto en evento de alta probabilidad (P > 70%):** +1 punto.
- **Acierto en evento de baja probabilidad (P < 20%):** Hasta +9 puntos.



## 🏗️ Arquitectura del Software
El proyecto implementa el patrón de diseño **MVC (Modelo-Vista-Controlador)** para garantizar la separación de la lógica matemática y la interfaz de usuario:

- **Modelo (`GameEngine`):** Gestiona el mazo, calcula las probabilidades y procesa las reglas del juego.
- **Vista/Controlador (`GameView`):** Renderiza la interfaz gráfica en Tkinter y captura los eventos del usuario.



## 🚀 Características Principales
- **Historial Dinámico:** Registro visual con indicadores de acierto (✓) o error (✗).
- **Indicador de Mazo:** Contador en tiempo real de cartas restantes ($n/52$).
- **Manejo de Empates:** Los empates se tratan como eventos neutrales que mantienen la racha.
- **Interfaz "Casino Style":** Diseño optimizado para legibilidad con símbolos de palos (♠♥♦♣).


## 🛠️ Tecnologías
- **Lenguaje:** Python 3.14
- **Interfaz:** Tkinter (Standard Library)
- **Arquitectura:** Model-View-Controller (MVC)

