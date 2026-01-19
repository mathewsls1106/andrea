import pytest
from core.s3.s3_manejador import S3Manejador


def test_subir_carpeta(s3_configuracion, tmp_path):
    s3_falso, nombre_bucket = s3_configuracion
    s3_manejador = S3Manejador(nombre_bucket)

    # creamos path temporal
    path_temporal = tmp_path / "mi proyecto"

    path_temporal.mkdir()
    (path_temporal / "archivo1.txt").write_text("contenido 1")
    (path_temporal / "archivo2.txt").write_text("contenido 2")
    # subimos carpeta
    s3_manejador.subir_carpeta(ruta_local=path_temporal)

    #ASSERT
    objetos = s3_falso.list_objects_v2(Bucket=nombre_bucket)
    keys = [obj['Key'] for obj in objetos.get('Contents', [])]
    assert "archivo1.txt" in keys
    assert "archivo2.txt" in keys
    assert len(keys) == 2
