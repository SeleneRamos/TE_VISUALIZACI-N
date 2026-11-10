"""Textos de contexto e interpretación de la app (tomados del informe en R Markdown)."""

INTRO = """
Esta app muestra la vigilancia epidemiológica del dengue en el Perú entre 2000 y 2025 con gráficos
interactivos hechos con **Highcharts**, la librería de JavaScript que está detrás del paquete
highcharter de R. En el informe en R Markdown los gráficos se hicieron con highcharter; aquí se usa
la misma librería desde Python, armando cada gráfico como un diccionario de opciones.

Al pasar el mouse sobre los gráficos aparece la información de cada punto. También se puede hacer zoom,
ocultar series desde la leyenda y descargar los gráficos desde el menú de la esquina superior derecha.
"""

DATOS = """
Se usa el dataset Vigilancia Epidemiológica de dengue, publicado en la
[Plataforma Nacional de Datos Abiertos](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-dengue).
Lo administra el Centro Nacional de Epidemiología, Prevención y Control de Enfermedades (CDC Perú) del
Ministerio de Salud. Los casos llegan a través de la Red Nacional de Epidemiología (RENACE), formada por
10 272 establecimientos de salud del MINSA, EsSalud y otras instituciones del sector. De ellos, 8 536 son
unidades notificantes que reportan los casos cada semana.

Cada fila de la base es un caso de dengue notificado. Indica dónde se habría contagiado la persona, la
semana en que empezaron los síntomas, la gravedad del caso, el tipo de diagnóstico, la edad y el sexo.
El CDC aclara que los datos son provisionales y pueden cambiar con las actualizaciones.

El archivo original tiene más de un millón de registros y pesa más de 100 MB. Para que la app cargue
rápido, los casos se agruparon antes por año, semana, departamento, gravedad, diagnóstico, sexo y grupo
de edad. Los grupos de edad siguen las etapas de vida que usa el MINSA.
"""

COMO_USAR = """
1. En la barra lateral elige el rango de años y, si quieres, uno o varios departamentos.
2. Recorre las pestañas en orden: primero la descripción de los datos, luego cuándo (Tiempo), dónde
   (Territorio) y a quiénes (Población) afecta el dengue.
3. Pasa el mouse sobre los gráficos para ver los valores exactos. En la serie semanal usa los botones de
   periodo y en el gráfico de departamentos haz clic en una barra para ver sus provincias.
4. En Clustering mueve el control para probar con más o menos grupos.
5. Si una palabra no es clara, búscala en el Glosario.
"""

DATOS_INTRO = """
Esta pestaña describe la base antes de pasar a los gráficos: de dónde viene, qué variables tiene, cuáles
se crearon para el análisis y cómo se reparten los casos en cada categoría. Los números de esta pestaña
usan los datos completos, sin filtros.
"""

DATOS_TABLA = """
La base original tiene 15 variables. En la app se usan 9 de ellas y se crearon 4 nuevas durante la
limpieza. Las variables que no se usan (distrito, localidad, diresa, ubigeo y localcod) dan más detalle
del lugar, pero el análisis se hizo a nivel de departamento y provincia.
"""

DATOS_CATEGORIAS = """
La tabla muestra cuántos casos hay en cada categoría. Sirve para revisar que la limpieza funcionó y para
ver si quedaron datos vacíos. "Sin dato" agrupa los casos que no tenían esa información.
"""

