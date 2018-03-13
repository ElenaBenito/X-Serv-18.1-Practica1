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
#Habria que copiar el contenido de diccionario.csv en el diccionario si el fichero csv ya existe. Después hay que buscar en el diccionario si la url solicitada ya ha sido acortada.
		if metodo == "GET":
			if recurso != '/':		#Redireccionar al sitio
				url_corta = "http://localhost:1234" + recurso
				print(self.diccionario_short)
				try: 
					redirect = self.diccionario_short[url_corta]
					code = "200 OK"
					body = "<html><head><meta http-equiv='Refresh' content=3;url=" + redirect +"></head><body><h1>""Espere a ser 								redirigido""</h1></body></html>"
				except KeyError:
					code = "404 NOT_FOUND"
					body = "<html>""HTTP ERROR: Recurso no disponible""</html>"	
			else:								#si no hay recurso, mostramos el formulario y la lista de urls acortadas (archivo csv)
				code = "200 OK"
				body = "<html><h1>Formulario<br><br></h1>" + formulario + "<html><body><br><br><h1>Lista de URLs acortadas: </h1></body></html>"
				with open('diccionario.csv') as csvarchivo:
					entrada = csv.reader(csvarchivo)
					for reg in entrada:
						line = str(reg)
						linecsv = line.split(',')[0] + " -->" + line.split(',')[1]
						body = body + "<html><body>" + linecsv + "<br></body></html>"
		elif metodo == "POST":
			url = peticion.split('\r\n\r\n',1)[1].split('=')[1]
			url = urllib.parse.unquote(url, encoding='utf-8', errors='replace')
			begin_url = url.split('://')[0] 
			print ("begin_url= "+begin_url)
			if begin_url != "http" and begin_url != "https":
				url = "http://" + url
			short_url = "http://localhost:1234/" + str(self.num)
			self.num += 1
			self.diccionario_real[url] = short_url
			self.diccionario_short[short_url] = url
			with open('diccionario.csv', 'a', newline='') as myfile:
				newUrl = csv.writer(myfile).writerow([short_url, url])
			code = "200 OK"
			body = "<html>""URL real: <a href=>"+ url +"</a><br><br>URL acortada: <a href=>" + short_url + "</a></html>"
		return(code, body)

	def __init__(self, hostname, port):
# Abrir el fichero que contiene el diccionario en formato separado por comas. 'x'-->crear y escribir; 'a'-->abrir para escribir al final de lo que tenga si está ya escrito
		myfile = open('diccionario.csv', 'a')
		myfile.close()
		super().__init__(hostname,port)

if __name__=="__main__":
	testWebApp = shortWebApp("localhost",1234)
