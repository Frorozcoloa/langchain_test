# Prueba técnica

## ***Agentes de Usuario:***

El agente de usuario se encuentra implementado en el archivo `users.py`. En este momento, el agente tiene la responsabilidad de recibir una descripción del usuario y devolver un JSON con los topics detectados en el archivo. A continuación, se presenta un ejemplo de entrada para el modelo:

```
I love biking, hiking and walking. I like to get to know new towns, talk to people. I hate when plans don't happen, I'm very strict with times. I love to eat, I always like to go to good restaurants and try the food, I don't like to see many dishes and I hate the noise, I like the countryside and live there.
```

En consecuencia, el modelo devolverá los topics principales del usuario en el siguiente formato:

```
,topic_name,topic_description
0,Outdoor Activities,"The user enjoys biking, hiking, and walking. They also like exploring new towns."
1,Social Interaction,The user enjoys talking to people and socializing.
2,Punctuality,The user values time and dislikes when plans do not happen as scheduled.
3,Food and Dining,The user loves eating and trying out food in good restaurants. They prefer not to see many dishes and dislike noise.
4,Living Preferences,The user prefers the quiet and peaceful environment of the countryside for living.
```

En este formato, se incluye el nombre del tema y una descripción detallada asociada a cada uno.

### **Prompt**

El prompt utilizado para el sistema es el siguiente:

> `You are a helpful assistant. Your task is to analyze the users of an ecommerce.`


Este prompt fue creado mediante la conversación en CodeGPT para establecer una nomenclatura coherente.

Además, el siguiente prompt se utiliza para extraer los tópicos a partir de los perfiles de usuarios:

>
> Please, identify the main topics mentioned in these users profile.
>
>     Return a list of 3-5 topics.
>
>     Output is a JSON list with the following format
>
>     [
>
>     {{"topic_name": "`<topic1>`", "topic_description": "<topic_description1>"}},
>
>     {{"topic_name": "`<topic2>`", "topic_description": "<topic_description2>"}},
>
>     ...
>
>     ]
>
>     Users profile:
>
>     {users_profile}

Estos son los prompts específicos utilizados en conjunto con el sistema.

### Conexión con codegpt

La conexión con el sistema se llevó a cabo utilizando la librería Langchain. La descripción del usuario se proporciona como entrada al sistema a través de esta librería.

El flujo de trabajo implica enviar la descripción del usuario como input al sistema, que a su vez utiliza la librería Langchain para procesar y analizar la información proporcionada.

### Ejecutar

Para ejecutar el código es lo siguiente:

```bash
python users.py
```

## ***Agentes de Producto***:

El agente de productos opera de manera similar al agente de usuario. Recibe una descripción del producto como entrada y genera los principales tópicos asociados con dicho producto. A continuación, se presenta un ejemplo de entrada y salida del agente de productos:

```
Small 10-liter hiking backpack nh100 quechua black, BENEFITS
Carrying comfort, COMFORT CARRYING COMFORT Spalder and padded straps 
1 main compartment with double zipper 
VOLUME
Volume: 10 liters | Weight: 145 g | Dimensions: 39 x 21 x 12 cm.friction resistance
FRICTION RESISTANCE
Durable, abrasion-resistant materials and joints. 10-year warranty. Warranty 10 years.Ventilation
VENTILATION
Simple to use backrest
EASE OF USE
Easy access to the external pocket by placing the backpack in a horizontal position while hiking.
```


### **Tópicos Generados por el Agente de Productos:**

```
,type_classes,class_description
0,Outdoor Gear,"This product is a small 10-liter hiking backpack, designed for outdoor activities such as hiking, trekking, and camping."
1,Travel Equipment,"With its compact size and lightweight design, this backpack is also suitable for travel, making it easy to carry essentials."
2,Sporting Goods,The backpack's durability and resistance to abrasion make it a good fit for sports and other physical activities.
3,Luggage & Bags,"As a backpack, this product falls under the category of luggage and bags."
4,Fitness & Wellness,"Given its use in hiking and other physical activities, this product is also related to fitness and 
wellness."
5,Warranty Services,"The product comes with a 10-year warranty, indicating a commitment to long-term service and quality 
assurance."
```