# (variable, tipo, origen, descripción, valores; "{...}" se completa con la data)
DICCIONARIO = [
    ("departamento", "Texto", "Original", "Departamento del lugar probable de infección.",
     "{n_dep} departamentos con casos"),
    ("provincia", "Texto", "Original", "Provincia del lugar probable de infección.",
     "{n_prov} provincias con casos"),
    ("distrito", "Texto", "Original (no se usa)", "Distrito del lugar probable de infección.", "Nombre del distrito"),
    ("localidad", "Texto", "Original (no se usa)", "Centro poblado o localidad de infección.", "Nombre de la localidad"),
    ("enfermedad", "Texto", "Original", "Clasificación del caso según su gravedad.",
     "Sin signos de alarma, con signos de alarma, grave"),
    ("ano", "Entero", "Original", "Año de inicio de síntomas.", "{anio_min} a {anio_max}"),
    ("semana", "Entero", "Original", "Semana epidemiológica de inicio de síntomas.", "1 a 53"),
    ("diagnostic", "Texto", "Original", "Código CIE-10 del diagnóstico.", "A97.0, A97.1, A97.2"),
    ("tipo_dx", "Texto", "Original", "Tipo de diagnóstico.", "C = confirmado, P = probable, S = sospechoso"),
    ("diresa", "Texto", "Original (no se usa)", "Código de la dirección regional de salud que notifica.", "Código numérico"),
    ("ubigeo", "Texto", "Original (no se usa)", "Código INEI del lugar probable de infección.", "6 dígitos, por ejemplo 100605"),
    ("localcod", "Texto", "Original (no se usa)", "Código de la localidad de infección.", "Código numérico"),
    ("edad", "Numérico", "Original", "Edad del paciente, en la unidad que indica tipo_edad.", "Número"),
    ("tipo_edad", "Texto", "Original", "Unidad de la edad.", "A = años, M = meses, D = días"),
    ("sexo", "Texto", "Original", "Sexo del paciente.", "M = masculino, F = femenino"),
    ("edad_anios", "Numérico", "Creada", "Edad pasada a años según tipo_edad (meses / 12, días / 365).", "Número"),
    ("grupo_edad", "Texto", "Creada", "Etapa de vida según el MINSA.", "0-4, 5-11, 12-17, 18-29, 30-59, 60+"),
    ("fecha", "Fecha", "Creada", "Fecha aproximada de la semana: 1 de enero más las semanas transcurridas.",
     "Para la serie semanal"),
    ("casos", "Entero", "Creada", "Número de casos en cada combinación de año, semana, departamento, gravedad, "
     "diagnóstico, sexo y grupo de edad.", "Conteo"),
]

AVISO_FILTROS = """
Los filtros de la barra lateral cambian los gráficos de las pestañas Tiempo, Territorio y Población.
Los textos de interpretación describen los datos completos (2000–2025, todo el país).
"""

ANIO_ANTES = """
La primera pregunta es cómo cambió el número de casos a lo largo del tiempo. El año con más casos se
pinta de naranja para que resalte apenas se abre el gráfico. Al pasar el mouse sobre una barra se ve el
total exacto de ese año.
"""

ANIO_DESPUES = """
El dengue en el Perú no creció de forma pareja, sino por brotes. Entre 2000 y 2009 los casos casi siempre
estuvieron por debajo de 20 mil al año. Desde 2010 empezaron a subir y aparecieron años con picos
marcados, como 2017, con alrededor de 65 mil casos, y 2022, con cerca de 60 mil. Después de cada pico los
casos bajan, como en 2018, que fue uno de los años con menos casos de todo el periodo.

El cambio más fuerte llegó en 2023 y 2024. El año con más casos fue {anio_max}, con {casos_max} casos
notificados, y 2023 quedó muy cerca. Entre los dos suman {casos_2324} casos, más que todos los años de
2000 a 2022 juntos ({casos_hasta22}). En 2025 los casos bajaron a niveles parecidos a los de 2015.

En 2023, varios departamentos de la costa norte con muchos casos, como Piura, Lambayeque y La Libertad,
sufrieron lluvias extremas por el ciclón Yaku a inicios de marzo. Esos mismos departamentos ya habían
tenido muchos casos en el brote de 2017 (Munayco et al., 2024).
"""

SEMANAL_ANTES = """
El gráfico anterior muestra cuántos casos hubo cada año, pero no cuándo aparecieron dentro del año. Esta
serie de tiempo cuenta los casos por semana y trae botones para elegir el periodo (1, 3, 5 o 10 años) y
una barra en la parte de abajo para moverse en el tiempo y acercarse a un brote.
"""

SEMANAL_DESPUES = """
Vista semana a semana, la serie pasa casi todo el tiempo cerca de cero y se dispara en momentos
puntuales. Cada brote dura pocas semanas: sube rápido, llega a su punto más alto y vuelve a bajar. Hasta
2016 los picos casi nunca pasaron de 2 mil casos por semana. En 2017 el pico llegó a cerca de 5 mil.

Lo que no se veía en el gráfico por año es que 2023 y 2024 fueron dos brotes separados y no una sola ola
larga. El primero llegó a cerca de 17 mil casos en una semana y el segundo superó los 19 mil. Entre
ambos, los casos bajaron casi a cero durante la segunda mitad de 2023. Con el botón "3a" se puede ver
este periodo de cerca.
"""

