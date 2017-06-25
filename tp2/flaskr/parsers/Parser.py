from gateway.OmdbGateway import OmdbGateway
from services.OmdbService import OmdbService

class Parser(object):
    def parse(text):
        """ Parsea y devuelve el texto correspondiente a la consulta realizada """
        words = text.split()

        gateway = OmdbGateway()
        service = OmdbService(gateway)
        # Chequear esto, la gramatica seria quiero algo pelicula, asumo que el titulo de la pelicula viene de la posicion 2 en adelante
        movie = " ".join(words[2:])
        answer = ""


        if("actores" in words):
            actores = service.actors(movie)
            answer = "Los actores de la pelicula son " + str(actores)
        if("genero" in words):
            genero = service.genre(movie)
            if(len(genero.split()) > 1):
                answer = "Los generos de la pelicula son " + str(genero)
            else:
                answer = "El genero de la pelicula es " + str(genero)
        if("año" in words):
            anio = service.anio(movie)
            answer = "El año en el que se filmo la pelicula es " + str(anio)
        if("duracion" in words):
            duracion = service.duracion(movie)
            duracion = duracion.split()
            answer = "La duración de la pelicula es de " + str(duracion[0]) + " minutos"
        if("argumento" in words):
            plot = service.plot(movie)
            answer = str(plot)
        if("idioma" in words):
            idioma = service.language(movie)
            if(len(idioma.split()) > 1):
                answer = "Los idiomas de la pelicula son  " + str(idioma)
            else:
                answer = "El idioma de la pelicula es " + str(idioma)
            answer = ""
        if("premios" in words):
            premios = service.awards(movie)
            answer = "Los premios de la pelicula son " + str(premios)
        if("poster" in words):
            pass
        if("rating" in words):
            rating = service.ratings(movie)
            answer = "El rating de la pelicula es " + str(rating)
        if("productor" in words):
            productor = service.production(movie)
            answer = "El productor de la pelicula es " + str(productor)
        return answer