La información sobre el nombre y la descripción de los tópicos tiene como objetivo facilitar búsquedas por similitud, permitiendo identificar características específicas del producto que podrían interesar al usuario final. Se considera la posibilidad de utilizar esta información en el futuro para generar promociones enfocadas en los gustos del usuario mediante consultas a plataformas como Stable Diffusion o MidJournal.

### Prompt

El prompt utilizado para el sistema es el siguiente:

> You are a helpful assistant. Your task is to analyze the products of an e-commerce.

El promp Human para el chat es similar al del agente usario.

### Conexión con code GPT

En el contexto de esta prueba, todos los agentes se conectaron al mismo modelo. Sin embargo, en la práctica, esta integración no debería ocurrir de esta manera. Por ejemplo este modelo debe estar un modelo que tiene como base de conocimientos, la misión, visión, la estrategía de mercada y demás carateristicas propiar del e-commerce.

La segmentación y especialización de modelos contribuirían a una experiencia más personalizada y eficiente para los usuarios finales, al tiempo que garantizarían una coherencia total con la estrategia general del e-commerce.

### Ejecutar el código

```bash
python prodcut.py
```

## ***Agentes de Análisis de Tendencias:***


El agente encargado del análisis de tendencias es uno de mis favoritos. Su desarrollo comienza con la búsqueda de las 100 primeras páginas web en Google, seguida por un proceso de web scraping en el que se recopilan datos. Todos estos datos obtenidos se almacenan en el objeto "documentos" de Langchain y se envían para su resumen mediante la técnica de MapReduce. Posteriormente, se extraen los tópicos para comprender las tendencias y los temas de actualidad en Internet.

Es importante señalar que, si bien la librería de Langchain ya ofrece la opción de buscar en Internet, nuestro enfoque busca obtener información más detallada para comprender a fondo las tendencias del mercado. Este enfoque nos permite tener una visión más completa y detallada de los temas relevantes en la red.

### Prompt

#### summary

Este es el prompt utilizado para realizar el resumen:

```
The following is a set of documents:
{docs}
Based on this list of docs, please identify the main themes
Helpful Answer:`
```

#### extracción de tópicos

Este es prompt utilizado

```
Given the following docs about a sports e-commerce, conduct an analysis of potential future trends.
        return a list of 10 topics.
        Output is a JSON list with the following format
        [
            {{"product_decription": "<product_decription>", "product_to_sell": "<product_to_sell1>"}},}}, 
            {{"product_decription": "<product_decription>", "product_to_sell": "<product_to_sell2>"}},}},
            ...
        ]
        {docs}
