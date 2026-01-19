import pytest
from core.s3.s3_manejador import S3Manejador


def test_eliminar_archivo(s3_configuracion):
    s3_falso, nombre_bucket = s3_configuracion

    nombre_archivo = "archivo.txt"
    contenido_archivo = b"Hola, mundo!"
    s3_falso.put_object(Bucket=nombre_bucket, Key=nombre_archivo, Body=contenido_archivo)
    s3_manejador = S3Manejador(nombre_bucket)

    s3_manejador.eliminar_archivo(nombre_archivo)
    sut = s3_falso.list_objects_v2(Bucket=nombre_bucket)['KeyCount']
    assert sut == 0
