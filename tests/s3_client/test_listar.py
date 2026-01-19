import pytest  # noqa
from core.s3.s3_manejador import S3Manejador


def test_list_objects(s3_configuracion):
    """
    debe retornar una lista de archivos
    """
    # ARRANGE
    s3_falso, nombre_bucket = s3_configuracion

    s3_falso.put_object(Bucket=nombre_bucket, Key="archivo.txt")
    s3_falso.put_object(Bucket=nombre_bucket, Key="archivo2.txt")

    # ACT
    manejador = S3Manejador(bucket=nombre_bucket)
    result = manejador.listar_archivos()

    # ASSERT
    assert isinstance(result, list), "El método debería retornar una lista"
    assert len(result) == 2, " solo hay dos objetos"

    assert "archivo.txt" in result
    assert "archivo2.txt" in result
