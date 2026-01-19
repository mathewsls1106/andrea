import pytest  # noqa
from core.s3.s3_manejador import S3Manejador

def test_subir_archivos(s3_configuracion):
    # ARRANGE
    s3_falso, nombre_bucket = s3_configuracion
    nombre_archivo = "documento.txt"
    contenido = "Hola criaturitas del senior"

    s3_falso.create_bucket(Bucket=nombre_bucket)
    manejador = S3Manejador(bucket=nombre_bucket)

    # ACT
    resultado = manejador.subir_archivo(nombre=nombre_archivo, contenido=contenido)

    # verifica que se haya subido el archivo correctamente
    objetos = s3_falso.list_objects_v2(Bucket=nombre_bucket)
    keys = [obj["Key"] for obj in objetos.get("Contents", [])]

    assert resultado is True
    assert nombre_archivo in keys
