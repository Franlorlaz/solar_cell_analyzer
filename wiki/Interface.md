# Descripción de la interfaz

La descripción que se propone a continuación corresponde a la primera versión
del programa, es decir, sin tener en cuenta las nuevas funcionalidades que
se pretenden añadir en un futuro.

## Funcionalidad principal
> **_NOTA:_**
> Un archivo `.json` contiene una *lista* o un *diccionario* cuyos elementos pueden ser
> también *listas* o *diccionarios*. Se parece mucho a las estructuras de python. 
> Cuando digo "se tiene que generar un archivo `.json`" puedes interpretarlo como
> "se tiene que generar un *diccionario*", ya que el paso de tener un *diccionario*
> en python a escribirlo en un archivo `.json` es prácticamente directo.

Propongo que la funcionalidad del botón de **comenzar** sea la de leer el estado de
todos los widgets y todas las variables de la interfaz agrupando todos estos datos
en un diccionario (que en un futuro se podría guardar en un archivo `interface.json`
para poder guardar distintas configuraciones, de esto no te preocupes por ahora)
con toda la configuración, a excepción de la configuración del modo, que irá en un
archivo `mode.json` (por lo que la funcionalidad del botón de **guardar**,
en la ventana de la configuración del modo, debe ser la de generar el archivo).
Tras la generación del diccionario de configuración principal, el botón **comenzar** 
generará la secuencia de medida y llevará a la aplicación a la ventana de medida
donde se irán mostrando los resultados a medida que se vayan obteniendo. La medida
en si se realiza llamando a una funcion `run()` que me encargo yo de definir.
La interfaz se diseñará en función del diccionario de configuración, con widgets 
que permitan al usuario introducir la información requerida en él. Este diccionario
lo puedes ver en la sección de **Archivos `.json` generados**.

Durante la medida, la pantalla cambiará a otra donde se muestren los resultados de
cada medida en tiempo real, de manera que vaya actualizándose cada vez que se termina
de medir un electrodo. En esta ventana solo habrá un botón `stop` para impedir que se
siga midiendo y el mismo botón pasará a `volver` una vez finalizadas todas las medidas
para volver a la ventana principal.


## Archivos `.json` generados

Un ejemplo del contenido del archivo `mode.json` se muestra a continuación:
```json
{
  "mode": "Lineal",
  
  "config": {
    "v_start": 1.2,
    "v_stop": -0.1,
    "points": 200,
    "speed": 0.240,
    "delay": 0.001,
    "cmpl": 0.05,
    "light_power": 1.0,
    "area": 0.14,
  }
}
```

El diccionario de configuración principal, que recoge toda la información que introduce
el usuario a través de los widgets se muestra a continuación en formato `.json` (en un
futuro este podría ser el contenido de un archivo `interface.json`):
```json
{
  "saving_directory": "directory/to/save/output",
  
  "mode": {
    "name": "Lineal",
    "config": "path/to/file/mode.json"
  },
  
  "repeat": {
    "type": "electrode",
    "times": 3,
    "wait": 5.0
  },
  
  "cells": {
    "cell_1": {
      "name": "Fancy perovskite",
      "electrodes": ["A", "B", "C", "D"]
    },
    "cell_2": {
      "name": "Normal perovskite",
      "electrodes": ["A", "C"]
    },
    "cell_3": {
      "name": "Default name",
      "electrodes": ["C", "D"]
    },
    "cell_4": {
      "name": "Default name",
      "electrodes": []
    }
  }
}
```


## Descripción de los widgets

Basándome en el diccionario que debe generarse al pulsar **comenzar**, se reconocen
cuatro secciones:

1. **Directorio de guardado (`saving_directory`):**
   Este widget yo lo tenía como un explorador de archivos donde el usuario podía
   seleccionar la carpeta donde quería que se guardasen los archivos de datos
   generados tras las medidas.
   

2. **Selección y configuración del modo (`mode`):**
   Este widget es el desplegable para seleccionar el modo (lineal, histeresis, etc).
   Junto al desplegable hay un botón que abre una ventana para establecer la configuración
   del modo. Esta ventana va a ser distinta dependiendo de la opción seleccionada 
   en el desplegable. Dentro de la ventana de configuración habrá los correspondientes
   widgets para meter números con sus etiquetas y tal para que el usuario introduzca 
   los parámetros que quiera. Habrá un botón de cancelar, para volver a la ventana 
   principal, y un botón de guardar, para guardar la configuración en un archivo 
   `.json`. Al darle a guardar se debe comprobar que todos los campos tengan un 
   valor correcto y si no lo tienen, que no deje guardar y salga un aviso de error 
   o bien que haya un valor por defecto y que se avise al usuario de que se ha 
   seleccionado el parámetro tal con el valor por defecto tal. Aquí en un futuro 
   (no para ahora) estaría guay que se pudiese cargar la configuración de otro 
   archivo, para no tener que reescribir los mismos parámetros cada vez que se 
   quiere medir.
   

3. **Sistema de repetición (`repeat`):**
   Está compuesto por una parte de un pack de tres *radio buttons* con los que se
   selecciona el tipo de repetición. Según la opción seleccionada, el campo `"type"`
   de `"repeat"` en el `.json` tendrá uno de los siguientes valores posibles: 
   `""`, `"electrode"`, `"all"`. Además de los radio buttons, habrá dos campos para 
   insertar numeros, uno para indicar el número de repeticiones (un número entero 
   positivo) y otro para el tiempo de espera (un número tipo float).
   El número de repeticiones se corresponde con el campo `"times"` del `.json` y
   el tiempo de espera se corresponde con el campo `"wait"`. Estos datos se deben 
   comprobar cuando se pulse **comenzar**, emitiendo un error al usuario si hay algún
   problema o estableciendo algún valor por defecto.
   

