import mimetypes
import tkinter
from flask import Flask,  render_template, request, redirect, url_for, session, Response # pip install Flask
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb
from os import path #pip install notify-py
from notifypy import Notify
from tkinter import *
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np
from twilio.rest import Client
import imutils
from xmlrpc.client import boolean
from tkinter import ttk

account = "AC1438004459be7b7a65289bbc37487091"
token = "41725217cf0c69de80a992025c85b388"
client = Client(account, token)


#import database as db


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'app_citas'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("contenido.html")   

@app.route('/herramientas')
def herramientas():
    return render_template("herramientas.html")   


@app.route('/layout', methods = ["GET", "POST"])
def layout():
    session.clear()
    return render_template("contenido.html")

comprobador = False
 

@app.route('/login', methods= ["GET", "POST"])
def login():
        
    return render_template("login.html")



@app.route('/registro', methods = ["GET", "POST"])
def registro():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tip_usu")
    tipo = cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM sexo_interes")
    interes = cur.fetchall()

    cur.close()

    notificacion = Notify()
    
    

    if request.method == 'GET':
        return render_template("registro.html", tipo = tipo, interes = interes )
    
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        tip = request.form['tipo']
        interes = request.form['interes']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password, id_tip_usu, interes) VALUES (%s,%s,%s,%s,%s)", (name, email, password,tip,interes,))
        mysql.connection.commit()
        notificacion.title = "Registro Exitoso"
        notificacion.message="ya te encuentras registrado en 🤵 MORE LOVE 👰, por favor inicia sesión y empieza a descubrir este nuevo mundo."
        notificacion.send()
        return redirect(url_for('login'))

