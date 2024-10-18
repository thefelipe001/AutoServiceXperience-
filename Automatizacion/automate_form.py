from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys  
import csv

import tkinter as tk

import time
import sys  
from tkinter import messagebox
import time


def agregar():
    try:
        # Inicializar el driver de Selenium
        chrome_driver_path = r"C:\Users\Dell\Desktop\chromedriver.exe"
        service = Service(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=service)

        # Navegar a la URL donde se encuentra el botón
        driver.get("http://127.0.0.1:5000/")
        driver.maximize_window()
        time.sleep(2)  # Esperar que la página cargue

        # Abrir el archivo Estudiante.txt y leer todas las líneas
        with open("CrearEstudiante.txt", "r") as archivo:
            estudiantes = archivo.readlines()

        # Procesar cada estudiante
        for linea in estudiantes:

            nombre, apellido, correo, telefono, fecha, direccion, ciudad, codigo_postal, carrera, semestre, promedio = linea.strip().split(",")

            # Hacer clic en el botón "Agregar Estudiante"
            driver.find_element(By.CSS_SELECTOR, "button.btn-outline-primary").click()
            time.sleep(2)  # Esperar que el modal se abra

            # Llenar el formulario del estudiante
            driver.find_element(By.ID, "nombre").send_keys(nombre)
            driver.find_element(By.ID, "apellido").send_keys(apellido)
            driver.find_element(By.ID, "correo").send_keys(correo)
            driver.find_element(By.ID, "celular").send_keys(telefono)
            driver.find_element(By.ID, "fecha").send_keys(fecha)
            driver.find_element(By.ID, "direccion").send_keys(direccion)
            driver.find_element(By.ID, "ciudad").send_keys(ciudad)
            driver.find_element(By.ID, "codigoPostal").send_keys(codigo_postal)
            driver.find_element(By.ID, "carrera").send_keys(carrera)
            driver.find_element(By.ID, "semestre").send_keys(semestre)
            driver.find_element(By.ID, "promedio").send_keys(promedio)

            # Enviar el formulario
            driver.switch_to.active_element.send_keys(Keys.TAB)
            driver.switch_to.active_element.send_keys(Keys.TAB)
            driver.switch_to.active_element.send_keys(Keys.ENTER)

            # Esperar que aparezca el botón "OK" del modal de confirmación y hacer clic
            time.sleep(3)  # Esperar que el mensaje de éxito aparezca
            boton_ok = driver.find_element(By.CSS_SELECTOR, "button.swal2-confirm")
            boton_ok.click()

            # Esperar un momento antes de registrar el siguiente estudiante
            time.sleep(2)

    except FileNotFoundError:
        # Manejar el error si el archivo no se encuentra
        messagebox.showerror("Error", "El archivo Estudiante.txt no se encontró.")
    except Exception as e:
        # Manejar cualquier otro error
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    finally:
        # Asegurarse de cerrar el navegador al finalizar
        driver.quit()


# Función para la opción de Eliminar
def eliminar():
    try:

        chrome_driver_path = r"C:\Users\Dell\Desktop\chromedriver.exe"
        service = Service(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=service)

        driver.get("http://127.0.0.1:5000/")
        driver.maximize_window()
        time.sleep(2) 

        with open("EliminarEstudiante.txt", "r") as archivo:
            estudiantes = archivo.readlines()

        for linea in estudiantes:
            id = linea.strip().split(",")

            # Buscar al estudiante ingresando su ID en el campo de búsqueda
            search_field = driver.find_element(By.ID, "searchByID")
            search_field.clear()  
            search_field.send_keys(id)
            botones = driver.find_elements(By.CSS_SELECTOR, "a.btn-delete")
            if botones:
               botones[0].click()
               boton_confirmar = driver.find_element(By.CSS_SELECTOR, "button.swal2-confirm")
               boton_confirmar.click()
               time.sleep(1)  
               boton_confirmar = driver.find_element(By.CSS_SELECTOR, "button.swal2-confirm")
               boton_confirmar.click()
               time.sleep(2) 
    except FileNotFoundError:
        # Manejar el error si el archivo no se encuentra
        messagebox.showerror("Error", "El archivo Estudiante.txt no se encontró.")
    except Exception as e:
        # Manejar cualquier otro error
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    finally:
        # Asegurarse de cerrar el navegador al finalizar
        driver.quit()