4. **Celdas y electrodos a medir (`cells`):**
   Cada una de las 4 celdas llevará asociado un nombre y una lista con los electrodos
   que se quieren medir. Si no se introduce ningún nombre, se le debe asignar uno por
   defecto (por ejemplo `"no_name"` o algo así). Con un conjunto de 4 checkboxes por cada
   celda, el usuario seleccionará qué electrodo quiere medir y en base al estado
   de los checkboxes se generará una lista con los electrodos seleccionados. Si no
   se selecciona ningún electrodo, se generará una lista vacía. La lista generada 
   está asociada al campo `electrodes` del `.json`.


> **_NOTA:_**
> Esto es todo lo que te puedo decir sobre el funcionamiento de la interfaz.
> Los widgets que te he comentado son una sugerencia, si ves que hay algo que puedes
> hacer de forma más óptima o que te resulta más cómoda, tienes total libertad 
> para implementar lo que sea. En principio, dudas como qué valores por defecto poner y tal
> por ahora pon el que te de la gana y ya en un futuro vemos qué valor es mejor en cada
> cosa.
> 
> Organiza el directorio de `interface` como quieras, crea las funciones, métodos, clases,
> etc, que te sean más útiles. Lo único imprescindible es que el botón de **comenzar**
> y **guardar** generen los diccionarios con los datos que necesito y que se
> dispare la función `run()` que crearé con la ejecución de las medidas y tal.
> 
> A la hora de construir la interfaz, ten en cuenta que en un futuro tendremos que añadirle
> cosas como el menú superior y no se si le pondremos algo más. Esto todavía no te lo
> puedo especificar porque hay que hablar primero con Juanra para ver qué quiere que
> añadamos. Así que eso, tenlo en cuenta al escribir el código, para que cuando lo ampliemos
> no sea un rompecabezas encontrar las cosas y no haya que hacer mil cambios.



## Acciones de los botones principales

El botón de **guardar** en la ventana de configuración del modo llamará a una función
con el siguiente esquema cuando sea pulsado:

```python
import json


def save(file='path/to/mode.json'):
    """Save the mode configuration in a .json file."""
    
    # TODO: change mode, config and data to the correct dictionary
    mode = 'Lineal'
    config = {'v_start': 1.2, 'v_stop': -0.1, 'points': 200, }
    data = {'mode': mode, 'config': config}
    
    # write the data dictionary in a .json file
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)
```

El botón de **comenzar** llamará a una función `start()` con el siguiente esquema 
cuando sea pulsado:

```python
import time
import json


def run(electrode, data):
    # TODO: implemented by franciss
    # results = (PCE, FF, Jsc, Voc)
    results = (4.9, 0.70, 7.1, 1.00)
    return results


def start():
    """Collect data from widgets and start measurement process."""
    
    # TODO: change data to the correct dictionary
    data = {'mode': {}, 'repeat': {}, 'cells': {}, }
    
    ##### Don't worry about this commented code
    # 
    # # write the data dictionary in a .json file
    # with open('path/to/file/interface.json', 'w') as f:
    #     json.dump(data, f, indent=2)
    # 
    # # extract data from .json file
    # with open('path/to/file/interface.json', 'r') as f:
    #     data = json.load(f)
    # 
    #####
    
    # variables
    repeat_electrode = data['repeat']['type'] == 'electrode'
    repeat_all = data['repeat']['type'] == 'all'
    
    # sequence of measures
    sequence = []
    for key, value in data['cells'].items():
        number = key.split('_')[-1]
        for electrode in value['electrodes']:
            sequence.append(number+electrode)
            if repeat_electrode:
                for _ in range(data['repeat']['times']):
                    sequence.append(number+electrode)
    basic_sequence = sequence
    if repeat_all:
        sequence *= data['repeat']['times'] + 1 
    
    # TODO: open the window to show the results
    
    # start measurement process
    for iteration in sequence:
        results = run(iteration, data)
        
        # TODO: take results and show them on window
        # TODO: check if stop button has been pressed. If true, break the loop
        
        repeat_all_now = iteration == basic_sequence[-1]
        if repeat_electrode or (repeat_all and repeat_all_now ):
            time.sleep(data['repeat']['wait'])
```

De la definición de la función `run()` me ocupo yo.

> **_NOTA:_**
> Seguramente la pantalla durante la medida se vaya quedando congelada.
> Esto es porque la función `run()` se queda esperando a que el *keithley*
> termine de medir. Además, cuando se ha seleccionado algún tipo de repetición,
> tal y como puedes comprobar en el código, se le dice a python que se espere 
> un rato antes de volver a medir (`time.sleep()`). Mientras python está parado, por
> uno u otro motivo, la ventana de la interfaz no se refresca y el loop que actúa
> de fondo para detectar eventos (pulsar botones, etc.) también se queda parado.
> De esto nos tenemos que ocupar, pero más adelante, cuando ya tengamos más cositas
> hechas. Además hay que mirarlo con cuidado por la solución no es fácil. Por
> ahora vamos a dejarlo así, aunque se quede congelado, no pasa na.