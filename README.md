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

![1](https://github.com/user-attachments/assets/2ab4462d-e271-42d5-a320-e4d74d3865ce)

![2](https://github.com/user-attachments/assets/4d7b9ef4-2338-4150-aa28-cbd596d81859)

![3](https://github.com/user-attachments/assets/11a2a47e-a6ee-4723-ae36-69e0ac28a709)

![4](https://github.com/user-attachments/assets/74620462-e87f-4f89-9223-f36b4d4f5e90)

![5](https://github.com/user-attachments/assets/01f13354-7ca4-42d9-b317-f6936c3740df)

![6](https://github.com/user-attachments/assets/736ff149-0429-4952-8507-90954cc05dd0)

![7](https://github.com/user-attachments/assets/397edb0d-a82e-4f7b-b473-6970bfdbde09)

![8](https://github.com/user-attachments/assets/a5b76669-3bcb-4244-a777-abaa407cebc3)

![9](https://github.com/user-attachments/assets/8890d971-9461-4e8e-bfb5-0ece5b10478b)

![10](https://github.com/user-attachments/assets/4e4c1ea7-386a-4cb7-ba16-0d885ddcfb68)

![11](https://github.com/user-attachments/assets/afb8eb64-0134-4f7b-b854-e13cbe480f01)


<h1 align="center"></h1>

> [!CAUTION]
> Cualquier uso indebido de este software será de exclusiva responsabilidad del usuario final, y no del autor. Este proyecto tiene como objetivo inicial demostrar las capacidades de Python como herramienta para el desarrollo de malware en entornos controlados. 

<h1 align="center"></h1>

#### Developer: ~R3LI4NT~
