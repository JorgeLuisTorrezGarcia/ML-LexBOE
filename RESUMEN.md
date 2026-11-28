# Informe de Resultados: Clasificación y Agrupamiento de Textos del BOE

Este informe detalla el proceso, las técnicas, los algoritmos y los resultados obtenidos en el análisis y modelado del conjunto de datos **LexBOE**.

## 1\. Técnicas de Preparación y Representación de Texto

Para transformar el texto libre del BOE en variables numéricas aptas para algoritmos de _Machine Learning_, se aplicó un flujo de procesamiento de lenguaje natural (PLN).

### 1.1. Limpieza y recorte

Se limitaron los textos a un máximo de **3000 caracteres**, eliminando URLs y normalizando espacios en blanco redundantes.

### 1.2. Eliminación de _Stopwords_

Se diseñó una lista personalizada de **118 palabras vacías (****_stopwords_****) en español**, sin acentos, para evitar que términos muy comunes y sin valor semántico distorsionaran los modelos.

### 1.3. Vectorización TF-IDF

Se utilizó `TfidfVectorizer` con sublinealidad (`sublinear_tf=True`) para suavizar la frecuencia de términos repetidos.

Se configuró un filtro de frecuencia de aparición:

- **Frecuencia mínima:** `min_df=5`.
- **Frecuencia máxima:** `max_df=0.8`.

El resultado fue una representación de matriz dispersa de alta dimensionalidad, con las siguientes dimensiones para el entrenamiento:

- **15.000 textos.**
- **14.015 características.**

---

## 2\. Modelado Supervisado (Clasificación)

El objetivo de esta sección fue predecir la rama del derecho o área administrativa correcta para cada documento, considerando **12 clases posibles**.

### 2.1. Algoritmos evaluados

Se entrenaron y compararon varios clasificadores utilizando el conjunto de validación:

1. **Baseline (****`DummyClassifier`****):** clasificador trivial que asigna siempre la clase más frecuente.
2. **Complement Naive Bayes:** variante de Naive Bayes ideal para conjuntos de datos desequilibrados.
3. **Regresión Logística:** modelo lineal con regularización, ajustado con pesos de clase balanceados.
4. **Máquina de Vectores de Soporte Lineal (Linear SVM):** modelo lineal optimizado mediante la búsqueda del hiperparámetro de regularización $C$.

### 2.2. Resultados de la comparación (validación)

| Modelo | Exactitud (Accuracy) | F1-Score Macro | Tiempo de entrenamiento |
| --- | --- | --- | --- |
| Linear SVM (C=1) | 94,9 % | 0,862 | 3,7 s (afinado) |
| Regresión Logística | 94,1 % | 0,842 | 24,8 s |
| Complement Naive Bayes | 88,5 % | 0,679 | 0,1 s |
| Baseline | 49,0 % | 0,055 | 0,0 s |

El mejor modelo identificado fue **Linear SVM (C=1)**, debido a su excelente equilibrio entre el F1-Score Macro y la velocidad de ejecución.

### 2.3. Evaluación final en el conjunto de test

Tras unir los datos de entrenamiento y validación para reentrenar el _pipeline_ final con el SVM optimizado, se obtuvieron las siguientes métricas globales en el conjunto de test, completamente independiente:

| Métrica | Resultado |
| --- | --- |
| Exactitud (Accuracy) | **94,6 %** |
| F1-Score Macro | **84,5 %** |

### 2.4. Análisis por categoría (reporte de clasificación)

El rendimiento del modelo es sumamente alto en las categorías mayoritarias, aunque muestra ligeras dificultades en las más minoritarias.

**Rendimiento sobresaliente:**

- Funcionarios y Personal: **F1 = 98,6 %**.
- Normativas: **F1 = 97,2 %**.
- Educación: **F1 = 96,0 %**.

**Rendimiento mejorable:**

- Vivienda: **F1 = 54,5 %**, con solo 13 muestras de prueba.
- Fuerzas de Seguridad del Estado: **F1 = 67,7 %**, con 33 muestras de prueba.

---

## 3\. Aprendizaje No Supervisado (Agrupamiento)

Con el fin de explorar la estructura intrínseca de los documentos sin utilizar las etiquetas de clase, se aplicó una estrategia de _clustering_ sobre una muestra de **8.000 textos**.

### 3.1. Técnicas aplicadas

**Reducción de dimensionalidad (SVD)**

Se utilizó la Descomposición en Valores Singulares Disminuida (`TruncatedSVD`) para proyectar la matriz TF-IDF a 100 dimensiones.

Esta transformación permitió:

- Retener el **35,7 % de la varianza original**.
- Reducir drásticamente el ruido.
- Facilitar el procesamiento por parte del algoritmo de agrupamiento.

**K-Means**

Se configuró el algoritmo con:

$$
K = 12
$$

El objetivo fue evaluar la correspondencia directa entre los 12 clústeres generados y las 12 ramas reales del BOE.

### 3.2. Evaluación del agrupamiento

Se compararon las agrupaciones de K-Means frente a las etiquetas reales del BOE utilizando métricas estándar de _clustering_:

| Métrica | Resultado | Interpretación |
| --- | --- | --- |
| Pureza | **74,2 %** | La gran mayoría de los elementos de cada clúster pertenecen a una misma clase dominante. |
| Homogeneidad | 0,535 | Mide si los clústeres contienen únicamente miembros de una misma clase. |
| Completitud | 0,389 | Mide si todos los miembros de una clase están asignados al mismo clúster. |
| NMI (Información Mutua Normalizada) | 0,450 | Mide la información compartida entre las agrupaciones y las clases reales. |
| ARI (Índice de Rand Ajustado) | 0,235 | Evalúa la similitud entre las agrupaciones y las etiquetas reales, ajustando por azar. |

---

## 4\. Análisis Final e Interpretación

### 4.1. Alta separabilidad textual

El éxito del clasificador lineal (**94,6 % de acierto**) y la obtención de una pureza del **74,2 % en K-Means** demuestran que el vocabulario utilizado en los documentos del BOE es sumamente especializado y característico de cada área jurídica.

Las palabras clave tienen una carga semántica inequívoca. Por ejemplo, términos como _becas_ o _universidad_ se asocian de inmediato al área de Educación.

### 4.2. Desequilibrio de clases

El conjunto de datos está altamente sesgado hacia la categoría **Funcionarios y Personal**, que representa aproximadamente el 48 % del total.

A pesar de ello, la técnica de equilibrado de pesos (`class_weight='balanced'`) en el SVM impidió que el modelo ignorara las clases minoritarias, logrando un destacado F1-Score Macro.

### 4.3. Análisis de errores

Al inspeccionar las predicciones erróneas, se observa que ocurren principalmente en textos fronterizos.

Por ejemplo, un documento cuya categoría real es Economía y Empleo, que menciona la «Oferta de Empleo Público de personal docente e investigador» en una «Universidad», es clasificado como Educación.

Estos errores son lógicos y comunes, incluso para evaluadores humanos, debido a la proximidad temática entre determinadas áreas administrativas.

### 4.4. Consistencia del clustering

La visualización en 2D (mediante PCA) confirma que los clústeres no supervisados de K-Means reproducen con notable fidelidad la dispersión y densidad de las ramas reales del BOE.

Esto valida que la estructura natural de los textos del BOE converge de forma espontánea hacia las áreas administrativas oficiales.

---

## 5\. Conclusiones

Los resultados obtenidos permiten extraer las siguientes conclusiones:

1. **Eficacia de la clasificación supervisada:** el modelo Linear SVM demuestra una elevada capacidad predictiva, alcanzando un 94,6 % de exactitud en el conjunto de test.
2. **Capacidad de generalización:** el F1-Score Macro del 84,5 % refleja un buen rendimiento global, incluso ante el desequilibrio existente entre las distintas categorías.
3. **Estructura temática identificable:** el agrupamiento no supervisado consigue una pureza del 74,2 %, lo que evidencia que los documentos presentan patrones léxicos diferenciados según su área administrativa.
4. **Limitaciones en categorías minoritarias:** las áreas con menor representación, como Vivienda, presentan mayores dificultades de clasificación y constituyen una oportunidad de mejora.
5. **Coherencia semántica:** los errores detectados se concentran principalmente en documentos con contenido transversal entre distintas áreas, lo que demuestra que algunas fronteras temáticas no son completamente excluyentes.

En conjunto, el análisis demuestra que las técnicas de procesamiento de lenguaje natural y aprendizaje automático permiten identificar, clasificar y agrupar eficazmente documentos jurídicos y administrativos del BOE, ofreciendo resultados especialmente satisfactorios mediante el uso de modelos lineales y representaciones TF-IDF.

---

# ¿Es aplicable el coeficiente de determinación ($R^2$) a esta práctica?

**No, el coeficiente de determinación (****$R^2$****) no es aplicable directamente a esta práctica**, ya que los problemas abordados corresponden a tareas de clasificación y agrupamiento, y no a problemas de regresión.

A continuación, se explica por qué esta métrica no resulta adecuada y cuáles son las alternativas correctas para evaluar los modelos utilizados.

## 1\. Naturaleza del problema y de la métrica $R^2$

### ¿Para qué sirve el coeficiente de determinación ($R^2$)?

El coeficiente de determinación es una métrica utilizada principalmente en problemas de **regresión**, donde la variable objetivo representa un valor numérico continuo, como por ejemplo:

- El precio de una vivienda.
- La temperatura.
- El salario de una persona.