CALOR_ANTES = """
La serie semanal mostró que los brotes duran pocas semanas, pero los años con más casos tapan a los
demás. En este mapa de calor cada fila es un año y cada columna una semana. El color no indica la
cantidad de casos, sino qué porcentaje de los casos de ese año se notificó en esa semana. Así un año con
pocos casos se puede comparar con uno de epidemia.
"""

CALOR_DESPUES = """
En casi todos los años las celdas más oscuras están en la primera mitad del año, entre febrero y mayo,
que en el Perú son los meses de más calor y lluvias. En la segunda mitad del año los casos son muy pocos,
lo que confirma que el dengue en el país es estacional.

La época del brote no fue la misma en los dos años de epidemia. En 2023 la mayor parte de los casos se
notificó entre fines de mayo e inicios de junio (semanas 19 a 24), más tarde de lo normal. En 2024 el
brote se adelantó y se concentró entre marzo y abril (semanas 10 a 17).
"""

MAPA_ANTES = """
Después de ver cuándo aparecen los casos, la siguiente pregunta es dónde. El mapa suma los casos por
departamento. El mapa de Highcharts separa Lima Metropolitana de Lima Provincias, por eso los casos de
Lima se reparten según la provincia. Se puede acercar con los botones + y -.
"""

MAPA_DESPUES = """
Los colores usan una escala logarítmica, donde cada paso de la leyenda multiplica los casos por 100. Se
eligió así porque la diferencia entre departamentos es enorme: con una escala normal, solo los más
afectados tendrían color y el resto se vería igual.

El mapa muestra dos zonas con más casos: la costa norte (Tumbes, Piura, Lambayeque y La Libertad) y la
selva (Loreto, San Martín, Ucayali y Madre de Dios). Las dos son cálidas y húmedas, y allí vive el
zancudo *Aedes aegypti*. Lima también tiene un color oscuro. En la sierra y en el sur los colores son
mucho más claros. Arequipa, Moquegua y Puno tienen pocos casos, y Huancavelica y Tacna no registran
casos como lugar de contagio. Ica es la excepción en la costa sur, con un color más oscuro que sus
vecinos.
"""

DRILL_ANTES = """
Con la escala logarítmica del mapa cuesta comparar un departamento con otro. Por eso aquí se ordenan los
15 departamentos con más casos. Al hacer clic en una barra se abren las 10 provincias con más casos de
ese departamento, y con el botón "Volver" se regresa.
"""

DRILL_DESPUES = """
Piura es por mucho el departamento con más casos, con cerca de 240 mil entre 2000 y 2025. Eso es casi el
doble que Lima, que está en segundo lugar, y equivale al {pct_piura}% de todos los casos del país.
Después vienen Loreto y La Libertad, ambos con más de 100 mil casos.

Hay que tener en cuenta que estas cifras son casos y no tasas: Lima tiene muchos casos en parte porque es
el departamento con más población. Tumbes, en cambio, aparece en el noveno lugar, pero tiene muy pocos
habitantes. Si se calculara la tasa por cada 100 mil habitantes, probablemente estaría entre los primeros.
"""

GRAVEDAD_ANTES = """
Además de cuántos casos hubo y dónde, importa qué tan graves fueron. En 2009 la OMS propuso clasificar el
dengue en tres niveles: sin signos de alarma, con signos de alarma (por ejemplo, dolor abdominal fuerte,
vómitos persistentes o sangrado de encías) y dengue grave. En esta base la clasificación se puede comparar
recién desde 2011, por eso el gráfico empieza ese año. Las barras están apiladas al 100 %.
"""

GRAVEDAD_DESPUES = """
La mayoría de los casos son leves. En todos los años, entre el 73 % y el 91 % fueron dengue sin signos de
alarma. El dengue grave es muy poco frecuente y no pasa del 2 % en ningún año.

El porcentaje de casos con signos de alarma fue más alto en 2013, 2014 y 2018, con alrededor de un cuarto
de los casos, y más bajo en 2021 y 2024, con cerca del 10 %. Llama la atención que 2018, uno de los años
con menos casos, tenga uno de los porcentajes más altos, mientras que 2023 y 2024, los años de epidemia,
tienen porcentajes bajos. Una posible explicación es que en los años de epidemia se notifican muchos más
casos leves, mientras que en los años tranquilos llegan sobre todo los casos que necesitan atención médica.
"""

