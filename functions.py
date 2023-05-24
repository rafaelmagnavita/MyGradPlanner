from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox
import pyodbc
import Models.Materias
import Models.Semestre
import Models.Cursos

class FunctionsU():

    def startQuery():          
        conexao = conectar_banco_dados()

        # Definir o número de semestres
        numero_semestres = 10
        materias_completadas = []
        print("Lista de Cursos: ")
        for curso in obter_cursos(conexao):
            print(f"Curso: {curso.Nome} - Código: {curso.id}")
        curso = input("Digite o ID do Curso: ")
        # Listar as matérias já completadas
        materias_disponiveis = obter_materias_semestre(conexao, curso)
        if not materias_disponiveis:
            FunctionsU.startQuery()
        semestres = []
        for semestre in range(1, numero_semestres + 1):
            semestreObject = Models.Semestre.Semestre(semestre, None)
            semestres.append(semestreObject)
            materias_do_semestre = []
            print(f"--- Semestre {semestre} ---")

            # Obter as matérias disponíveis para o semestre atual

            if not materias_disponiveis:
                print("Nenhuma matéria disponível para este semestre.")
                continue

            print("Matérias disponíveis:")
            for materia in materias_disponiveis:
                print(f"{materia.Nome}")

            while True:
                # Solicitar ao usuário que selecione uma matéria
                while True:
                    materia_selecionada = input("Digite o ID da matéria que deseja selecionar (ou 's' para sair e 'p' para próximo semestre): ")

                    if materia_selecionada == 's':
                        break
                    if materia_selecionada == 'p':                
                        break
                    if not materia_selecionada.isdigit():
                        print('Código Inválido')
                        continue
                    else:
                        break                 
                   
                if materia_selecionada == 's':
                    break
                if materia_selecionada == 'p':                
                    break 
                else:
                    materia_id = int(materia_selecionada)
                    materias_disponiveis_dict = {materia.id: materia for materia in materias_disponiveis}
                    materia = materias_disponiveis_dict.get(materia_id)
                    if materia is None:
                        print('Matéria Incorreta')                       
                    else:
                        if materia.Dependencias is None:   
                            materias_do_semestre.append(materia) 
                            materias_completadas.append(materia)
                            materias_disponiveis.remove(materia)
                            print(f"Matéria {materia.Nome} Adicionada Com Sucesso")   
                 
                        else:
                            preRequisitosCursados = True
                            for materiaDependencia in materia.Dependencias:
                                materias_completadas_dict = {materia.id: materia for materia in materias_completadas}
                                materias_semestre_dict = {materia.id: materia for materia in materias_do_semestre}          
                                dependenciaOnSemestre = materias_semestre_dict.get(materiaDependencia)
                                if not dependenciaOnSemestre is None:
                                    print(f'Pré-Requisito {materiaDependencia} no mesmo Semestre')
                                    preRequisitosCursados = False                                       
                                materiaCursada = materias_completadas_dict.get(materiaDependencia)
                                if materiaCursada is None:
                                    print(f'Ausência do Pré-Requisito {materiaDependencia}')
                                    preRequisitosCursados = False
                            if(preRequisitosCursados == True):
                                materias_do_semestre.append(materia) 
                                materias_completadas.append(materia)
                                materias_disponiveis.remove(materia)
                                print(f"Matéria {materia.Nome} Adicionada Com Sucesso")   
    
                                
                                    

                              
                    
                        


def conectar_banco_dados():
    # Configurar a conexão com o banco de dados SQL Server
    server = 'localhost\SQLEXPRESS'
    database = 'DadosUniversidade'
    username = 'ecp'
    password = '1234'

    # Conectar ao banco de dados
    conexao = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    return conexao

def obter_materiasIds_curso(cursoID, conexao):
    materias = []
    cursor = conexao.cursor()
    cursor.execute(f"SELECT * FROM MateriasCursos where CursoId = {cursoID}")
    results = cursor.fetchall()
    if not results:
     print('Curso Inválido')
     return None
    for row in results:
        materia_id = getattr(row, 'MateriaId')
        materias.append(materia_id)
    return materias

def obter_cursos(conexao):
    cursos = []
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM Cursos")
    results = cursor.fetchall()
    for row in results:
        cursoId = getattr(row, 'Id')
        Nome = getattr(row, 'Nome')
        curso = Models.Cursos.Cursos(cursoId, Nome)
        cursos.append(curso)
    return cursos

def obter_materias_semestre(conexao, curso):
    # Consultar as matérias disponíveis para o curso especificado
    materias = obter_materiasIds_curso(curso, conexao)
    if not materias:
        return None
    materias_disponiveis = []
    for materiaCurso in materias:
        cursor = conexao.cursor()
        cursor.execute(f"SELECT * FROM Materias where Id = {materiaCurso}")
        results = cursor.fetchall()

        for row in results:
            materia_id = getattr(row, 'Id')
            materia_nome = getattr(row, 'Nome')
            materia_codigo = getattr(row, 'Codigo')
            materia_dependencias = obter_dependencias_materia(conexao, materia_id)
            materia = Models.Materias.Materia(materia_id,materia_nome,materia_codigo, materia_dependencias)
            materias_disponiveis.append(materia)
    return materias_disponiveis

def obter_dependencias_materia(conexao, id):
    # Consultar as matérias disponíveis para o semestre especificado
    cursor = conexao.cursor()
    cursor.execute(f"SELECT * FROM Dependencias Where MateriaId = {id}")
    results = cursor.fetchall()
    dependencias = []

    for row in results:
        dependencia = getattr(row, 'DependenciaId')
        dependencias.append(dependencia)
    return dependencias
