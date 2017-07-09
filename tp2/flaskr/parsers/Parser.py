from gateway.OmdbGateway import OmdbGateway
from services.OmdbService import OmdbService

class Parser(object):
    def parse(self, pelicula, tipo_info):
        """ Parsea y devuelve el texto correspondiente a la consulta realizada """

        gateway = OmdbGateway()
        service = OmdbService(gateway)
        answer = ""

        if("actores" in tipo_info):
            actores = service.actors(pelicula)
            answer = "Los actores de la película son " + str(actores)
        if("género" in tipo_info):
            genero = service.genre(pelicula)
            if(len(genero.split()) > 1):
                answer = "Los generos de la película son " + str(genero)
            else:
                answer = "El género de la película es " + str(genero)
        if("año" in tipo_info):
            anio = service.anio(pelicula)
            answer = "El año en el que se filmó la película es " + str(anio)

        if("director" in tipo_info):
            director = service.director(pelicula)
            answer = "El director de la película es " + str(director)

        if("duracion" in tipo_info):
            duracion = service.duracion(pelicula)
            duracion = duracion.split()
            answer = "La duración de la película es de " + str(duracion[0]) + " minutos"
        if("argumento" in tipo_info):
            plot = service.plot(pelicula)
            answer = str(plot)
        if("idioma" in tipo_info):
            idioma = service.language(pelicula)
            if(len(idioma.split()) > 1):
                answer = "Los idiomas de la película son  " + str(idioma)
            else:
                answer = "El idioma de la película es " + str(idioma)
            answer = ""
        if("premios" in tipo_info):
            premios = service.awards(pelicula)
            answer = "Los premios de la película son " + str(premios)
        if("poster" in tipo_info):
            pass
        if("rating" in tipo_info):
            rating = service.ratings(pelicula)
            answer = "El rating de la película es " + str(rating)
        if("productor" in tipo_info):
            productor = service.production(pelicula)
            answer = "El productor de la película es " + str(productor)
        return answer
