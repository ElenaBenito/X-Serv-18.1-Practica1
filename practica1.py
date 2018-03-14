#!/usr/bin/python3

import webapp
import csv
import urllib.parse

formulario = """
		<form method="POST" >
 		 URL a acortar:<br>
	   <input type="text" name="url" value=""><br>
  	   <input type="submit" value="Enviar"><br><br>
	   </form> 
		"""

class shortWebApp(webapp.webApp):
	
	diccionario_real = {}
	diccionario_short = {}
	num = 0

	def parse(self, request):
		return (request.split()[0], request.split()[1], request)

	def process(self, parsedRequest):  #parsedRequest es la tupla (metodo,recurso, peticion) de la petición
		metodo, recurso, peticion = parsedRequest	
		print("metodo =" + metodo)
		print("recurso =" + recurso)
		if metodo == "GET":
			if recurso != '/':		#Redireccionar al sitio
				url_corta = "http://localhost:1234" + recurso
				print(self.diccionario_short)
				try: 
					redirect = self.diccionario_short[url_corta]
					code = "302 FOUND"
					body = "<html><head><meta http-equiv='Refresh' content=3;url=" + redirect +"></head><body><h1>""HTTP REDIRECT<br></h1>""Espere a ser redirigido""</body></html>"
				except KeyError:
					code = "404 NOT_FOUND"
					body = "<html><body><h1>""HTTP ERROR: Recurso no disponible""</body></h1></html>"	
			else:								#si no hay recurso, mostramos el formulario y la lista de urls acortadas (archivo csv)
				code = "200 OK"
				body = "<html><h1>Formulario<br><br></h1>" + formulario + "<html><body><br><br><h1>Lista de URLs acortadas: </h1></body></html>"
				with open('diccionario.csv') as csvarchivo:
					entrada = csv.reader(csvarchivo)
					for reg in entrada:
						linecsv = reg[0] + " -->" + reg [1]
						body = body + "<html><body>" + linecsv + "<br></body></html>"
		elif metodo == "POST":
			url = peticion.split('\r\n\r\n',1)[1].split('=')[1]
			url = urllib.parse.unquote(url, encoding='utf-8', errors='replace')
			begin_url = url.split('://')[0] 
			print ("begin_url= "+begin_url)
			if begin_url != "http" and begin_url != "https":		#si no tiene http/https añadimos http por defecto
				url = "http://" + url
			#Buscamos la url en el diccionario_real
			if url in self.diccionario_real:	#Si está devolvemos la url que teníamos ya acortada
				short_url = self.diccionario_real[url]				
				code = "200 OK"
				body = "<html><h1>Url ya acortada!</h1><body>""URL real: <a href=>"+ url +"</a><br><br>URL acortada: <a href=>" + short_url + "</a></body></html>"
			else:	#Si no está en el diccionario la creamos y guardamos en el fichero csv		
				short_url = "http://localhost:1234/" + str(self.num)
				self.num += 1
				self.diccionario_real[url] = short_url
				self.diccionario_short[short_url] = url
				with open('diccionario.csv', 'a', newline='') as myfile:
					newUrl = csv.writer(myfile).writerow([short_url, url])
				code = "200 OK"
				body = "<html><body>""URL real: <a href=>"+ url +"</a><br><br>URL acortada: <a href=>" + short_url + "</a></body></html>"
		return(code, body)

	def __init__(self, hostname, port):
# Abrir el fichero que contiene el diccionario en formato separado por comas. 'x'-->crear y escribir; 'a'-->abrir para escribir al final de lo que tenga si está ya escrito
		myfile = open('diccionario.csv', 'a')
		with open('diccionario.csv') as csvarchivo:		#copiamos el archivo csv a los diccionarios
					entrada = csv.reader(csvarchivo)	#para tenerlos actualizados y que el programa
					for reg in entrada:					#sea persistente
						key = reg[0]
						value = reg[1]
						self.diccionario_short[key] = value
						self.diccionario_real[value] = key
		myfile.close()
		self.num = len(self.diccionario_short)			#cambiamos el valor de num=0 si tenemos guardadas más urls
		super().__init__(hostname,port)

if __name__=="__main__":
	testWebApp = shortWebApp("localhost",1234)
