import pytest
from core.s3.s3_manejador import S3Manejador

def test_descargar(s3_configuracion):
    # ARRANGE
    s3_falso, nombre_bucket = s3_configuracion

    nombre_archivo = "archivo.txt"
    contenido_archivo = b"Hola, mundo!"
    s3_falso.put_object(Bucket=nombre_bucket, Key=nombre_archivo, Body=contenido_archivo)


    # ACT
    manejador = S3Manejador(bucket=nombre_bucket)
    resultado = manejador.descargar_archivo(nombre_archivo)

    #ASSERT
    assert resultado == contenido_archivo
