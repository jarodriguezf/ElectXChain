<h1 align='center'>Elect X Chain</h1>

![ElecxChain_github](https://github.com/user-attachments/assets/ff6b764c-b94e-4f3c-bfb2-f8cf1ce5f2c2)


*El proposito de este proyecto es realizar un sistema de votacion online. 
La idea de realizar dicho proyecto es la mejora y aprendizaje de nuevas areas en el procesamiento en streaming y tecnologías emergentes como blockchain.
Todo se ha realizado con objetivos didacticos, por tanto, no estamos ante un sistema profesional, ni tampoco con objetivos comerciales.*

##  Estructura del proyecto  📁
![root](https://github.com/user-attachments/assets/04c720cf-fbef-4574-87b0-aca33e386808)

*Algunos archivos tanto de configuración como de desarrollo no se han subido dada la sensibilidad de sus datos, ejemplo: archivo de desencriptación, archivos de configuración, etc*
- api: Contiene la api para interactuar con los datos y el front, así como scripts de encriptacion varios.
- blockchain: Contiene lo relacionado con el servicio hardhat (servicio de blockchain local), el contrato inteligente (contract), el desplegable (deploy) y scripts para interactuar con el contrato (guardar y extraer informacion).
- diagrams-uml: Contiene tres diagramas mostrando el diseño de flujo de datos con sus servicios y tecnologías. Hace referencia a las tres fases del proyecto desarrolladas; Register_Autentication (fase de registro y autenticacion completa), voting (fase de votado y envio de datos a kafka encriptado) y process_vote (manejo de los datos en diferentes servicios como spark, blockchain, redis y powerbi).
- kafka: Contiene la configuracion inicial y los productores.
- powerbi: Contiene el dashboard donde podemos monitorizar constantemente el conteo de votos a cada opcion, así como visualizar varias estadisticas mas.
- spark: Contiene lo relacionado a los scripts de spark streaming, sus funciones y conexiones a db tambien están aquí, así como el archivo de desencriptación. 
- venv: Entorno virtual.
- .env: Secretos.
- .gitignore
- custom.cnf: archivo de configuracion para el servicio de db (mariadb), configura el tiempo y hora de la zona local.
- docker-compose.yml: Contiene los servicios del proyecto con sus respectivas configuraciones, variables y conexiones.
- system_keys.py: archivo para generar las variables publicas y privadas del sistema.
- system_private_key/pub_key: claves generadas del sistema en formato PEM.

## Dataset 📄

Los datos usados en este proyecto han sido todos ficticios, tanto dnis, nombres, como telefonos. Cualquier parecido a la realidad es mera coincidencia.

## Tecnologias usadas 💻

- Python (FastAPI)
- Spark Streaming
- Kafka
- Lenguajes web (html, css, javascript)
- Gestores de DB (mariaDB, Redis)
- Hardhat (blockchain)
- PowerBI

## Funcionamiento de la aplicación 🚀

1. Registro:
   - El usuario accede a la pagina de registro.
   - Ingresa sus datos.
   - Envia sus datos.
     
   *En todo este proceso se producen controles de excepciones, garantizando la integridad de los datos almacenados*

![register](https://github.com/user-attachments/assets/b85429de-7126-4fc9-b544-7326cc1bc429)

2. Autenticacion:
   - El usuario ingresa su dni y el numero de telefono con el que se registró conteriormente.
   - Envía su peticion de ser autenticado.
     
   *En todo el proceso se garantiza que el usuario sea verídico, activando un campo para controlar los usuarios autenticados y los solo registrados*

![autenticate](https://github.com/user-attachments/assets/1b5833b5-c661-4c60-9093-60da6b2993bf)

3. Autentication two factor:
   - El usuario ingresa el codigo enviado a través de sms en su movil (en este caso se envía mediente un endpoint para simular el envío de sms).
   - Si el tiempo establecido en 2 minutos es excedido, se genera un nuevo codigo (así también podremos clickar en resend code para generar el codigo y enviarlo al sms de nuevo)
   - Envía el codigo para validar si es correcto y acceder a votar.
   
   *Controlamos que el codigo generado sea correcto manteniendo la seguridad en el proceso de autenticacion*

![2fa](https://github.com/user-attachments/assets/efc6734c-9811-4e54-bfde-01ed9d774ea6)

4. Votación:
   - El usuario selecciona la opcion dada entre los candidatos/partidos.
   - Cuando tenga la opcion seleccionada, pinchará en 'Vote' para enviar su voto al sistema, se abrirá un pop-up con esto el usuario confirmará su decision de votación.
     
   *Controlamos que el usuario no haya votado mas de una vez y que los datos se pasen al sistema encriptados*

![vote_page](https://github.com/user-attachments/assets/11772794-b523-435a-b05c-b2b9d37ffde4)

Finaliza la interacción del usuario viendo la pagina de información final.

![final_user_page](https://github.com/user-attachments/assets/b782f0dc-c732-4850-9355-6cc3cd61c9a3)

5. Proceso de encriptación del voto y desencriptacion.
   - ENCRIPTACIÓN -
   - Cuando el usuario selecciona la eleccion deseada, el voto se envía a un script ('voting', no se muestra en el repositorio remoto por seguridad) donde se realizan varios procesos:
     1. Hasheo del voto en bytes.
     2. Firma del voto con la llave privada del usuario (la llave privada del usuario viene de la db cifrada simetricamente, por tanto es necesario desencriptarla para obtener su valor original).
     3. Cifrado simetrica de la firma con el voto dado previamente (algoritmo AES), generando una clave para encriptar y desencriptar.
     4. Cifrado de la clave AES con la llave publica del sistema (asegurando que solo el sistema acceda a la clave AES y por tanto firma del usuario), cifrado con RSA.
     5. Envió de la firma cifrada tanto con RSA como AES.
   - DESENCRIPTACIÓN -
   - Cuando la firma digital llega al ultimo script de spark ('spark_counter'), validamos el tipo y contenido de la firma, si es correcto inicia el proceso de desencriptación ('process_signature', no esta subido al remoto por seguridad).
     1. Separar la clave cifrada  de la firma cifrada.
     2. Obtener la clave mediante la llave privada del sistema (obteniendo la clave AES).
     3. Con la clave desencriptamos la firma del usuario.
     4. Comparamos el contenido interno con el voto almacenado en bd (toda comparación has hash de bytes).
     5. Si es correcto, se contabiliza el voto, si no es correcto se rechaza.

![cipher_flow drawio](https://github.com/user-attachments/assets/5607a71b-6e84-49ab-9ed0-8e117a4021b6)


7. Manejo interno de los datos.
  - Base de datos relacional: Los datos del usuario se guardan en mariadb, permitiendo persistir la información. Estos datos se guardan de manera que no podemos saber que votó cada usuario, manteniendo la seguridad e integridad de voto.

*La información mas sensible como la clave privada y el voto, se almacenan por un lado (clave privada) encriptada y por otro lado (voto) hasheado*

![db](https://github.com/user-attachments/assets/9ac97604-7594-494e-ae88-e0e044612871)

  - Kafka-1: Los datos de la votación ejercido por el usuario en el punto 4, viaja a un topico de kafka (directorio: kafka, script: producer_1, topic: vote_passthrough) almacenando en el broker tanto el uuid como la firma digital encriptada.
  - Spark-1: Un script (directorio: spark, script: spark_process) consume los datos del topico, validando que los datos lleguen integros y almacenando en cache estos mismos (almacenamiento en Redis).
  - Redis: Persiste los datos en caché hasta que la blockchain notifique a Redis la llegada correcta de estos datos, entonces borra el registro.
  - Blockchain: Almacena en el nodo los datos (directorio: blockchain, archivos: contracts y scripts), permitiendo revisar las transaccciones realizadas de cada usuario (aumenta la seguridad, la integridad de voto y la inmutabilidad de los datos).
  - Kafka-2: Una vez almacenado se envía a otro topico de kafka (directorio: kafka, script: producer_2, topic: vote_result) encargado de mover la información hacia el script para desencriptar y contabilizar los votos.
  - Spark-2: Consumimos los datos del segundo topico de kafka (directorio: spark, script: spark_counter), validamos la información y desencriptamos la firma, permitiendo validar si el contenido interno es igual al hash de la firma en db para cada usuario. Si la firma es correcta el voto se persiste en una nueva tabla en la base de datos (contabilizando cada voto por separado).
  
![vote_table](https://github.com/user-attachments/assets/28e7f828-247e-41b3-9f69-ded8bb4258e3)

  - PowerBI: Conectamos a la base de datos, tanto la de los usuarios como la de votos. Extrayendo la información y realizando un dashboard para monitorizar el conteo automatico del sistema.

*Cada conteo de votos así como provincias cuyos usuarios han votado y el genero se registra para posterior analisis*
![dashboard](https://github.com/user-attachments/assets/0df1da58-0d69-472d-b0d2-601499aacdd7)

## Conclusión 🎉

Este proyecto ha sido uno de los más completos que he llevado a cabo, ya que me ha permitido profundizar en varios aspectos clave, especialmente en seguridad y gestión de almacenamiento, además de interactuar con contenedores para un despliegue eficiente.

El manejo de procesamiento en tiempo real representó un desafío importante, requiriendo un enfoque diferente en la programación, particularmente en términos de latencia y la gestión de procesos livianos. En mi caso, el último script puede considerarse un procesamiento por lotes o micro-lotes, optimizado para flujos de datos en tiempo real.

Trabajar con tecnología blockchain ha sido otra gran oportunidad de aprendizaje, ya que me ha permitido construir una DApp (aplicación descentralizada), proporcionando un nivel adicional de seguridad e integridad a cada transacción generada en el sistema.

Finalmente, el dashboard desarrollado ofrece una visualización clara y sencilla de los resultados en tiempo real, lo que facilita el monitoreo y la comprensión del comportamiento del sistema.

¡Gracias por explorar el proyecto!