PIRAMIDE_ANTES = """
Falta ver a quiénes afecta más el dengue. En la pirámide los hombres van hacia la izquierda y las mujeres
hacia la derecha.
"""

PIRAMIDE_DESPUES = """
El grupo de 30 a 59 años es el que tiene más casos, seguido por el de 18 a 29. Hay que tener cuidado al
compararlos, porque los grupos no tienen el mismo tamaño: el de 30 a 59 abarca 30 años, mientras que el
de 0 a 4 solo cinco. Aun así, los niños menores de 5 años son el grupo con menos casos.

En los niños y adolescentes los casos están casi parejos entre hombres y mujeres. Desde los 18 años las
mujeres pasan adelante, y entre los 30 y 59 años tienen cerca de 228 mil casos frente a unos 172 mil de
los hombres. En total, el {pct_mujeres}% de los casos son mujeres. La base no explica esta diferencia. Una
posibilidad es que el zancudo *Aedes aegypti* vive dentro y alrededor de las viviendas (OPS, s.f.), donde
muchas mujeres adultas pasan más tiempo. Otra es que las mujeres acuden más a los establecimientos de
salud y por eso más casos suyos llegan a notificarse.
"""

DX_ANTES = """
Un caso confirmado es el que tiene una prueba de laboratorio positiva. Un caso probable es el de una
persona con síntomas de dengue que vive o estuvo en una zona con transmisión, pero que no tiene
confirmación de laboratorio.
"""

DX_DESPUES = """
El {pct_conf} % de los casos son confirmados y el {pct_prob} % son probables. No hay casos sospechosos,
aunque el diccionario de datos sí incluye esa categoría. Casi nueve de cada diez casos tienen respaldo de
laboratorio, lo que da más confianza a los resultados.
"""

CLUSTER_ANTES = """
Los gráficos anteriores muestran cada variable por separado. Para ver qué departamentos se parecen
considerando varias a la vez, se aplicó un clustering jerárquico con el método de Ward. Cada departamento
se describe con seis variables: el número de casos (en logaritmo), el porcentaje de años con casos, el
porcentaje de casos con signos de alarma o graves, la semana mediana de los brotes, el porcentaje de
casos en menores de edad y el porcentaje en mujeres. Las variables se estandarizaron antes de agrupar y
solo se incluyen los departamentos con al menos 30 casos. El clustering siempre usa los datos completos.
"""

DENDRO_DESPUES = """
La altura de cada unión indica qué tan distintos son los grupos que se juntan: mientras más arriba se
unen, más se diferencian. Arequipa, Apurímac, Moquegua, Huancavelica y Tacna quedaron fuera por tener
menos de 30 casos o ninguno.

Con tres grupos, el Grupo 1 está formado por Piura, Lima, Lambayeque, Áncash y La Libertad, y es el más
compacto. El Grupo 2 reúne a diez departamentos de la selva y la selva central, junto con Tumbes. El
Grupo 3 junta a Puno, Ayacucho, Cusco, Callao e Ica. Los grupos 1 y 3 se unen primero, mientras que el
Grupo 2 se une al final, lo que indica que es el que tiene el perfil más distinto.
"""

PERFIL_DESPUES = """
Con tres grupos la silueta promedio es 0.27. Este valor indica que los grupos existen, pero no están del
todo separados: algunos departamentos están cerca del límite entre dos grupos. Es un resultado esperable
con solo 20 departamentos y seis variables.

El Grupo 1 es el de mayor volumen, con un promedio de casi 112 mil casos por departamento. Sus brotes
llegan antes que en el resto (semana mediana 17, fines de abril). En el Grupo 2 lo que más pesa es la
persistencia: sus departamentos registran casos en el 98 % de los años. Es también el grupo con más casos
graves o con signos de alarma (15 %) y con más casos en menores de 18 años (35 %), y sus brotes llegan más
tarde, alrededor de fines de mayo. Una posible razón de que haya más niños con dengue es que, donde el
virus circula todos los años, las personas se contagian desde más jóvenes. El Grupo 3 es lo opuesto:
tiene casos solo en el 43 % de los años, el menor promedio de casos y el menor porcentaje de casos con
signos de alarma (6 %).
"""