```

El input del sistema consiste en la query a buscar, la cual se obtiene utilizando la librería `googlesearch`, seguida de la utilización de `newspaper3` para extraer los datos relevantes. Después de este proceso, se emplea Langchain para realizar tanto el resumen como la extracción de tópicos, estableciendo conexiones con CodeGPT.

Este flujo de trabajo integral permite no solo la obtención de información precisa mediante la búsqueda en Internet, sino también la aplicación de técnicas avanzadas de resumen y análisis de tópicos gracias a Langchain y la interacción con CodeGPT. La combinación de estas herramientas asegura una comprensión profunda de las tendencias y temas relevantes en el entorno digital.

### ejecutar el código

```bash
python trends.py
```

## Algoritmo de scoring


**Algoritmo de Scoring: Comparación de Tópicos de Productos y Tendencias**

Para calcular el puntaje, se utiliza la similitud del coseno entre dos palabras. En este contexto, el proceso inicia comparando los tópicos del producto con las tendencias, siguiendo estas combinaciones:

1. **Título 1 con Título 2:** Se realiza una comparación de similitud de coseno entre los títulos de los productos.
2. **Descripción 1 con Descripción 2:** Similaridad de coseno entre las descripciones de los productos.
3. **Título 1 con Descripción 2:** Comparación entre el título del producto 1 y la descripción del producto 2.
4. **Descripción 1 con Título 2:** Comparación entre la descripción del producto 1 y el título del producto 2.

Luego de realizar estas comparaciones, los puntajes obtenidos se suman. Se realizó una prueba dividiendo los textos de las descripciones, aunque no se observó una variación significativa en los resultados.

Este enfoque integral permite evaluar la similitud entre los tópicos de los productos y las tendencias identificadas, proporcionando un puntaje acumulativo que refleja la relevancia y correspondencia entre ambos conjuntos de datos.

#### Algoritmo de Scoring: Comparación de Tópicos de usrios y productos

Después de determinar qué tópicos de nuestros productos coinciden con las tendencias identificadas, se lleva a cabo un proceso de filtrado mediante un umbral establecido. Los tópicos que superan este umbral se consideran relevantes y se procede a realizar el mismo procedimiento, pero utilizando los tópicos asociados al usuario.

El proceso se repite de la siguiente manera:

1. **Título 1 con Título 2:** Se compara la similitud de coseno entre los títulos filtrados por tendencias del producto y los tópicos del usuario.
2. **Descripción 1 con Descripción 2:** Se evalúa la similitud de coseno entre las descripciones filtradas por tendencias del producto y los tópicos del usuario.
3. **Título 1 con Descripción 2:** Se realiza la comparación entre el título del producto, filtrado por tendencias, y la descripción del usuario.
4. **Descripción 1 con Título 2:** Comparación entre la descripción del producto, filtrada por tendencias, y el título del usuario.

Este enfoque de filtrado por umbral asegura que solo se consideren los tópicos más relevantes para el usuario, basados en las tendencias identificadas. Este proceso refinado mejora la correspondencia y la personalización del sistema al adaptarse a los intereses específicos del usuario en relación con las tendencias actuales del mercado.

Al final se va a observa lo siguiente:

```
2           2      Sporting Goods  The backpack's durability and resistance to ab...  1.280408
4           4  Fitness & Wellness  Given its use in hiking and other physical act...  0.910994
0           0        Outdoor Gear  This product is a small 10-liter hiking backpa...  0.758707
1           1    Travel Equipment  With its compact size and lightweight design, ...  0.664162
3           3      Luggage & Bags  As a backpack, this product falls under the ca...  0.623401
5           5   Warranty Services  The product comes with a 10-year warranty, ind...  0.195448
```

Donde se obtiene una lista de mayor a menor de partes del producto que le gusta al usario. Este puede ser el input de stable diffusion y ser usado como pieza publicitaria.

```bash
python get_scoring.py
```

## ***Agentes de Retroalimentación:***


Para desarrollar el siguiente agente, empleamos la librería "autogen", haciendo uso de diferentes agentes especializados:

1. **Data Analyst (Analista de Datos):** Este agente se encarga de analizar el perfil del usuario y realizar modificaciones según los cambios propuestos. Su función principal es asegurar que el perfil del usuario se adapte de manera óptima a las necesidades y preferencias actuales.
2. **Engineer (Ingeniero):** El ingeniero es responsable de crear código, realizar gráficos (plots) y extraer información relevante. Su labor abarca la implementación de soluciones técnicas para procesar y presentar datos de manera efectiva.
3. **Executor (Ejecutor):** Este agente tiene la tarea de ejecutar el código desarrollado por el ingeniero. Su función es llevar a cabo las operaciones técnicas de manera eficiente y precisa.
4. **Reviewer (Revisor):** El papel del revisor es imitar al usuario. Este agente debe estar conectado a un Recurrent Attention Generator (RAG) para tener más información sobre el usuario y poder asistir al analista respondiendo preguntas que obtiene durante el proceso de análisis.

La colaboración entre estos agentes, cada uno con un rol específico, permite un desarrollo integral y eficiente del sistema, abarcando desde la modificación del perfil del usuario hasta la ejecución y revisión de las operaciones técnicas. Este enfoque modular facilita la gestión y mejora la efectividad de cada tarea especializada.

Todo este proceso se llevó a cabo utilizando la comunicación de chat grupal. La interacción y coordinación entre los agentes se facilitaron a través de este entorno colaborativo, permitiendo una comunicación fluida y eficiente entre los diversos componentes del sistema.

### Input

Obviamente, al trabajar con varios agentes, la entrada de información puede provenir de diversas fuentes, como las URL de archivos, consultas a bases de datos, entre otros. En este caso, utilizamos una breve descripción (que puede ser generada por un agente) que resume los cambios observados:

"There is a user with ID 1234451 who enjoys mountain biking. Cycling clothing, glasses, and other gear have been recommended to them, but they have not made any purchases. We have noticed an increase in their searches for therapeutic items, such as orthopedic collars and small weights, among others. We have also observed a change in location from a mountainous area with few inhabitants to a larger area."

Esta descripción proporciona un panorama de la situación del usuario, incluyendo sus preferencias, recomendaciones anteriores y cambios notables en su comportamiento, como la búsqueda de artículos terapéuticos y el cambio de ubicación geográfica. Este tipo de resumen sirve como entrada clave para los agentes especializados, permitiéndoles adaptar eficientemente el perfil del usuario según las nuevas circunstancias.

### Output

El resultado del modelo es el siguiente:

"The user with ID 1234451, previously interested in mountain biking and related gear, has shown a recent shift in interest towards therapeutic items such as orthopedic collars and small weights. This change, coupled with a relocation from a mountainous area to a larger city, suggests a potential health concern. The recommendation strategy for this user will be updated to focus on health and wellness products, including ergonomic furniture, physiotherapy equipment, and health supplements."

Lo que destaca es cómo el modelo pudo intuir que el usuario posiblemente tenga alguna molestia o inquietud relacionada con su salud. La capacidad del sistema para reconocer estos cambios sutiles y adaptar la estrategia de recomendación en consecuencia es uno de los aspectos más sorprendentes y valiosos de esta prueba técnica. Este enfoque proactivo y sensible a las señales del usuario demuestra la eficacia del sistema para comprender y responder de manera inteligente a las evoluciones en las preferencias y necesidades de los usuarios.

### Ejecutar código

```bash
python  reviewer_agents.py
```

## ***Integración con Redes Sociales***

Para abordar el flujo de identificar perfiles similares, proponemos un enfoque en dos etapas:

1. **Extracción de Información de Imágenes:**
   * Utilizamos comentarios y convertimos la información de las imágenes a texto.
   * Creamos perfiles individuales para cada persona basándonos en los datos obtenidos de las imágenes.
2. **Búsqueda de Similitudes entre Perfiles:**
   * Utilizamos técnicas como la similitud del coseno para comparar los perfiles y encontrar similitudes.
   * Implementamos un pipeline end-to-end que integra GPT-4 para analizar y encontrar patrones comunes en los perfiles.

Este enfoque nos permite aprovechar tanto la información textual como visual de los comentarios e imágenes. Al convertir la información de las imágenes a texto, creamos perfiles más ricos y completos. La búsqueda de similitudes se realiza mediante técnicas de procesamiento de lenguaje natural y modelos avanzados como GPT-4, lo que nos proporciona un análisis más profundo y detallado de los perfiles.

El uso de la similitud del coseno y la incorporación de GPT-4 en un pipeline end-to-end potencian la capacidad del sistema para identificar patrones y conexiones entre los perfiles, ofreciendo una visión más completa y precisa de las similitudes entre las personas en función de sus perfiles. Este enfoque integral permite un análisis exhaustivo y eficiente de los perfiles similares en el contexto dado.
