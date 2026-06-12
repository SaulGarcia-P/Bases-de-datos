
---
### Primera Forma Normal (1FN) - Dataset 1: Netflix Movies and TV Shows

#### 1. Estructura original 
La estructura original es una tabla plana que consta de 8,807 registros y 12 columnas. Dado nuestro ánalisis, se detectaron violaciones a la 1FN debido a que contiene campos que almacenan conjuntos de datos y múltiples valores concatenados.

Específicamente, las columnas `director`, `cast`, `country` y `listed_in` almacenan listas de valores separados por comas dentro de una misma celda, rompiendo la regla fundamental de que cada celda debe contener un único valor atómico. Además, la tabla carece de un diseño que prevenga la repetición de grupos de información.

#### Estructura resultante
Para alcanzar la 1FN sin generar una sola tabla con millones de filas redundantes, se crearon nuevas tablas dependientes y se definieron claves primarias (PK) compuestas. La estructura resultante es la siguiente:

* **Tabla `shows**`: `show_id` (PK), `type`, `title`, `release_year`, `rating`, `duration`, `description`, `date_added`.
* **Tabla `show_cast**`: `show_id` (PK), `actor_name` (PK).
* **Tabla `show_director**`: `show_id` (PK), `director_name` (PK).
* **Tabla `show_country**`: `show_id` (PK), `country_name` (PK).
* **Tabla `show_category**`: `show_id` (PK), `category_name` (PK).

#### 3. Explicación de las transformaciones realizadas
El proceso consistió en identificar todas las columnas con listas separadas por comas y dividirlas en registros separados. Dado que intentar mantener esta división en la tabla original provocaría la repetición innecesaria de datos como el título o la descripción, se optó por crear tablas independientes para cada atributo multivaluado.

En estas nuevas tablas, se definió una clave primaria compuesta integrando el `show_id` (para mantener la relación con el título original) y el valor atómico extraído (por ejemplo, el nombre del actor). Esto garantiza que cada registro sea único y que cada celda contenga un valor indivisible, cumpliendo estrictamente con los requisitos de la 1FN.

#### 4. Ejemplos de datos antes y después
**Antes (Tabla Desnormalizada con grupos repetitivos):** 
| show_id | title | cast | country | listed_in |
| --- | --- | --- | --- | --- |
| s2 | Blood & Water | Ama Qamata, Khosi Ngema | South Africa | TV Dramas, TV Mysteries |

**Después (Tablas Transformadas en 1FN):** 
*Tabla: `shows` (Datos atómicos únicos)*
| show_id (PK) | title |
| --- | --- |
| s2 | Blood & Water |

*Tabla: `show_cast` (Separación de registros múltiples)*
| show_id (PK) | actor_name (PK) |
| --- | --- |
| s2 | Ama Qamata |
| s2 | Khosi Ngema |

*Tabla: `show_category` (Separación de registros múltiples)*
| show_id (PK) | category_name (PK) |
| --- | --- |
| s2 | TV Dramas |
| s2 | TV Mysteries |

---

### Segunda Forma Normal (2FN) - Dataset 1: Netflix Movies and TV Shows

#### Estructura en 1FN 

Al finalizar la etapa anterior, contábamos con la siguiente estructura:
* **`shows`**: `show_id` (PK), `type`, `title`, `release_year`, `rating`, `duration`, `description`, `date_added`.
* **`show_cast`**: `show_id` (PK), `actor_name` (PK).
* **`show_director`**: `show_id` (PK), `director_name` (PK).
* **`show_country`**: `show_id` (PK), `country_name` (PK).
* **`show_category`**: `show_id` (PK), `category_name` (PK).

#### 2. Identificación de dependencias parciales
La regla de la 2FN dicta que una tabla debe estar en 1FN y que todos los atributos no clave deben depender de *toda* la clave primaria compuesta, no solo de una parte de ella .

En nuestra estructura 1FN, las tablas dependientes (`show_cast`, `show_director`, etc.) usan cadenas de texto completas como parte de su clave primaria compuesta (ej. `actor_name`). Esto presenta una **dependencia parcial conceptual y de diseño relacional**:

* Un actor, un director o un país son entidades del mundo real que existen independientemente del `show`. Su identidad (el nombre) depende de la entidad "Actor", no de la combinación `(show_id, actor_name)`.


* Mantener cadenas de texto (`VARCHAR`) repetidas en claves compuestas genera ineficiencia en las consultas y anomalías si quisiéramos agregar más atributos propios del actor en el futuro (ej. fecha de nacimiento), ya que esos atributos dependerían solo del actor y no del `show_id`.

#### Estructura resultante (tablas en 2FN)

Para resolver esto y lograr un modelo relacional robusto, separamos los atributos multivaluados en sus propias tablas "catálogo" (maestras) con identificadores numéricos únicos (PK simples). Luego, resolvemos la relación de muchos-a-muchos (M:N) estableciendo tablas intermedias (puente) con claves foráneas (FK) .

* **Tabla Principal:**
* `shows` (`show_id` PK, `type`, `title`, `release_year`, `rating`, `duration`, `description`, `date_added`)

* **Tablas Catálogo (Entidades Independientes):**
* `actors` (`actor_id` PK, `full_name`)
* `directors` (`director_id` PK, `full_name`)
* `countries` (`country_id` PK, `country_name`)
* `categories` (`category_id` PK, `category_name`)