MAPA_GRUPOS_DESPUES = """
En el mapa los grupos forman tres franjas bastante claras: la costa norte y centro, la selva con los
departamentos andinos que bajan hacia ella, y el sur. Aunque el clustering no usó la ubicación de los
departamentos, los grupos coinciden con regiones geográficas, lo que sugiere que el clima y el territorio
influyen en cómo se presenta el dengue.
"""

DISPERSION_DESPUES = """
Los puntos del Grupo 2 están casi todos arriba, en el 100 % de años con casos, aunque su número de casos
va de unos 4 mil a más de 100 mil. Los del Grupo 3 quedan abajo, con casos en menos del 65 % de los años.

Dos departamentos se salen del patrón de su grupo. Lima tiene más de 100 mil casos, pero solo en el 77 %
de los años, porque el dengue no siempre estuvo presente en la capital. Ica tiene cerca de 60 mil casos,
pero en menos de la mitad de los años, lo que indica que casi todos sus casos vinieron de pocos brotes
grandes.
"""

CONCLUSIONES_DENGUE = """
- Entre 2000 y 2025 se notificaron {total} casos de dengue. La enfermedad no creció de forma pareja, sino
  por brotes que duran pocas semanas. Los dos más grandes fueron los de 2023 y 2024.
- El dengue es estacional: los casos se concentran entre febrero y mayo. Aun así, la época del brote
  puede moverse de un año a otro, como pasó entre 2023 y 2024.
- Los casos se concentran en la costa norte y en la selva. Piura, Lima y Loreto suman el {pct_top3}% del
  total. Huancavelica y Tacna no registran casos.
- La mayoría de los casos son leves y el dengue grave no pasa del 2 % en ningún año. Los adultos de 18 a
  59 años concentran la mayor parte de los casos, y desde los 18 años hay más mujeres que hombres.
- El clustering separó tres perfiles: la costa norte, con muchos casos y brotes tempranos; la selva, donde
  el dengue está presente casi todos los años y afecta más a menores de edad; y el sur, donde aparece solo
  de forma esporádica.
"""

CONCLUSIONES_HERRAMIENTA = """
- Highcharts permitió mostrar una base de más de un millón de registros sin problemas, siempre que los
  datos se agrupen antes de graficar. En esta app la data se agrupó una sola vez y se guardó en archivos
  pequeños, lo que permite publicarla y que cargue rápido.
- La interactividad ayudó a entender mejor los datos. El selector de rango permitió ver que 2023 y 2024
  fueron dos brotes distintos, el drilldown permitió pasar de departamento a provincia sin hacer otro
  gráfico, y el tooltip mostró los valores exactos sin llenar los gráficos de números.
- Streamlit agregó lo que un informe estático no tiene: filtros por año y departamento que actualizan los
  gráficos, y un control para cambiar el número de grupos del clustering.
- Las limitaciones son las mismas que en highcharter: Highcharts solo es gratis para uso no comercial, y
  las opciones se escriben como estructuras anidadas, lo que hace el código más largo.
"""

REFERENCIAS = """
- CDC Perú – MINSA. *Vigilancia Epidemiológica de dengue*. Plataforma Nacional de Datos Abiertos.
  https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-dengue
- Highsoft. *Highcharts documentation*. https://www.highcharts.com/docs/
- Kunst, J. (2022). *highcharter: A Wrapper for the 'Highcharts' Library*. https://jkunst.com/highcharter/
- Munayco, C. V., Valderrama Rosales, B. Y., Mateo Lizarbe, S. Y., et al. (2024). Notas desde el campo:
  brote de dengue, Perú, 2023. *MMWR Morbidity and Mortality Weekly Report, 73*.
  https://www.cdc.gov/mmwr/volumes/73/wr/mm7304a4_ensp.htm
- Organización Mundial de la Salud. (2009). *Dengue: guías para el diagnóstico, tratamiento, prevención y
  control*.
- Organización Panamericana de la Salud. (s.f.). *Conociendo a los mosquitos*.
  https://www.paho.org/sites/default/files/2026/05/conociendo-mosquitosdocx.pdf
"""

