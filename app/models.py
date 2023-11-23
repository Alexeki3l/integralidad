from django.db import models
from authentication.models import Profile
from django.contrib.auth.models import User

from django.urls import reverse, reverse_lazy
# Create your models here.


class Asignatura(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    # student = models.ForeignKey(ActivityAndStudent, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Aspecto(models.Model):
    name = models.CharField(max_length=1500)
    
    create_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Activity(models.Model):
    # MONTHS = (
    #     (0, '--'),
    #     (1, 'enero'),
    #     (2, 'febrero'),
    #     (3, 'marzo'),
    #     (4, 'abril'),
    #     (5, 'mayo'),
    #     (6, 'junio'),
    #     (7, 'julio'),
    #     (8, 'agosto'),
    #     (9, 'septiembre'),
    #     (10, 'octubre'),
    #     (11, 'noviembre'),
    #     (12, 'diciembre'),
    # )
    
    name = models.CharField(max_length=2500)
    # month =  models.IntegerField(choices=MONTHS, default=0)
    # weight = models.FloatField()
    is_open = models.BooleanField(default=True)
    aspecto = models.ForeignKey(Aspecto, on_delete=models.CASCADE)
    
    profiles = models.ManyToManyField(Profile, through="ActivityAndStudent")
    
    create_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('list_activities')
    

class ActivityAndStudent(models.Model):
    
    TYPE_NIVEL = (
        (1, 'Brigada'),
        (2, 'Facultad'),
        (3, 'Universidad'),
    )
    
    TYPE_NIVEL_CARGO_FEU = (
        (1, 'Presidente'),
        (2, 'Vice-Presidente'),
        (3, 'Activista de Alta'),
        (4, 'Organizador'),
        (5, 'Ideologico'),
        (6, 'Cultura'),
        (7, 'Deporte'),
        (8, 'Comunicacion'),
        (9, 'Atension a planteamientos'),
        (10, 'Atension al becario'),
        (11, 'Investigacion'),
        (12, 'Docencia'),
    )
    
    TYPE_EVALUACION = (
        (1, 'Bien'),
        (2, 'Regular'),
        (3, 'Mal'),
    )
    
    TYPE_NIVEL_CARGO_UJC = (
        (1, 'Presidente'),
        (2, 'Vice-Presidente'),
        (3, 'Activista de Alta'),
        (4, 'Organizador'),
        (5, 'Ideologico'),
        (6, 'Cultura'),
        (7, 'Deporte'),
        (8, 'Comunicacion'),
        (9, 'Atension a planteamientos'),
        (10, 'Atension al becario'),
        (11, 'Investigacion'),
        (12, 'Docencia'),
    )
    
    TYPE_ROLES = (
        (1, 'Administrador'),
        (2, 'Analista'),
        (3, 'Programador'),
        (4, 'Jefe de Proyecto'),
    )
    
    TYPE_NIVEL_ALCANZADO = (
        (1, 'Avanzado'),
        (2, 'Intermedio'),
        (3, 'Basico'),
    )
    
    TYPE_PARTICIPACION = (
        (1, 'Capacitaciones'),
        (2, 'Despliegues'),
        (3, 'Exposicion de Resultado de la Produccion'),
        # (4, 'Exposicion de Resultado'),
    )
    
    TYPE_NIVEL_EVENTO= (
        (1, 'Nacionales'),
        (2, 'Internacionales'),
    )
    
    TYPE_AUTOR = (
        (1, '1er Autor'),
        (2, '2do Autor'),
        (2, '3er Autor'),
    )
    
    TYPE_NIVEL_PUBLICACION = (
        (1, 'Primero'),
        (2, 'Segundo'),
        (3, 'Tercero'),
        (4, 'Cuarto'),
    )
    
    TYPE_ACTIVIDAD_PID = (
        (1, 'Ferias'),
        (2, 'Despliegues'),
        (3, 'Otras Actividades de la Produccion'),
    )
    
    # TYPE_ORGANIZACION = (
    #     (1, 'FEU'),
    #     (2, 'UJC'),
    # )
    
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    is_valid = models.BooleanField(default=True)
    year = models.IntegerField(null=True, blank=True)
    
    # ---------------- Politico Ideologico ------------------
    # organizacion = models.IntegerField(choices=TYPE_ORGANIZACION, null=True, blank=True)
    is_feu = models.BooleanField(default=False)
    is_ujc = models.BooleanField(default=False)
    nivel =  models.IntegerField(choices=TYPE_NIVEL, null=True, blank=True)
    cargo_feu =  models.IntegerField(choices=TYPE_NIVEL_CARGO_FEU, null=True, blank=True)
    evaluacion = models.IntegerField(choices=TYPE_EVALUACION, null=True, blank=True)
    
    comite_base = models.CharField(max_length=50, null=True, blank=True)
    cargo_ujc = models.IntegerField(choices=TYPE_NIVEL_CARGO_UJC, null=True, blank=True)
    
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    
    distincion_marzo = models.BooleanField(default=False,
                                    help_text="Este se refiere a la distincion 13 de Marzo")
    
    distincion_fututo_maestro = models.BooleanField(default=False,
                                    help_text="Este se refiere a la distincion del Futuro Maestro")
    
    distincion_joven = models.BooleanField(default=False,
                                    help_text="Este campo se refiere a la distinsion Joven 20 Aniversario de la FEU")
    is_ayudante = models.BooleanField(default=False,
                                    help_text="Este campo se refiere a que si el alumno fue 'alumno ayudante'")
    
    # asignatura_ayudante = models.CharField(max_length=100, null=True, blank=True)
    
    asignaturas_ayudante = models.ManyToManyField(Asignatura)
    
    # ------------------------------------------------------
    
    # ----------------- Investigativa son 4 ----------------------
    # Esto es el tema de los Eventos
    TYPE_NIVEL = (
        (1, 'Facultad'),
        (2, 'Universidad'),
        (3, 'Provincial'),
        (4, 'Nacional'),
        (5, 'Internacional'),
        
    )
    TYPE_RESULT = (
        (1, 'Relevante'),
        (2, 'Destacado'),
        (3, 'Mencion'),
        (4, 'Participacion'),
    )
    TYPE_JORNADA_ICI = (
        (1, 'Copa de Ingeniera de Software'),
        (2, 'Copa de Base de Datos'),
        (3, 'Copa Pascal'),
        (4, 'Mi web por Cuba'),
        (5, 'Olimpiada de Matematica'),
    )
    TYPE_NOMBRE_EVENTO = (
        (1, 'Forum de Historia'),
        (2, 'Seminario Juvenil MArtiano'),
        (3, 'Olimpiada de Idiomas'),
        (4, 'Jornada de Ingeniero en Ciencias Informaticas'),
        (5, 'Jornada Cientifica Estudiantil'),
        (6, 'Peña Tecnologica'),
    )
    # nombre = models.CharField(max_length=255, null=True, blank=True)
    is_evento = models.BooleanField(default=False)
    nombre_evento = models.IntegerField(choices=TYPE_NOMBRE_EVENTO, null=True, blank=True)
    nombre_sub_evento = models.IntegerField(choices=TYPE_JORNADA_ICI, null=True, blank=True)
    es_colateral = models.BooleanField(default=False)
    nombre_evento_colateral = models.CharField(max_length=255, null=True, blank=True)
    nivel =  models.IntegerField(choices=TYPE_NIVEL, null=True, blank=True)
    result = models.IntegerField(choices=TYPE_RESULT, null=True, blank=True)
    
    # Aqui hay una relacion de con la clase Eventos
    has_roles = models.BooleanField(default=False,)
    roles = models.CharField(max_length=255, choices=TYPE_ROLES, null=True, blank=True)
    nivel_alcanzado = models.IntegerField(choices=TYPE_NIVEL_ALCANZADO, null=True, blank=True)
    
    has_investigacion = models.BooleanField(default=False, help_text="Si pertence o no a una linea de investigacion")
    participacion = models.IntegerField(choices=TYPE_PARTICIPACION, null=True, blank=True)
    nivel_evento = models.IntegerField(choices=TYPE_NIVEL_EVENTO, null=True, blank=True, help_text="Esto es de 'Pertenece a una linea de investigacion'")
    
    has_publicacion = models.BooleanField(default=False)
    nombre_publicacion = models.CharField(max_length=100, null=True, blank=True)
    nivel_autor = models.IntegerField(choices=TYPE_AUTOR, null=True, blank=True, help_text="Esto es de 'Publicaciones logradas como autor o coautor'")
    nivel_publicacion = models.IntegerField(choices=TYPE_NIVEL_PUBLICACION, null=True, blank=True, help_text="Esto es de 'Publicaciones logradas como autor o coautor'")
    
    # ---------------------- Academico --------------------------
    where_pid = models.CharField(max_length=100, null=True, blank=True, help_text="Area donde has realizado la PID")
    rol = models.CharField(max_length=100, null=True, blank=True, help_text="Area donde has realizado la PID")
    actividades_pid = models.IntegerField(choices=TYPE_ACTIVIDAD_PID, null=True, blank=True)
    
    grupo_edu_amor = models.BooleanField(default=False)
    
    with_arrastres = models.BooleanField(default=False)
    with_mundiales = models.BooleanField(default=False)
    with_repitencias = models.BooleanField(default=False)
    cantidad_repitencias = models.IntegerField(default=0,null=True, blank=True)
    
    other_reconocimiento = models.TextField(max_length=255, null=True,blank=True)
    
    # ------------------------------------------------------
    
    # ---------------------- Extension --------------------------
    is_miembro = models.BooleanField(default=False)
    nombre_catedra = models.CharField(max_length=255, null=True, blank=True)
    actividad_participado = models.CharField(max_length=1000, null=True, blank=True)
    
    # Actividades Culturales
    if_participacion_actos_matutinos = models.BooleanField(default=False)
    # ------------
    TYPE_NIVEL_ARTISTA_AFICIONADO = (
        (1, 'Facultad'),
        (2, 'Provincial'),
        (3, 'Nacional'),
    )
    TYPE_PREMIO_ARTISTA_AFICIONADO = (
        (1, 'Oro'),
        (2, 'Plata'),
        (3, 'Bronce'),
        (4, 'Mencion'),
    )
    if_participacion_festivales = models.BooleanField(default=False)
    manifestacion_festivales = models.CharField(max_length=255, null=True, blank=True)
    nivel_artista_aficionado = models.IntegerField(choices=TYPE_NIVEL_ARTISTA_AFICIONADO, null=True, blank=True)
    premio_artista_aficionado = models.IntegerField(choices=TYPE_PREMIO_ARTISTA_AFICIONADO, null=True, blank=True)
    # ------------
    nombre_actividad_facultad = models.CharField(max_length=255, null=True, blank=True)
    manifestacion_actividad_facultad = models.CharField(max_length=255, null=True, blank=True)
    # ------------
    # Trabajo Socialmente Util
    lugar_dnd_realizo = models.CharField(max_length=255, null=True, blank=True)
    # ------------
    # Actividades Deportivas
    # *Juegos Mella
    TYPE_DEPORTE = (
        (1, 'Ajedrez'),
        (2, 'Atletismo'),
        (3, 'Carrera de Orientacion'),
        (4, 'Baloncesto'),
        (5, 'Balonmano'),
        (6, 'Boxeo'),
        (7, 'Futbol Sala'),
        (8, 'Futbol 11'),
        (9, 'Natacion'),
        (10, 'Tenis'),
        (11, 'Pelota'),
        (12, 'Softball'),
        (13, 'Voleyball'),
        (14, 'Voleyball Playa'),
        (15, 'Yudo'),
        (16, 'Karate'),
        (17, 'Taewondo'),
        (18, 'Taewondo'),
        (19, 'Cubalon'),
        (20, 'Maraton'),
        (21, 'DOTA'),
    )
    TYPE_RESULTADO_DEPORTE = (
        (1, 'Oro'),
        (2, 'Plata'),
        (3, 'Bronce'),
        (4, 'Participacion'),
    )
    TYPE_LUGAR = (
        (1, 'Universidad'),
        (2, 'Juegos Provinciales Giraldillos'),
        (3, 'Juegos Nacionales'),
    )
    if_jjmm = models.BooleanField(default=False)
    deporte = models.CharField(choices=TYPE_DEPORTE, null=True, blank=True, max_length=255)
    resultado_deporte = models.IntegerField(choices=TYPE_RESULTADO_DEPORTE, null=True, blank=True)
    lugar = models.IntegerField(choices=TYPE_LUGAR, null=True, blank=True)
    
    # Copas y Mundiales
    if_copas_mundialess = models.BooleanField(default=False)
    nombre_evento_copas_mundiales = models.CharField(max_length=255, null=True, blank=True)
    resultado_copas_mundiales = models.CharField(choices=TYPE_RESULTADO_DEPORTE, null=True, blank=True, max_length=255)
    lugar_copas_mundiales = models.CharField(max_length=255, null=True, blank=True)
    
    # *Eventos del Proyecto
    TYPE_EVENTO_MARABANA = (
        (1, 'MaraCuba'),
        (2, 'MaraHabana'),
        (3, 'Cacahual'),
        (4, 'Maratón por el Día Olímpico'),
        (5, 'Maratón Terry Fox'),
        (6, 'Maratón 10 de Octubre'),
    )
    
    TYPE_EVALUACION_CUARTELERIA = (
        (1, 'Excelente'),
        (2, 'Bien'),
        (3, 'Regular'),
        (4, 'Mal'),
    )
    if_marabana = models.BooleanField(default=False)
    nombre_evento_marabana = models.IntegerField(choices=TYPE_EVENTO_MARABANA, null=True, blank=True)
    resultado_evento_marabana = models.IntegerField(choices=TYPE_RESULTADO_DEPORTE, null=True, blank=True)
    
    # ------------
    # Evaluacion en la residencia
    # *Cuarteleria
    cuartelerias = models.JSONField(null=True, blank=True)
    evaluacion_cuarteleria = models.CharField(choices=TYPE_EVALUACION_CUARTELERIA, null=True, blank=True, max_length=255)
    
    # *Responsabilidad
    TYPE_RESPONSABILIDAD = (
        (1, 'Jefe de Edificio'),
        (2, 'Jefe de Apartamento'),
        (3, 'Ninguna'),
    )
    responsabilidad = models.IntegerField(choices=TYPE_RESPONSABILIDAD, null=True, blank=True)
    # evaluacion
    # *Acta o sennalamiento en la residencia
    if_senalamiento_residencia = models.BooleanField(default=False)
    # hay un campo motivo que puede ser descripcion\
    
    # ------------
    # Guardia Estudiantil
    total_ausencias = models.IntegerField(null=True, blank=True)
    total_ausencias_justificadas = models.IntegerField(null=True, blank=True)
    total_ausencias_injustificadas = models.IntegerField(null=True, blank=True)
    total_recuperadas = models.IntegerField(null=True, blank=True)
    
    # *Acta o senalamiento por incumplimiento en la guardia estudiantil
    if_senalamiento_guardia_estudiantil = models.BooleanField(default=False)
    cantidad_senalamiento_guardia_estudiantil = models.IntegerField(null=True, blank=True)
    
    # ------------
    # Participacion en actividades de organizacion y limpieza de apartamento y áreas comunes 
    if_actividades_limpieza_areas_comunes = models.BooleanField(default=False)
    nombre_actividades_limpieza_areas_comunes = models.CharField(max_length=255, null= True, blank=True)
    mes = models.CharField(max_length=255, null= True, blank=True)
    resultado_actividades_limpieza_areas_comunes = models.CharField(max_length=255, null= True, blank=True)
    # poner la evidencia
    
    # *Participacion en mi BK+Bonita
    if_bk_mas_bonita = models.BooleanField(default=False)
    # reconocimiento se escribiran en el campo:other_reconocimiento
    # poner la evidencia
    
    # ------------
    # Reconocimiento en esta Etapa
    # nombre del reconocimiento se escribiran en el campo:other_reconocimiento
    reconocimiento_otorgado_por = models.CharField(max_length=255, null= True, blank=True)
    # poner la evidencia
    
    # ------------
    # Sanciones durante el curso
    sanciones_o_medida = models.CharField(max_length=1000, null=True, blank=True)
    motivo_sancion     = models.CharField(max_length=1000, null=True, blank=True)
    
    # ------------
    # Senalamiento durante el curso
    senalamiento_curso = models.CharField(max_length=1000, null=True, blank=True)
    
    # ------------
    # Distinciones Otorgadas
    nombre_distincion = models.CharField(max_length=255, null=True, blank=True)
    organismo_otorga_distincion = models.CharField(max_length=255, null=True, blank=True)
    
    # ------------
    # Misiones en la que haya participado
    PROCESO = (
        (1,'Cumplido'),
        (2,'En Cumplimiento'),
    )
    nombre_mision = models.CharField(max_length=255, null=True, blank=True)
    funsion_desempenada = models.CharField(max_length=255, null=True, blank=True)
    proceso = models.IntegerField(choices=PROCESO, null=True, blank=True)

    # ------------------------------------------------------
    
    
    
    create_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.activity.name} -- {self.profile.user.first_name} -- {self.year}'
    
    def get_absolute_url(self):
        return reverse('list_activities')

class Caracterizacion(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    fac = models.CharField(max_length=4)
    in_production = models.CharField(max_length=1)
    is_investigation = models.CharField(max_length=1)
    
    deporte = models.CharField(max_length=1)
    guardia = models.CharField(max_length=1)
    cultura = models.CharField(max_length=1)
    residencia = models.CharField(max_length=1)
    tsu = models.CharField(max_length=1)
    
    feu_ujc = models.CharField(max_length=1)
    premio_mella = models.BooleanField(default=False)
    titulo_oro = models.BooleanField(default=False)
    #medidas disciplinarias
    menos_graves = models.IntegerField(default=0)
    graves = models.IntegerField(default=0)
    muy_graves = models.IntegerField(default=0)
    
    is_repitente = models.BooleanField(default=False)
    arrastre = models.IntegerField(default=0)
    mundial = models.IntegerField(default=0)
    
    index_academico = models.FloatField(default=0)
    other_indicator = models.FloatField(default=0)
    valor_final = models.FloatField(default=0)


class Group(models.Model):
    name = models.CharField(max_length=4)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    create_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now_add=True)
    
    