* **Tablas Puente (Relación M:N, PK Compuesta sin dependencias parciales):**
* `show_actor` (`show_id` PK/FK, `actor_id` PK/FK)
* `show_director` (`show_id` PK/FK, `director_id` PK/FK)
* `show_country` (`show_id` PK/FK, `country_id` PK/FK)
* `show_category` (`show_id` PK/FK, `category_id` PK/FK)



#### 4. Diagramas entidad-relación

**Figura 1.1** Diagrama ER - Transformación a 2FN (Netflix)

#### 5. Ejemplos de datos transformados

**Antes (Estructura en 1FN con texto repetitivo en PK):**

*Tabla: `show_cast*`

| show_id (PK) | actor_name (PK) |
| --- | --- |
| s2 | Ama Qamata |
| s2 | Khosi Ngema |
| s5 | Khosi Ngema |

**Después (Estructura en 2FN con catálogos y tablas puente):**

*Tabla: `actors` (Entidad independiente)*

| actor_id (PK) | full_name |
| --- | --- |
| 1 | Ama Qamata |
| 2 | Khosi Ngema |

*Tabla: `show_actor` (Tabla puente - Dependencia total de la PK compuesta)*

| show_id (PK/FK) | actor_id (PK/FK) |
| --- | --- |
| s2 | 1 |
| s2 | 2 |
| s5 | 2 |

Aquí tienes la documentación final para culminar el proceso teórico del **Dataset 1 (Netflix)**, llevando la base de datos hasta la Tercera Forma Normal (3FN) con todos los elementos que solicita la rúbrica .

---

### Tercera Forma Normal (3FN) - Dataset 1: Netflix Movies and TV Shows

#### 1. Estructura en 2FN 

Al iniciar esta fase, nuestra base de datos cuenta con catálogos independientes y tablas puente, eliminando las dependencias parciales y la redundancia de listas:

* **Tabla Principal:** `shows` (`show_id` PK, `type`, `title`, `release_year`, `rating`, `duration`, `description`, `date_added`)
* **Catálogos:** `actors`, `directors`, `countries`, `categories`.
* **Tablas Puente:** `show_actor`, `show_director`, `show_country`, `show_category`.

#### Identificación de dependencias transitivas

La 3FN exige que la base de datos esté en 2FN y que se eliminen las dependencias transitivas.

* **Problema:** En la tabla `shows`, los atributos `type` (Movie, TV Show) y `rating` (PG-13, TV-MA, R) son atributos categóricos que se repiten como texto a lo largo de miles de filas .

* **Anomalía:** Aunque parecen depender de `show_id`, en realidad representan dominios de datos independientes. Mantenerlos como texto libre permite errores tipográficos (ej. "Tv Show" vs "TV Show") y dificulta la actualización global de una categoría.

#### Estructura final normalizada (tablas en 3FN)
Para resolver esto, extraemos los atributos categóricos a sus propias tablas maestras y los referenciamos en la tabla principal mediante Claves Foráneas (FK) .

* Se crean las tablas `show_types` y `ratings`.
* La tabla `shows` se actualiza para almacenar únicamente `type_id` y `rating_id` en lugar de las cadenas de texto.

#### 4. Modelo relacional completo con todas las tablas

El esquema relacional final queda compuesto por 12 tablas fuertemente tipadas y relacionadas:

1. `shows`
2. `show_types`
3. `ratings`
4. `actors`
5. `show_actor`
6. `directors`
7. `show_director`
8. `countries`
9. `show_country`
10. `categories`
11. `show_category`

**Figura 1.2** Diagrama.

#### Diccionario de datos de cada tabla

A continuación se detalla el esquema principal que refleja la 3FN. 
| Tabla | Columna | Tipo de Dato | Llaves | Descripción |
| --- | --- | --- | --- | --- |
| **shows** | `show_id` | VARCHAR(10) | PK | Identificador original de Netflix (ej. 's1'). |
|  | `type_id` | INT | FK | Referencia al tipo de contenido. |
|  | `title` | VARCHAR(255) |  | Título oficial de la obra. |
|  | `release_year` | INT |  | Año de lanzamiento. |
|  | `rating_id` | INT | FK | Referencia a la clasificación por edades. |
|  | `duration` | VARCHAR(50) |  | Duración (minutos o temporadas). |
|  | `description` | TEXT |  | Sinopsis del contenido. |
|  | `date_added` | DATE |  | Fecha en que se añadió a la plataforma. |
| **show_types** | `type_id` | INT | PK | Identificador numérico autoincremental. |
|  | `type_name` | VARCHAR(50) | UNIQUE | Formato (ej. 'Movie', 'TV Show'). |
| **ratings** | `rating_id` | INT | PK | Identificador numérico autoincremental. |
|  | `code` | VARCHAR(20) | UNIQUE | Código de clasificación (ej. 'PG-13'). |

#### Ejemplos de datos en el modelo normalizado

Así lucen los datos interactuando sin redundancia textual:

**Tabla: `show_types**`

| type_id (PK) | type_name |
| --- | --- |
| 1 | Movie |
| 2 | TV Show |

**Tabla: `ratings**`

| rating_id (PK) | code |
| --- | --- |
| 1 | PG-13 |
| 2 | TV-MA |

**Tabla Principal: `shows` (Completamente Normalizada)**

| show_id (PK) | type_id (FK) | title | release_year | rating_id (FK) |
| --- | --- | --- | --- | --- |
| s1 | 1 | Dick Johnson Is Dead | 2020 | 1 |
| s2 | 2 | Blood & Water | 2021 | 2 |
| s3 | 2 | Ganglands | 2021 | 2 |

---

