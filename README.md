# Sequence Inpainter
![Result](https://github.com/SmolFalcon/Boastful/assets/19425531/c81568e8-0f5e-467d-9440-5c70185a4ede)

Desarrollado para un proyecto personal, este programa utiliza *lama-cleaner*[^1], una implementación de *Resolution-robust Large Mask Inpainting with Fourier Convolutions*[^2] para resolver errores de renderizado en una secuencia de imágenes a través de una interfaz sencilla que automatiza el proceso de corregir todas las imágenes de una animación.




## Proceso
Esta herramienta fue creada como una posible solución a las inconsistencias de un sistema de plumas (Ahora obsoleto) al interactuar con simulaciones de ropa. El sistema de plumas utilizaba máscaras en espacio de pantalla para determinar qué plumas debían esconderse (Aquellas que estuvieran debajo de polígonos de tela), 
sin embargo, este sistema presentaba inconsistencias que llevaban a errores difíciles de predecir antes del renderizado (Plumas o fragmentos errantes).

La aplicación utiliza operaciones de procesamiento de imágenes para generar una máscara de las plumas errantes, para esto utiliza información generada por el motor de render y el sistema de plumas:
- Feather AOV: Una máscara de toda la geometría de las plumas visibles en render.
- TWMasked: máscara de la región en la que, en principio, deberían permitirse plumas. Generado por el sistema de plumas.
- TWOccluder: Rasterización de aquellos objetos que deben ocultar plumas (La ropa). Generado por el sistema de plumas.

![MaskProcessing](https://github.com/SmolFalcon/Boastful/assets/19425531/1e78e422-0ee7-4898-9435-92b2b0e62b80)

Una vez generadas las máscaras que localizan las plumas errantes, puede ejecutarse el inpainting, que corregirá el render eliminando los artefactos no deseados.

![Inpaint](https://github.com/SmolFalcon/Boastful/assets/19425531/70f9925d-97ca-4d21-8603-6ba909882ac6)

## Resultado
![Result](https://github.com/SmolFalcon/Boastful/assets/19425531/c81568e8-0f5e-467d-9440-5c70185a4ede)

## Referencias
[^2]: Suvorov, Roman and Logacheva, Elizaveta and Mashikhin, Anton and Remizova, Anastasia and Ashukha, Arsenii and Silvestrov, Aleksei and Kong, Naejin and Goka, Harshith and Park, Kiwoong and Lempitsky, Victor. 2021. Resolution-robust Large Mask Inpainting with Fourier Convolutions. arXiv preprint arXiv:2109.07161. https://github.com/advimman/lama 
[^1]: Sanster. 2022. Lama-Cleaner. https://github.com/Sanster/lama-cleaner