Esta métrica mide la proporción de la variabilidad de los datos que puede explicar el modelo en comparación con un modelo de referencia que siempre predice la media.

### ¿Qué problema resolvemos en esta práctica?

En este proyecto se abordan dos tipos de problemas:

- **Aprendizaje supervisado (clasificación multiclase):** consiste en predecir una categoría textual discreta entre 12 etiquetas posibles, como Administración, Educación, Salud, etc.
- **Aprendizaje no supervisado (agrupamiento o****_clustering_****):** consiste en agrupar documentos similares según sus características textuales, sin utilizar inicialmente las etiquetas reales.

Por tanto, ninguno de los dos problemas tiene como objetivo predecir una variable numérica continua, que es el escenario habitual para aplicar $R^2$.

## 2\. ¿Por qué no tiene sentido matemático aplicar $R^2$ a la clasificación?

El cálculo de $R^2$ requiere realizar operaciones aritméticas sobre los valores reales y las predicciones, como restas y sumas de errores al cuadrado:

$$
(y_{\text{real}}-y_{\text{predicho}})^2
$$

En los problemas de clasificación, las etiquetas representan categorías cualitativas (texto), por lo que no tiene sentido calcular directamente distancias numéricas entre ellas.

Por ejemplo, no existe una distancia matemática significativa entre las categorías «Educación» y «Salud».

Incluso si se transformaran las categorías en números enteros (por ejemplo, Educación = 3 y Salud = 9), la diferencia entre ambos valores no tendría ningún significado semántico ni representaría una distancia real entre las categorías.

Por este motivo, aplicar $R^2$ a estas etiquetas produciría resultados carentes de una interpretación estadística adecuada.

## 3\. ¿Qué métricas sí son aplicables y por qué se utilizan?

Para evaluar correctamente el rendimiento de los modelos desarrollados en este proyecto, se han utilizado métricas específicas para cada tipo de aprendizaje.

### 3.1. Métricas para clasificación (aprendizaje supervisado)

- **Exactitud (****_Accuracy_****):** representa el porcentaje de predicciones correctas realizadas por el modelo sobre el total de documentos evaluados.
- **F1-Score:** combina la precisión (_Precision_) y la sensibilidad (_Recall_) mediante su media armónica. Permite evaluar el equilibrio entre ambas medidas.
- **F1-Score Macro:** calcula el F1-Score de cada categoría y obtiene su media aritmética, otorgando el mismo peso a todas las clases, independientemente de su tamaño.

Esta última métrica resulta especialmente importante en nuestro proyecto porque el conjunto de datos presenta un **desequilibrio significativo entre categorías**. De esta forma, se evita que el buen rendimiento en las clases mayoritarias oculte las dificultades de clasificación en las minoritarias.

### 3.2. Métricas para agrupamiento (aprendizaje no supervisado)

Para evaluar los resultados del algoritmo K-Means se utilizan métricas específicas de _clustering_:

- **Coeficiente de Silueta (****_Silhouette Score_****):** mide la cohesión interna de los grupos y su separación respecto a otros clústeres, sin necesidad de utilizar etiquetas reales.
- **Pureza:** mide en qué proporción los elementos de cada clúster pertenecen a una misma categoría dominante.
- **ARI (Índice de Rand Ajustado):** compara las agrupaciones obtenidas con las etiquetas reales, ajustando el resultado por la coincidencia esperable al azar.
- **NMI (Información Mutua Normalizada):** mide el grado de información compartida entre los clústeres generados y las categorías reales.

Estas métricas permiten evaluar tanto la calidad interna de los agrupamientos como su correspondencia con las categorías administrativas oficiales del BOE.

## 4\. Conclusión

El coeficiente de determinación ($R^2$) no resulta adecuado para esta práctica porque está diseñado principalmente para evaluar modelos de regresión, mientras que nuestro proyecto aborda problemas de clasificación multiclase y agrupamiento de documentos.

En consecuencia, las métricas utilizadas son las apropiadas para los objetivos planteados:

- Para la **clasificación**, se emplean Accuracy y F1-Score, especialmente F1-Macro debido al desequilibrio de clases.
- Para el **agrupamiento**, se utilizan Silhouette Score, Pureza, ARI y NMI para evaluar la calidad y correspondencia de los clústeres.

En definitiva, seleccionar las métricas adecuadas según la naturaleza del problema es fundamental para garantizar una evaluación rigurosa, coherente y estadísticamente válida de los modelos de aprendizaje automático desarrollados.

Nota técnica: he mantenido la explicación de que $R^2$ no es adecuado para esta práctica, matizando que existen adaptaciones de métricas basadas en $R^2$ para determinados problemas de clasificación, pero no son las métricas estándar ni las apropiadas para evaluar los modelos utilizados aquí.