# ---------------------------------------------------------------------------
# Glosario: (término, tema, definición, dónde se ve en la app)
# ---------------------------------------------------------------------------
GLOSARIO_INTRO = """
Estas son las palabras que aparecen en la app. Puedes buscar un término o filtrar por tema.
"""

GLOSARIO = [
    # Enfermedad
    ("Dengue", "Enfermedad",
     "Infección causada por un virus que se transmite por la picadura del zancudo Aedes aegypti. "
     "Hay cuatro tipos del virus (DENV-1 a DENV-4), por eso una persona puede tener dengue más de una vez.",
     "Es el tema de toda la app."),
    ("Aedes aegypti", "Enfermedad",
     "Zancudo que transmite el dengue. Vive dentro y alrededor de las viviendas y se reproduce en recipientes "
     "con agua, como baldes, tanques, llantas o floreros. Solo pican las hembras.",
     "Ayuda a explicar por qué hay más casos en zonas cálidas y húmedas."),
    ("Dengue sin signos de alarma", "Enfermedad",
     "Caso con fiebre y molestias como dolor de cabeza, dolor detrás de los ojos, dolor muscular o "
     "sarpullido, pero sin señales de que la persona pueda empeorar.",
     "Es la mayoría de los casos en el gráfico de gravedad."),
    ("Signos de alarma", "Enfermedad",
     "Señales de que el dengue puede volverse grave, por ejemplo dolor abdominal fuerte, vómitos que no "
     "paran o sangrado de encías. Un caso con estos signos necesita atención médica cercana.",
     "Pestaña Población, gráfico de gravedad."),
    ("Dengue grave", "Enfermedad",
     "Forma más peligrosa del dengue. Incluye choque por pérdida de líquido de los vasos sanguíneos, "
     "sangrado grave o daño grave de órganos.",
     "Es menos del 2 % de los casos cada año."),
    # Vigilancia
    ("Vigilancia epidemiológica", "Vigilancia",
     "Recojo continuo de información sobre una enfermedad para saber cuántos casos hay, dónde y cuándo, "
     "y así tomar decisiones de prevención y control.",
     "Es el origen de la base de datos de la app."),
    ("Notificación", "Vigilancia",
     "Reporte de un caso que hace un establecimiento de salud al sistema de vigilancia. La base cuenta "
     "casos notificados, que no siempre son todos los casos reales.",
     "Todos los conteos de la app son casos notificados."),
    ("RENACE", "Vigilancia",
     "Red Nacional de Epidemiología. Reúne a los establecimientos de salud que reportan los casos al "
     "CDC Perú cada semana.",
     "Pestaña Datos."),
    ("Caso confirmado", "Vigilancia",
     "Caso con una prueba de laboratorio positiva para dengue.",
     "Gráfico de tipo de diagnóstico."),
    ("Caso probable", "Vigilancia",
     "Persona con síntomas de dengue que vive o estuvo en una zona con transmisión, pero sin "
     "confirmación de laboratorio.",
     "Gráfico de tipo de diagnóstico."),
    ("Brote", "Vigilancia",
     "Aumento de casos en un lugar y un periodo limitados, por encima de lo que se esperaría.",
     "Los picos de la serie semanal son brotes."),
    ("Epidemia", "Vigilancia",
     "Brote que alcanza muchos casos o se extiende a varias zonas del país. En el Perú, 2023 y 2024 "
     "fueron años de epidemia.",
     "Pestaña Tiempo."),
    ("Endémico", "Vigilancia",
     "Se dice de una enfermedad que está presente de forma constante en una zona, año tras año.",
     "El Grupo 2 del clustering, con casos casi todos los años."),
    ("Estacionalidad", "Vigilancia",
     "Patrón que se repite en la misma época de cada año. En el Perú los casos de dengue se concentran "
     "entre febrero y mayo.",
     "Mapa de calor año × semana."),
    ("Incidencia", "Vigilancia",
     "Número de casos nuevos en una población durante un periodo. Se suele expresar por cada 100 mil "
     "habitantes para comparar lugares con distinta población.",
     "La app muestra casos, no incidencia; por eso Lima aparece tan arriba."),
    # Datos
    ("Semana epidemiológica", "Datos",
     "Forma de dividir el año en 52 o 53 semanas para reportar casos. Cada semana va de domingo a sábado "
     "y permite comparar el mismo periodo entre años.",
     "Serie semanal y mapa de calor."),
    ("Lugar probable de infección", "Datos",
     "Lugar donde se cree que la persona se contagió. No siempre coincide con donde vive o donde la "
     "atendieron.",
     "Mapa por departamento y drilldown."),
    ("CIE-10", "Datos",
     "Clasificación Internacional de Enfermedades, décima revisión. Da un código a cada diagnóstico; "
     "en el dengue se usan A97.0, A97.1 y A97.2 según la gravedad.",
     "Variable diagnostic de la base."),
    ("Ubigeo", "Datos",
     "Código del INEI que identifica cada departamento, provincia y distrito del Perú.",
     "Variable ubigeo de la base."),
    ("Datos provisionales", "Datos",
     "Datos que todavía pueden cambiar porque se siguen revisando o se agregan casos notificados tarde.",
     "Aviso del CDC sobre la base."),
    ("Ciclón Yaku", "Datos",
     "Ciclón que a inicios de marzo de 2023 trajo lluvias extremas a la costa norte del Perú, sobre todo a "
     "Piura, Lambayeque y La Libertad (Munayco et al., 2024).",
     "Contexto del brote de 2023, en la pestaña Tiempo."),
    # Visualización
    ("Highcharts", "Visualización",
     "Librería de JavaScript para hacer gráficos interactivos en el navegador. En R se usa con el paquete "
     "highcharter y en esta app se usa desde Python.",
     "Todos los gráficos de la app."),
    ("Tooltip", "Visualización",
     "Cuadro que aparece al pasar el mouse sobre un punto del gráfico y muestra su valor exacto.",
     "Todos los gráficos."),
    ("Drilldown", "Visualización",
     "Opción que permite hacer clic en un dato para ver su detalle en un nivel más bajo, por ejemplo de "
     "departamento a provincia.",
     "Pestaña Territorio."),
    ("Selector de rango", "Visualización",
     "Botones y barra que permiten elegir qué periodo de una serie de tiempo se muestra.",
     "Serie semanal."),
    ("Mapa de calor", "Visualización",
     "Gráfico de celdas donde el color indica el valor. Sirve para ver patrones en dos dimensiones, como "
     "año y semana.",
     "Pestaña Tiempo."),
    ("Mapa coroplético", "Visualización",
     "Mapa en el que cada zona se pinta según el valor de una variable.",
     "Mapa de casos y mapa de grupos."),
    ("Escala logarítmica", "Visualización",
     "Escala en la que cada paso multiplica el valor (por ejemplo, 1 mil, 10 mil, 100 mil). Permite ver "
     "juntos valores muy pequeños y muy grandes.",
     "Mapa de casos y gráfico de dispersión."),
    # Estadística
    ("Clustering jerárquico", "Estadística",
     "Método que agrupa elementos parecidos uniéndolos paso a paso, empezando por los más similares.",
     "Pestaña Clustering."),
    ("Método de Ward", "Estadística",
     "Forma de decidir qué grupos unir en el clustering jerárquico: en cada paso une los dos grupos que "
     "menos aumentan la variación dentro de los grupos.",
     "Dendrograma."),
    ("Dendrograma", "Estadística",
     "Diagrama en forma de árbol que muestra cómo se fueron uniendo los grupos. Mientras más arriba se "
     "unen dos ramas, más distintas son.",
     "Pestaña Clustering."),
    ("Coeficiente de silueta", "Estadística",
     "Indicador de qué tan bien separados están los grupos. Va de -1 a 1; mientras más cerca de 1, mejor "
     "definidos están.",
     "Pestaña Clustering, sobre la tabla de perfiles."),
    ("Estandarización", "Estadística",
     "Transformar cada variable para que tenga media 0 y desviación estándar 1. Así ninguna pesa más solo "
     "por estar en una escala mayor.",
     "Paso previo al clustering."),
    ("Mediana", "Estadística",
     "Valor que queda en el medio cuando los datos se ordenan. La mitad de los datos está por debajo y la "
     "otra mitad por encima.",
     "Semana mediana de los brotes en el clustering."),
]
