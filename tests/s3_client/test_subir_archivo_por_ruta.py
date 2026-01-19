import pytest
from core.s3.s3_manejador import S3Manejador

def test_subir_archivo_por_ruta(s3_configuracion, tmp_path):
    # ARRANGE
    s3_falso, nombre_bucket = s3_configuracion

    archivo_local = tmp_path / "mi_reporte.txt"
    archivo_local.write_text("Contenido del archivo")

    manejador = S3Manejador(bucket=nombre_bucket)

    resultado = manejador.subir_archivo_por_ruta(ruta_archivo=archivo_local)

    # ASSERT
    objetos = s3_falso.list_objects_v2(Bucket=nombre_bucket)
    keys = [objeto["Key"] for objeto in objetos.get("Contents", [])]
    assert len(keys) == 1
    assert resultado is True