def baseAlgoritmo():
        personName = 'DEST'
        dataPath = 'C:/Users/USER/Desktop/ESFOT 4/proyecyo3/prote/paginaWeb-proyecto/ImagenesBase'#Cambia a la ruta donde hayas almacenado Data

        personPath = dataPath + '/' + personName
        if not os.path.exists(personPath):
            print('Carpeta creada: ',personPath)
            os.makedirs(personPath)
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        #cap = cv2.VideoCapture('Video.mp4')
        faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
        count = 0
        while True:
            
            ret, frame = cap.read()
            if ret == False: break
            frame =  imutils.resize(frame, width=640)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = frame.copy()
            faces = faceClassif.detectMultiScale(gray,1.3,5)
            for (x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                rostro = auxFrame[y:y+h,x:x+w]
                rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(personPath + '/rostro_{}.jpg'.format(count),rostro)
                count = count + 1
            cv2.imshow('frame',frame)
            k =  cv2.waitKey(1)
            if k == 27 or count >= 300:
                break
        cap.release()
        cv2.destroyAllWindows()


def entrenamientoAlgoritmo():
    # Cambia a la ruta donde hayas almacenado Data
    dataPath = 'C:/Users/USER/Desktop/ESFOT 4/proyecyo3/prote/paginaWeb-proyecto/ImagenesBase'#Cambia a la ruta donde hayas almacenado Data

    peopleList = os.listdir(dataPath)
    print('Lista de personas: ', peopleList)
    labels = []
    facesData = []
    label = 0
    for nameDir in peopleList:
        personPath = dataPath + '/' + nameDir
        print('Leyendo las imágenes')
        for fileName in os.listdir(personPath):
            print('Rostros: ', nameDir + '/' + fileName)
            labels.append(label)
            facesData.append(cv2.imread(personPath+'/'+fileName, 0))
            #image = cv2.imread(personPath+'/'+fileName,0)
            # cv2.imshow('image',image)
            # cv2.waitKey(10)
        label = label + 1
    print('labels= ', labels)
    print('Número de etiquetas 0: ', np.count_nonzero(np.array(labels) == 0))
    print('Número de etiquetas 1: ', np.count_nonzero(np.array(labels) == 1))

    # Métodos para entrenar el reconocedor
    #face_recognizer = cv2.face.EigenFaceRecognizer_create()
    #face_recognizer = cv2.face.FisherFaceRecognizer_create()
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Entrenando el reconocedor de rostros
    print("Entrenando...")
    face_recognizer.train(facesData, np.array(labels))
    # Almacenando el modelo obtenido
    #face_recognizer.write('modeloEigenFace.xml')
    #face_recognizer.write('modeloFisherFace.xml')
    face_recognizer.write('modeloLBPHFace.xml')
    print("Modelo almacenado...")


def pruebaAlgoritmo():
    ##Concepto de tkinter
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    # Cambia a la ruta donde hayas almacenado Data
    dataPath = 'C:/Users/USER/Desktop/ESFOT 4/proyecyo3/prote/paginaWeb-proyecto/ImagenesBase'#Cambia a la ruta donde hayas almacenado Data

    imagePaths = os.listdir(dataPath)
    print('imagePaths=', imagePaths)

    #face_recognizer = cv2.face.EigenFaceRecognizer_create()
    #face_recognizer = cv2.face.FisherFaceRecognizer_create()
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Leyendo el modelo
    # face_recognizer.read('modeloEigenFace.xml')
    # face_recognizer.read('modeloFisherFace.xml')
    face_recognizer.read('modeloLBPHFace.xml')

    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) #Reconocimiento en striming
    #cap = cv2.VideoCapture('Video.mp4') #Reconocimiento en video

    faceClassif = cv2.CascadeClassifier(
        cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()

        faces = faceClassif.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            rostro = auxFrame[y:y+h, x:x+w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            result = face_recognizer.predict(rostro)

            cv2.putText(frame, '{}'.format(result), (x, y-5),
                        1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)

            # # EigenFaces
            # if result[1] < 5700:
            #     cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
            #     cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
            # else:
            #     cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
            #     cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)

            # # FisherFace
            # if result[1] < 500:
            #     cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
            #     cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
            # else:
            #     cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
            #     cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)

            # LBPHFace
            a=False;
            if result[1] < 70:
                cv2.putText(frame, '{}'.format(
                    imagePaths[result[0]]), (x, y-25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                #AQui va lo correcto
                ##time.sleep(10)
                ##Event().wait(10)
                a=True;
                #message = client.messages.create(to="+593939305304", from_="+12535232583", body="Inicio de Sesion Exitososssss")
                ##Label(pantalla1, text = "Registro Convencional Exitoso222222222", fg = "green", font = ("Calibri",11)).pack()
                
                
            else:
                cv2.putText(frame, 'Desconocido', (x, y-20), 2,
                            0.8, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            if a==True:
                    
                    #message = client.messages.create(to="+593939305304", from_="+12535232583", body="Inicio de Sesion Exitososssss")
                    
                    
                    root.mainloop()
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1)
        if k == 27:
            break




    cap.release()
    cv2.destroyAllWindows()








def faceId():
    
    #--------------------------------------Importamos librerias--------------------------------------------


    #------------------------ Crearemos una funcion que se encargara de registrar el usuario ---------------------
    def getEnter(screen):
        ''' Set an enter inside the screen '''
        #Label(screen, text="", bg=color_background).pack()


    def registrar_usuario():
        usuario_info = usuario.get() #Obetnemos la informacion alamcenada en usuario
        contra_info = contra.get() #Obtenemos la informacion almacenada en contra

        archivo = open(usuario_info, "w") #Abriremos la informacion en modo escritura
        archivo.write(usuario_info + "\n")   #escribimos la info
        archivo.write(contra_info)
        archivo.close()

        #Limpiaremos los text variable
        usuario_entrada.delete(0, END)
        contra_entrada.delete(0, END)

        #Ahora le diremos al usuario que su registro ha sido exitoso
        Label(pantalla1, text = "Registro Convencional Exitoso", fg = "green", font = ("Calibri",11)).pack()
        

    #--------------------------- Funcion para almacenar el registro facial --------------------------------------
        
    def registro_facial():
        #Vamos a capturar el rostro
        cap = cv2.VideoCapture(0)               #Elegimos la camara con la que vamos a hacer la deteccion
        while(True):
            ret,frame = cap.read()              #Leemos el video
            cv2.imshow('Registro Facial',frame)         #Mostramos el video en pantalla
            if cv2.waitKey(1) == 27:            #Cuando oprimamos "Escape" rompe el video
                break
        usuario_img = usuario.get()
        cv2.imwrite(usuario_img+".jpg",frame)       #Guardamos la ultima caputra del video como imagen y asignamos el nombre del usuario
        cap.release()                               #Cerramos
        cv2.destroyAllWindows()

        usuario_entrada.delete(0, END)   #Limpiamos los text variables
        contra_entrada.delete(0, END)
        Label(pantalla1, text = "Registro Facial Exitoso", fg = "green", font = ("Calibri",11)).pack()

        #----------------- Detectamos el rostro y exportamos los pixeles --------------------------
        def reg_rostro(img, lista_resultados):
            data = pyplot.imread(img)
            for i in range(len(lista_resultados)):
                x1,y1,ancho, alto = lista_resultados[i]['box']
                x2,y2 = x1 + ancho, y1 + alto
                pyplot.subplot(1, len(lista_resultados), i+1)
                pyplot.axis('off')
                cara_reg = data[y1:y2, x1:x2]
                cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) #Guardamos la imagen con un tamaño de 150x200
                cv2.imwrite(usuario_img+".jpg",cara_reg)
                #cv2.imwrite(direccion + "/"+usuario_img+".jpg",cara_reg)
                pyplot.imshow(data[y1:y2, x1:x2])
            pyplot.show()

        img = usuario_img+".jpg"
        #path = 'C:/Users/jeanp/OneDrive/Escritorio/LWRF/'
        #db.registerUser(usuario_img, path + img)
        pixeles = pyplot.imread(img)
        detector = MTCNN()
        caras = detector.detect_faces(pixeles)
        reg_rostro(img, caras)   

        
   

    #------------------------------------------- Funcion para verificar los datos ingresados al login ------------------------------------
        
    def verificacion_login():
        log_usuario = verificacion_usuario.get()
        log_contra = verificacion_contra.get()

        usuario_entrada2.delete(0, END)
        contra_entrada2.delete(0, END)

        lista_archivos = os.listdir()   #Vamos a importar la lista de archivos con la libreria os
        if log_usuario in lista_archivos:   #Comparamos los archivos con el que nos interesa
            archivo2 = open(log_usuario, "r")  #Abrimos el archivo en modo lectura
            verificacion = archivo2.read().splitlines()  #leera las lineas dentro del archivo ignorando el resto
            if log_contra in verificacion:
                print("Inicio de sesion exitoso")
                Label(pantalla2, text = "Inicio de Sesion Exitososssss", fg = "green", font = ("Calibri",11)).pack()
                message = client.messages.create(to="+593939305304", from_="+12535232583", body="Inicio de Sesion Exitososssss")
            else:
                print("Contraseña incorrecta, ingrese de nuevo")
                Label(pantalla2, text = "Contraseña Incorrecta", fg = "red", font = ("Calibri",11)).pack()
        else:
            print("Usuario no encontrado")
            Label(pantalla2, text = "Usuario no encontrado", fg = "red", font = ("Calibri",11)).pack()
        
    #--------------------------Funcion para el Login Facial --------------------------------------------------------
    def login_facial():
    #------------------------------Vamos a capturar el rostro-----------------------------------------------------
        cap = cv2.VideoCapture(0)            
        while(True):
            ret,frame = cap.read()              #Leemos el video
            cv2.imshow('Login Facial',frame)         #Mostramos el video en pantalla
            if cv2.waitKey(1) == 27:            #Cuando oprimamos "Escape" rompe el video
                break
        usuario_login = verificacion_usuario.get()    #Con esta variable vamos a guardar la foto pero con otro nombre para no sobreescribir
        cv2.imwrite(usuario_login+"LOG.jpg",frame)       #Guardamos la ultima caputra del video como imagen y asignamos el nombre del usuario
        cap.release()                               #Cerramos
        cv2.destroyAllWindows()

        usuario_entrada2.delete(0, END)   #Limpiamos los text variables
        contra_entrada2.delete(0, END)

        #----------------- Funcion para guardar el rostro --------------------------
        
        def log_rostro(img, lista_resultados):
            data = pyplot.imread(img)
            for i in range(len(lista_resultados)):
                x1,y1,ancho, alto = lista_resultados[i]['box']
                x2,y2 = x1 + ancho, y1 + alto
                pyplot.subplot(1, len(lista_resultados), i+1)
                pyplot.axis('off')
                cara_reg = data[y1:y2, x1:x2]
                cara_reg = cv2.resize(cara_reg,(150,200), interpolation = cv2.INTER_CUBIC) 
                cv2.imwrite(usuario_login+"LOG.jpg",cara_reg)
                return pyplot.imshow(data[y1:y2, x1:x2])
            pyplot.show()

        #-------------------------- Detectamos el rostro-------------------------------------------------------
        
        img = usuario_login+"LOG.jpg"
        pixeles = pyplot.imread(img)
        detector = MTCNN()
        caras = detector.detect_faces(pixeles)
        log_rostro(img, caras)

        #-------------------------- Funcion para comparar los rostros --------------------------------------------
        def orb_sim(img1,img2):
            orb = cv2.ORB_create()  
    
            kpa, descr_a = orb.detectAndCompute(img1, None)  
            kpb, descr_b = orb.detectAndCompute(img2, None)  

            comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) 

            matches = comp.match(descr_a, descr_b) 

            regiones_similares = [i for i in matches if i.distance < 70] 
            if len(matches) == 0:
                return 0
            return len(regiones_similares)/len(matches)
            
        #---------------------------- Importamos las imagenes y llamamos la funcion de comparacion ---------------------------------
        
        im_archivos = os.listdir()  
        if usuario_login+".jpg" in im_archivos:   
            rostro_reg = cv2.imread(usuario_login+".jpg",0)     
            rostro_log = cv2.imread(usuario_login+"LOG.jpg",0)
            similitud = orb_sim(rostro_reg, rostro_log)
            if similitud >= 0.98:
                Label(pantalla2, text = "Inicio de Sesion Exitoso", fg = "green", font = ("Calibri",11)).pack()
                message = client.messages.create(to="+593967165147", from_="+12535232583", body="Inicio de Sesion Exitososssss")
                global comprobador
                comprobador = True
                print("Bienvenido al sistema usuario: ",usuario_login)
                print("Compatibilidad con la foto del registro: ",similitud)
                print("Redirigiendo . . . . . : ",comprobador)
                if(comprobador == True):
                    print("ESTOY EN LA REDIRECCION DEL PERFIL")
                    return redirect(url_for("profile"))
                else:
                    redirect("/login")
            else:
                print("Rostro incorrecto, Cerifique su usuario")
                print("Compatibilidad con la foto del registro: ",similitud)
                Label(pantalla2, text = "Incompatibilidad de rostros", fg = "red", font = ("Calibri",11)).pack()
        else:
            print("Usuario no encontrado")
            Label(pantalla2, text = "Usuario no encontrado", fg = "red", font = ("Calibri",11)).pack()
                
#////////////////////////////Pantalla de REGISTRO///////////////////////////////////////////////////////////////////////////////////////////////////////////
 #------------------------Crearemos una funcion para asignar al boton registro --------------------------------
    def registro():
        global usuario
        global contra  #Globalizamos las variables para usarlas en otras funciones
        global usuario_entrada
        global contra_entrada
        global pantalla1
        
        pantalla1 = Toplevel(pantalla) #Esta pantalla es de un nivel superior a la principal
        pantalla1.title("Registro")
        pantalla1.config(bg="gray1")
        ancho_ventana = 300
        alto_ventana = 300
        x_ventana = pantalla1.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = pantalla1.winfo_screenheight() // 2 - alto_ventana // 2
        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        pantalla1.geometry(posicion)  #Asignamos el tamaño de la ventana
        
        #--------- Empezaremos a crear las entradas ----------------------------------------
        
        usuario = StringVar()
        contra = StringVar()
        Label(pantalla1, text = "",bg="gray1").pack()  #Dejamos un poco de espacio
        Label(pantalla1, text = "REGISTRO DE USUARIO",bg="gray1", fg="turquoise1").pack()
        Label(pantalla1, text = "",bg="gray1").pack()  #Dejamos un poco de espacio
        Label(pantalla1, text = "Usuario",bg="gray1",fg="white").pack()  #Mostramos en la pantalla 1 el usuario
        usuario_entrada = Entry(pantalla1, textvariable = usuario) #Creamos un text variable para que el usuario ingrese la info
        usuario_entrada.pack()
        Label(pantalla1, text = "Contraseña",bg="gray1",fg="white").pack()  #Mostramos en la pantalla 1 la contraseña
        contra_entrada = Entry(pantalla1, textvariable = contra) #Creamos un text variable para que el usuario ingrese la contra
        contra_entrada.pack()
        Label(pantalla1, text = "",bg="gray1").pack()  #Dejamos un espacio para la creacion del boton
        Button(pantalla1, text = "Registrarse", width = 15, height = 1, command = registrar_usuario,bg="turquoise1").pack()  #Creamos el boton
        #------------ Vamos a crear el boton para hacer el registro facial --------------------
        Label(pantalla1, text = "",bg="gray1").pack()
        Button(pantalla1, text = "Registro Facial", width = 15, height = 1, command = registro_facial,bg="turquoise1").pack()
        
#////////////////////////////Pantalla de LOGIN///////////////////////////////////////////////////////////////////////////////////////////////////////////
#------------------------Funcion que asignaremos al boton login -------------------------------------------------
            
    def login():
        global pantalla2
        global verificacion_usuario
        global verificacion_contra
        global usuario_entrada2
        global contra_entrada2
        
        pantalla2 = Toplevel(pantalla)
        pantalla2.title("Login")
        pantalla2.config(bg="gray1")
        ancho_ventana = 300
        alto_ventana = 300
        x_ventana = pantalla2.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = pantalla2.winfo_screenheight() // 2 - alto_ventana // 2
        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        pantalla2.geometry(posicion)   #Creamos la ventana
        Label(pantalla2, text = "",bg="gray1").pack()  #Dejamos un poco de espacio
        Label(pantalla2, text = "INICIO DE SESION", bg="gray1",fg="turquoise1").pack()
        Label(pantalla2, text = "",bg="gray1").pack()  #Dejamos un poco de espacio
        
        verificacion_usuario = StringVar()
        verificacion_contra = StringVar()
        
        #---------------------------------- Ingresamos los datos --------------------------
        Label(pantalla2, text = "Usuario",fg="white",bg="gray1").pack()
        usuario_entrada2 = Entry(pantalla2, textvariable = verificacion_usuario)
        usuario_entrada2.pack()
        Label(pantalla2, text = "Contraseña",fg="white",bg="gray1").pack()
        contra_entrada2 = Entry(pantalla2, textvariable = verificacion_contra)
        contra_entrada2.pack()
        Label(pantalla2, text = "" ,bg="gray1").pack()
        Button(pantalla2, text = "Inicio de Sesion", width = 20, height = 1, command = verificacion_login, bg="turquoise1").pack()
    
        #------------ Vamos a crear el boton para hacer el login facial --------------------
        Label(pantalla2, text = "", bg="gray1").pack()
        Button(pantalla2, text = "Inicio de Sesion Facial", width = 20, height = 1, command = login_facial, bg="turquoise1").pack()
        
                
    #/////////////////////////////////////////////////////////////////////////// Funcion de nuestra pantalla principal ///////////////////////////////////////////////////////////////////////////////////////////
        
    def pantalla_principal():
        global pantalla          #Globalizamos la variable para usarla en otras funciones
        pantalla = Tk()
    
        pantalla.config(bg="gray1")
        ancho_ventana = 700
        alto_ventana = 540
        x_ventana = pantalla.winfo_screenwidth() // 2 - ancho_ventana // 2;
        y_ventana = pantalla.winfo_screenheight() // 2 - alto_ventana // 2;
        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        pantalla.geometry(posicion)
        pantalla.resizable(0,0)    
        
        
        pantalla.title("Login con Reconocimiento Facial")       #Asignamos el titulo de la pantalla
        Label(text = "Login Facial", bg = "gray1", width = "300",fg="white", height = "2", font = ("Verdana", 13)).pack() #Asignamos caracteristicas de la ventana
        Label(text = "", bg = "gray1")
        
    #------------------------- Vamos a Crear los Botones ------------------------------------------------------
        
        #Label(text = "").pack()  #Creamos el espacio entre el titulo y el primer boton
        Button(text = "Iniciar Sesion", height = "2", width = "30", command = login, bg="turquoise1").pack()
        Label(text = "", bg = "gray1").pack() #Creamos el espacio entre el primer boton y el segundo boton
        Button(text = "Registro", height = "2", width = "30", command = registro, bg="turquoise1").pack()
        Label(text = "", bg = "gray1").pack()
        #COLOCAR IMAGEN
        img =tkinter.PhotoImage(file="static/img/IA2.png")
        lbl_img = tkinter.Label(pantalla, image = img, bg="gray1")
        lbl_img.pack()

        pantalla.mainloop()

    pantalla_principal()
    return redirect(url_for("login"))

    

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    

@app.route('/video',  methods= ["GET", "POST"])
def video():
    return Response(faceId(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/profile', methods = ["GET", "POST"])
def profile():
    #session.clear()
    if (comprobador == False):
        return redirect(url_for("home"))
    else:
        return render_template("profile.html")

if __name__ == '__main__':
    app.secret_key = "pinchellave"
    app.run(debug=True)


@app.route('/Extra', methods = ["GET", "POST"])
def Extra():
    return render_template("Extra.html")

# @app.route('/Extra?', methods = ["GET", "POST"])
# def Extra():
#     return render_template("Extra.html")





@app.route('/base',  methods= ["GET", "POST"])
def base():
    return Response(baseAlgoritmo(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/entrenamiento',  methods= ["GET", "POST"])
def entrenamiento():
    return Response(entrenamientoAlgoritmo(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/prueba',  methods= ["GET", "POST"])
def prueba():
    return Response(pruebaAlgoritmo(), mimetype='multipart/x-mixed-replace; boundary=frame')    

    