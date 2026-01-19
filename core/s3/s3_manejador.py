import boto3
from typing import Optional, List, Any
from pathlib import Path
import os

class S3Manejador:
    def __init__(self, bucket: str):
        self.nombre_bucket = bucket
        self.s3 = boto3.client("s3")

    def listar_archivos(self, prefijo: Optional[str] = None) -> List[str]:
        """
        lista todos los objetos en el bucket
        """
        parametros = {"Bucket": self.nombre_bucket}

        if prefijo:
            parametros["Prefix"] = prefijo

        respuesta = self.s3.list_objects_v2(**parametros)

        # retorna solo los keys de los archivos
        return [objeto["Key"] for objeto in respuesta.get("Contents", [])]

    def subir_archivo(self, nombre: str, contenido: Any) -> bool:
        """
        sube un archivo al bucket
        """
        try:
            self.s3.put_object(Bucket=self.nombre_bucket, Key=nombre, Body=contenido)
            print("subida correctamente")
            return True
        except Exception as e:
            print(f"error al subir archivo: {e}")
            return False

    def descargar_archivo(self, nombre_archivo: str) -> Optional[bytes]:
        """
        descarga un archivo del bucket
        """
        try:
            respuesta = self.s3.get_object(Bucket=self.nombre_bucket, Key=nombre_archivo)
            contenido = respuesta["Body"].read()
            print("descarga correcta")
            return contenido
        except Exception as e:
            print(f"error al descargar archivo: {e}")
            return None

    def eliminar_archivo(self, nombre_archivo: str) -> bool:
        """
        elimina un archivo del bucket
        """
        try:
            self.s3.delete_object(Bucket=self.nombre_bucket, Key=nombre_archivo)
            print("eliminacion correcta")
            return True
        except Exception as e:
            print(f"error al eliminar archivo: {e}")
            return False

    def subir_carpeta(self, ruta_local: str) -> bool:
        """
        sube una carpeta al bucket
        """
        ruta_base = Path(ruta_local)
        try:
            for raiz, directorios, archivos in os.walk(ruta_base):
                for archivo in archivos:
                    ruta_completa = Path(raiz) / archivo
                    s3_key = str(ruta_completa.relative_to(ruta_base))
                    self.s3.upload_file(
                        Filename=str(ruta_completa),
                        Bucket=self.nombre_bucket,
                        Key=s3_key
                    )
            print("subida correcta")
            return True
        except Exception as e:
            print(f"error al subir carpeta: {e}")
            return False
