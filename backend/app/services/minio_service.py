from minio import Minio
from minio.error import S3Error
from app.core.config import settings
import hashlib
from typing import BinaryIO, Optional
import logging

logger = logging.getLogger(__name__)

class MinioService:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
    
    def ensure_bucket(self, bucket_name: str) -> bool:
        """确保桶存在，不存在则创建"""
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                logger.info(f"创建桶: {bucket_name}")
            return True
        except S3Error as e:
            logger.error(f"桶操作失败: {e}")
            return False
    
    def upload_file(
        self,
        bucket_name: str,
        object_name: str,
        file_data: BinaryIO,
        file_size: int,
        content_type: str = "text/markdown"
    ) -> Optional[str]:
        """上传文件到 MinIO"""
        try:
            self.ensure_bucket(bucket_name)
            
            self.client.put_object(
                bucket_name,
                object_name,
                file_data,
                file_size,
                content_type=content_type
            )
            
            logger.info(f"文件上传成功: {bucket_name}/{object_name}")
            return f"{bucket_name}/{object_name}"
        except S3Error as e:
            logger.error(f"文件上传失败: {e}")
            return None
    
    def download_file(self, bucket_name: str, object_name: str) -> Optional[bytes]:
        """从 MinIO 下载文件"""
        try:
            response = self.client.get_object(bucket_name, object_name)
            data = response.read()
            response.close()
            response.release_conn()
            return data
        except S3Error as e:
            logger.error(f"文件下载失败: {e}")
            return None
    
    def delete_file(self, bucket_name: str, object_name: str) -> bool:
        """删除文件"""
        try:
            self.client.remove_object(bucket_name, object_name)
            logger.info(f"文件删除成功: {bucket_name}/{object_name}")
            return True
        except S3Error as e:
            logger.error(f"文件删除失败: {e}")
            return False
    
    def get_file_url(self, bucket_name: str, object_name: str, expires: int = 3600) -> Optional[str]:
        """获取文件的预签名 URL"""
        try:
            url = self.client.presigned_get_object(bucket_name, object_name, expires=expires)
            return url
        except S3Error as e:
            logger.error(f"获取文件 URL 失败: {e}")
            return None
    
    @staticmethod
    def calculate_file_hash(file_data: bytes) -> str:
        """计算文件的 SHA256 哈希值"""
        return hashlib.sha256(file_data).hexdigest()
    
    def build_object_path(self, project_name: str, open_id: str, filename: str) -> str:
        """构建对象存储路径"""
        return f"{open_id}/{filename}"
    
    def upload_multiple_files(
        self,
        bucket_name: str,
        base_path: str,
        files: list,
        content_type: str = "text/markdown"
    ) -> list:
        """批量上传文件，保持目录结构
        
        Args:
            bucket_name: 桶名
            base_path: 基础路径 (open_id)
            files: 文件列表，每个文件包含 (relative_path, file_data, file_size)
            content_type: 内容类型
            
        Returns:
            上传成功的文件路径列表
        """
        uploaded_files = []
        
        try:
            self.ensure_bucket(bucket_name)
            
            for relative_path, file_data, file_size in files:
                # 构建完整的对象路径，保持目录结构
                object_name = f"{base_path}/{relative_path}"
                
                try:
                    self.client.put_object(
                        bucket_name,
                        object_name,
                        file_data,
                        file_size,
                        content_type=content_type
                    )
                    
                    uploaded_files.append({
                        "path": f"{bucket_name}/{object_name}",
                        "relative_path": relative_path,
                        "size": file_size
                    })
                    logger.info(f"文件上传成功: {bucket_name}/{object_name}")
                    
                except S3Error as e:
                    logger.error(f"文件上传失败 {relative_path}: {e}")
                    continue
            
            return uploaded_files
            
        except Exception as e:
            logger.error(f"批量上传失败: {e}")
            return uploaded_files
    
    def list_objects(self, bucket_name: str, prefix: str = "") -> list:
        """列出桶中的对象"""
        try:
            objects = self.client.list_objects(bucket_name, prefix=prefix, recursive=True)
            return [obj.object_name for obj in objects]
        except S3Error as e:
            logger.error(f"列出对象失败: {e}")
            return []
    
    def delete_folder(self, bucket_name: str, folder_path: str) -> bool:
        """删除文件夹及其所有内容"""
        try:
            objects = self.list_objects(bucket_name, prefix=folder_path)
            for obj in objects:
                self.client.remove_object(bucket_name, obj)
            logger.info(f"文件夹删除成功: {bucket_name}/{folder_path}")
            return True
        except S3Error as e:
            logger.error(f"文件夹删除失败: {e}")
            return False

minio_service = MinioService()
