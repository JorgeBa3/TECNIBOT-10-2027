LECCIÓN 8. Clustering y clasificación en tu SmartHouse

INTRODUCCIÓN

Hoy aprenderás a **descubrir automáticamente patrones ocultos en los datos que recolectas de tu hogar, agrupándolos en categorías sin que tengas que decirle al modelo cuáles son esas categorías**. Hasta ahora has entrenado modelos que ya sabían exactamente qué buscaban: predice temperatura, detecta luz, limpia outliers. Pero ¿qué sucede cuando quieres que la máquina descubra por sí sola que tu casa tiene tres “modos” distintos? Por las mañanas hay mucha luz, la casa está activa y la temperatura sube; por las tardes todo es más tranquilo; por la noche se oscurece y enfría. Un algoritmo de clustering (agrupación) llamado K-means puede descubrir esos patrones sin que tú le pongas etiquetas. Es como si mirara tus lecturas de temperatura y luz y dijera: “estos puntos se parecen entre sí, aquellos forman otro grupo, y aquellos un tercero.” Después tú interpretas: Modo Activo, Modo Relajado, Modo Dormido. Con esa lectura nueva, la casa decide sola: si está Dormido, apaga luces; si está Activo, las enciende. Comprenderás cómo esta práctica contribuye al **ODS 7: Energía asequible y no contaminante**, al **ODS 9: Industria, innovación e infraestructura** y al **ODS 12: Producción y consumo responsables**, porque un hogar que se adapta a sus propios patrones gasta menos energía y no necesita que alguien programe cada horario a mano.

PUNTO DE PARTIDA

¿Cómo diseñamos una casa que no solo funcione, sino que aprenda, se adapte y optimice sus recursos automáticamente?

CONCEPTOS IMPORTANTES

**Clustering (Agrupación):** Es una técnica de aprendizaje no supervisado que junta puntos parecidos sin que nadie le haya dicho antes cuáles son las categorías. En la práctica tus puntos son pares (temperatura, luz). El modelo no recibe “esto es de noche”; solo ve números.

**K-means:** Es el algoritmo de clustering más usado en clase y en la industria. Tú le dices “busca K = 3 grupos”. Coloca 3 centros, acerca cada dato al centro más cercano, recalcula los centros con el promedio del grupo, y repite. Cuando los centros dejan de moverse, ya tienes 3 clusters.

**Aprendizaje no supervisado:** El modelo aprende sin etiquetas correcto/incorrecto. En la lección 6 tú sí tenías supervisor: “a los 10 s hay 25 °C”. En K-means no hay supervisor: solo similitud.

**Centroide:** Es el punto del medio de cada grupo. Cada medición nueva se compara con los 3 centroides; gana el más cercano. Eso es “¿en qué modo está la casa ahora?”.

**Interpretación de clusters:** El paso humano. K-means no sabe que un grupo se llama Dormido. Tú miras los centroides: poca luz y temperatura baja → noche; mucha luz y calor → casa activa. En la práctica el programa te ayuda ordenando por luz, pero la historia la pones tú.

**Decisiones basadas en clusters:** Ya con nombres, una lectura nueva enciende las luces de la casa: DÍA → LED verde; TARDE → LED amarillo; NOCHE → LED rojo. Si temperatura y luz están las dos muy altas, no es un horario: es una emergencia. Suena el buzzer y las tres LEDs se encienden en secuencia, como el camino de salida. Así el clustering deja de ser una lista de números y pasa a ser el cerebro de la SmartHouse.

DATO STEAM

¿Sabías que Spotify usa K-means (y variantes) para agrupar canciones y usuarios con gustos parecidos? No le dicen “esto es rock”: descubren que millones de personas escuchan combinaciones similares y te recomiendan lo que esos grupos también oyeron. Netflix hace lo mismo con películas y Amazon con productos. En casas y edificios inteligentes, K-means agrupa horas del día según temperatura, luz y ocupación para apagar lo que no se usa. Es rápido, cabe en la ESP32 del aula y de verdad se usa en la industria.
