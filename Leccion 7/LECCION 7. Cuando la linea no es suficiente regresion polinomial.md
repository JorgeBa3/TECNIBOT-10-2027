LECCIÓN 7. Cuando la línea no es suficiente: regresión polinomial

INTRODUCCIÓN

Hoy aprenderás que no todos los fenómenos naturales se comportan en línea recta, y necesitas entrenar modelos más sofisticados que capturen curvas y cambios acelerados para hacer predicciones realistas. En la lección anterior usaste regresión lineal, que dibuja una línea recta a través de tus datos. Funciona bien cuando algo cambia de forma constante, pero ¿qué sucede cuando la temperatura sube lentamente al principio y luego rápidamente? Una curva te permite capturar esos comportamientos más complejos. Además, hoy revisarás una técnica de limpieza más avanzada: no solo eliminarás valores nulos, sino también valores atípicos u outliers que no tienen sentido en el contexto de lo que mides. Todo esto —recolección, limpieza, entrenamiento y predicción— corre dentro de tu ESP32 con MicroPython, sin pandas ni numpy: las sumatorias de la regresión y la eliminación gaussiana las escribes tú. Comprenderás cómo esta práctica contribuye al **ODS 4: Educación de calidad** y al **ODS 9: Industria, innovación e infraestructura**, ya que los modelos polinomiales son fundamentales en ingeniería, desde predicción de consumo de energía hasta diseño de sistemas de control en fábricas.

PUNTO DE PARTIDA

¿Por qué un cambio que acelera o desacelera no puede ser representado bien por una línea recta?

CONCEPTOS IMPORTANTES

**Regresión polinomial:** Es un modelo que ajusta una curva (no una línea) a través de tus datos. En lugar de usar solo `temperatura = m × tiempo + b`, usa un término de mayor grado: `temperatura = a + b × tiempo + c × tiempo²`. El término al cuadrado es lo que crea la curvatura.

**Grado del polinomio:** Es el exponente más alto de la ecuación. Un polinomio de grado 1 es la línea recta que usaste en la lección 6. El de grado 2, el de hoy, es una parábola: más flexible, pero también más riesgo de que simplemente siga el ruido de los datos en vez del patrón real.

**Outliers o valores atípicos:** Son mediciones muy alejadas del rango esperado. Si mides una temperatura de casa y esperas entre 0°C y 50°C, una lectura de 90°C o negativa es claramente un error del sensor (o, en esta práctica, del potenciómetro llevado a propósito al tope). Deben descartarse antes de entrenar, o el modelo aprende del error en vez del fenómeno real.

**Sistema de ecuaciones normales:** Ajustar la parábola a mano no es adivinar `a`, `b` y `c`: es resolver un sistema de 3 ecuaciones (las sumatorias de tiempo, tiempo al cuadrado, etc. contra la temperatura) por eliminación gaussiana, el mismo método que usarías con lápiz y papel, escrito en MicroPython.

**Flujo de trabajo completo:** Es la secuencia recolectar → limpiar (outliers) → entrenar → predecir → visualizar. Cada paso depende del anterior: un error en la limpieza arruina todo lo que viene después, por eso `limpieza.py` guarda un archivo limpio aparte antes de que `RegresionPolinomial.py` entrene con él.

DATO STEAM

¿Sabías que los sistemas de predicción de demanda de energía en ciudades inteligentes usan regresión polinomial? La demanda no sube linealmente a lo largo del día: sube suave por la mañana, acelera a mediodía por el aire acondicionado, baja por la tarde y sube otra vez al atardecer. Una curva polinomial captura esa aceleración y desaceleración, permitiendo que la red eléctrica prepare exactamente la energía que necesita en cada momento, evitando apagones y desperdicio.