def editar():
    try:
        # Ruta al chromedriver
        chrome_driver_path = r"C:\Users\Dell\Desktop\chromedriver.exe"
        service = Service(executable_path=chrome_driver_path)
        driver = webdriver.Chrome(service=service)

        # Navegar a la página web
        driver.get("http://127.0.0.1:5000/")
        driver.maximize_window()
        time.sleep(2)

        # Leer el archivo CSV de estudiantes
        with open("ActualizarEstudiante.txt", "r") as archivo:
            lector_csv = csv.reader(archivo)

            for linea in lector_csv:

                if len(linea) != 12:
                    messagebox.showerror("Error", f"La línea no tiene 12 campos: {','.join(linea)}")
                    continue 

                (id, nombre, apellido, correo, telefono, fecha, direccion,
                 ciudad, codigo_postal, carrera, semestre, promedio) = linea

                # Buscar al estudiante ingresando su ID en el campo de búsqueda
                search_field = driver.find_element(By.ID, "searchByID")
                search_field.clear()  
                search_field.send_keys(id)
                botones = driver.find_elements(By.CSS_SELECTOR, "a.btn-editar")
                if botones:
                   botones[0].click()
                   time.sleep(2)
                   driver.switch_to.active_element.send_keys(Keys.TAB)
                   driver.switch_to.active_element.send_keys(Keys.TAB)
                   driver.switch_to.active_element.send_keys(nombre)
                   driver.switch_to.active_element.send_keys(Keys.TAB)
                   driver.switch_to.active_element.send_keys(apellido)
                   driver.switch_to.active_element.send_keys(Keys.TAB)
                   driver.switch_to.active_element.send_keys(correo)
                   driver.switch_to.active_element.send_keys(Keys.TAB)
                   driver.switch_to.active_element.send_keys(telefono)
                   driver.switch_to.active_element.send_keys(Keys.TAB)
                   driver.switch_to.active_element.send_keys(direccion)
                   driver.switch_to.active_element.send_keys(Keys.TAB)
                   driver.switch_to.active_element.send_keys(codigo_postal)
                   driver.switch_to.active_element.send_keys(Keys.TAB)
                   driver.switch_to.active_element.send_keys(carrera)
                   driver.switch_to.active_element.send_keys(Keys.TAB)
                   driver.switch_to.active_element.send_keys(semestre)
                   driver.switch_to.active_element.send_keys(Keys.TAB)
                   driver.switch_to.active_element.send_keys(promedio)
                   driver.switch_to.active_element.send_keys(Keys.TAB)
                   time.sleep(2)  
                   driver.switch_to.active_element.send_keys(Keys.TAB)
                   driver.switch_to.active_element.send_keys(Keys.TAB)
                   driver.switch_to.active_element.send_keys(Keys.TAB)
                   driver.switch_to.active_element.send_keys(Keys.TAB)
                   driver.switch_to.active_element.send_keys(Keys.ENTER)
                   time.sleep(2)  
                   boton_ok = driver.find_element(By.CSS_SELECTOR, "button.swal2-confirm")
                   boton_ok.click()

                   time.sleep(2)
 
    except FileNotFoundError:
        # Manejar el error si el archivo no se encuentra
        messagebox.showerror("Error", "El archivo 'ActualizarEstudiante.txt' no se encontró.")

    except Exception as e:
        # Manejar cualquier otro error
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    finally:
        # Asegurarse de cerrar el navegador al finalizar
        driver.quit()



















def cerrar():
    respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas cerrar el programa?")
    if respuesta:
        ventana.destroy()  # Cerrar la ventana de Tkinter
        sys.exit()  # Finalizar el proceso del script    


# Crear la ventana principal con un color de fondo y un tamaño mejorado
ventana = tk.Tk()
ventana.title("Menú Principal - Automatización")
ventana.geometry("500x400")
ventana.configure(bg="#f0f0f0")

# Etiqueta de bienvenida con una fuente más grande y centrada
titulo = tk.Label(
    ventana, 
    text="Selecciona una opción", 
    font=("Arial", 20, "bold"), 
    bg="#f0f0f0", 
    fg="#333"
)
titulo.pack(pady=20)

# Estilo uniforme para los botones
boton_style = {
    "width": 20, 
    "height": 2, 
    "font": ("Arial", 14), 
    "bg": "#4CAF50", 
    "fg": "white", 
    "activebackground": "#45a049"
}

# Crear botones del menú con estilo
boton_agregar = tk.Button(ventana, text="Agregar", command=agregar, **boton_style)
boton_agregar.pack(pady=10)

boton_eliminar = tk.Button(ventana, text="Eliminar", command=eliminar, **boton_style)
boton_eliminar.pack(pady=10)

boton_editar = tk.Button(ventana, text="Editar", command=editar, **boton_style)
boton_editar.pack(pady=10)

boton_cerrar = tk.Button(ventana, text="Cerrar la Aplicacion", command=cerrar, **boton_style)
boton_cerrar.pack(pady=10)

# Iniciar la ventana principal
ventana.mainloop()