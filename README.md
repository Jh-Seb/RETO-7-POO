# RETO-7-POO
# Sistema de Gestión de Restaurante en Python

Este repositorio contiene un proyecto en Python que implementa un sistema de gestión de restaurante. El sistema incluye funcionalidades para gestionar múltiples órdenes, administrar el menú mediante persistencia en archivos JSON y agrupar ítems del menú utilizando *named tuples*.

## Características

- **Gestión de órdenes**: 
  - Uso de una cola FIFO (con `deque`) para administrar y procesar las órdenes en el orden de llegada.
  
- **Gestión del menú**:
  - Creación, adición, actualización y eliminación de ítems en el menú.
  - Persistencia del menú en archivos JSON para mantener la información.
  
- **Estructura modular**:
  - Clases para representar distintos tipos de ítems del menú (*Beverage*, *Appetizer*, *MainCourse*).
  - Clase `Order` que agrega la funcionalidad de gestionar platos y calcular totales.
  - Clase `Payment` para simular el procesamiento de pagos.
  - Clase `Restaurant` para manejar múltiples órdenes.
  
- **Uso de Named Tuples**:
  - Se define un `MenuSet` para agrupar conjuntos de ítems del menú de manera inmutable.

## Estructura del Proyecto

El proyecto se organiza en las siguientes clases:

- **MenuItem**: Clase base para los ítems del menú, con propiedades para nombre y precio.
- **Beverage, Appetizer, MainCourse**: Clases derivadas de `MenuItem` que añaden atributos específicos de cada tipo de plato.
- **Order**: Maneja la lista de platos agregados a la orden y ofrece métodos para gestionar el menú (crear, agregar, actualizar y eliminar ítems) con persistencia en JSON.
- **Payment**: Simula el proceso de pago de una orden.
- **Restaurant**: Utiliza una cola FIFO para gestionar y procesar múltiples órdenes.

## Requisitos

- Python 3.6 o superior.
- No se requieren librerías externas, ya que se utilizan módulos estándar como `json`, `collections` y `namedtuple`.

## Cómo Ejecutar el Proyecto

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
