# Práctica 1: Web scraping

## Contexto
Esta práctica se realiza bajo el contexto de la asignatura _Tipología y ciclo de vida de los datos_, perteneciente al Máster de Ciencia de Datos de la UOC.

## Descripción
El propósito de esta práctica consiste en desarrollar un script en Python que, mediante el uso de técnicas de web scraping, sea capaz de "scrapear" la web https://huggingface.co/models y genere un dataset en formato CSV que contenga los modelos de ML publicados en Hugging Face, así como información asociada a los mismos (autor, tipo de modelo, likes, descargas, etc).

_Hugging Face_ es una plataforma open source que permite publicar modelos de ML a cualquier persona u organización y este dataset  permitirá a otros desarrolladores crear diferentes tipos de análisis sobre el estado del arte de la tecnología actual.

## Miembros del equipo
La práctica ha sido desarrollada de forma conjunta por:
* Marcos Gómez Vázquez
* Mario Bru Barrero

## Ficheros del código fuente
* **source/script.py**:  orquesta y ejecuta el programa, permitiendo al usuario interactuar con él personalizando diferentes parámetros según la necesidad del mismo.
* **source/scraper.py**: aquí se definen las funciones que utiliza `script.py` para realizar las tareas de web scraping.
* **dataset**: contiene el dataset `huggingface_models_dataset.csv` generado mediante el uso del script.
* **requirements.txt**: aquí se especifican las liberías y versiones utilizadas en el desarrollo de la práctica.

## Instrucciones de uso

