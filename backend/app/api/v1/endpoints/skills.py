from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.skill import (
    SkillCreate, SkillResponse, SkillListResponse, SkillUpdate, 
    CommentCreate, CommentResponse, SkillBatchUploadResponse
)
from app.models.skill import Skill, SkillStar, SkillComment
from app.services.minio_service import minio_service
from app.core.config import settings
from slugify import slugify
import io
import os
from pathlib import Path

router = APIRouter()

def get_current_user_open_id():
    """获取当前用户的 open_id (需要实现 SSO 认证)"""
    # TODO: 从 JWT token 或 session 中获取
    return "test_open_id"

@router.post("", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
async def upload_skill(
    file: UploadFile = File(...),
    skill_name: str = None,
    description: str = None,
    category_id: int = 1,
    project_id: int = 1,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_open_id)
):
    """上传 Skill 文件"""
    # 验证文件类型
    if not any(file.filename.endswith(ext) for ext in settings.ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="不支持的文件类型")
    
    # 读取文件内容
    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超过限制")
    
    # 计算文件哈希
    file_hash = minio_service.calculate_file_hash(file_content)
    
    # 检查是否已存在相同文件
    existing = db.query(Skill).filter(Skill.file_hash == file_hash).first()
    if existing:
        raise HTTPException(status_code=400, detail="文件已存在")
    
    # 构建存储路径
    project = db.execute("SELECT bucket_name FROM projects WHERE id = :id", {"id": project_id}).fetchone()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    bucket_name = project[0]
    object_path = minio_service.build_object_path(bucket_name, current_user, file.filename)
    
    # 上传到 MinIO
    file_stream = io.BytesIO(file_content)
    upload_result = minio_service.upload_file(
        bucket_name=bucket_name,
        object_name=object_path,
        file_data=file_stream,
        file_size=file_size
    )
    
    if not upload_result:
        raise HTTPException(status_code=500, detail="文件上传失败")
    
    # 创建数据库记录
    skill = Skill(
        skill_name=skill_name or file.filename,
        slug=slugify(skill_name or file.filename),
        description=description,
        category_id=category_id,
        project_id=project_id,
        owner_open_id=current_user,
        file_path=upload_result,
        file_name=file.filename,
        file_size=file_size,
        file_hash=file_hash
    )
    
    db.add(skill)
    db.commit()
    db.refresh(skill)
    
    return skill

@router.get("", response_model=SkillListResponse)
def list_skills(
    page: int = 1,
    page_size: int = 20,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取 Skill 列表"""
    query = db.query(Skill).filter(Skill.status == 1, Skill.is_public == 1)
    
    if category_id:
        query = query.filter(Skill.category_id == category_id)
    
    if search:
        query = query.filter(Skill.skill_name.contains(search))
    
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items
    }

@router.get("/{skill_id}", response_model=SkillResponse)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    """获取 Skill 详情"""
    skill = db.query(Skill).filter(Skill.id == skill_id, Skill.status == 1).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill 不存在")
    
    # 增加浏览次数
    skill.view_count += 1
    db.commit()
    
    return skill

@router.put("/{skill_id}", response_model=SkillResponse)
def update_skill(
    skill_id: int,
    skill_update: SkillUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_open_id)
):
    """更新 Skill"""
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill 不存在")
    
    if skill.owner_open_id != current_user:
        raise HTTPException(status_code=403, detail="无权限操作")
    
    for field, value in skill_update.dict(exclude_unset=True).items():
        setattr(skill, field, value)
    
    db.commit()
    db.refresh(skill)
    return skill

@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_open_id)
):
    """删除 Skill"""
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill 不存在")
    
    if skill.owner_open_id != current_user:
        raise HTTPException(status_code=403, detail="无权限操作")
    
    # 软删除
    skill.status = 0
    db.commit()

@router.post("/{skill_id}/star", status_code=status.HTTP_201_CREATED)
def star_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_open_id)
):
    """收藏 Skill"""
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill 不存在")
    
    existing = db.query(SkillStar).filter(
        SkillStar.skill_id == skill_id,
        SkillStar.user_open_id == current_user
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="已收藏")
    
    star = SkillStar(skill_id=skill_id, user_open_id=current_user)
    db.add(star)
    
    skill.star_count += 1
    db.commit()
    
    return {"message": "收藏成功"}

@router.delete("/{skill_id}/star", status_code=status.HTTP_204_NO_CONTENT)
def unstar_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_open_id)
):
    """取消收藏"""
    star = db.query(SkillStar).filter(
        SkillStar.skill_id == skill_id,
        SkillStar.user_open_id == current_user
    ).first()
    
    if not star:
        raise HTTPException(status_code=404, detail="未收藏")
    
    db.delete(star)
    
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if skill:
        skill.star_count = max(0, skill.star_count - 1)
    
    db.commit()

@router.post("/{skill_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    skill_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_open_id)
):
    """添加评论"""
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill 不存在")
    
    new_comment = SkillComment(
        skill_id=skill_id,
        user_open_id=current_user,
        **comment.dict()
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment

@router.get("/{skill_id}/comments", response_model=List[CommentResponse])
def list_comments(skill_id: int, db: Session = Depends(get_db)):
    """获取评论列表"""
    comments = db.query(SkillComment).filter(
        SkillComment.skill_id == skill_id,
        SkillComment.status == 1
    ).order_by(SkillComment.created_at.desc()).all()
    
    return comments

@router.post("/batch-upload", response_model=SkillBatchUploadResponse, status_code=status.HTTP_201_CREATED)
async def batch_upload_skills(
    files: List[UploadFile] = File(...),
    skill_name: str = Form(...),
    description: str = Form(None),
    category_id: int = Form(1),
    project_id: int = Form(1),
    preserve_structure: bool = Form(True),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_open_id)
):
    """批量上传文件/文件夹，保持目录结构
    
    Args:
        files: 上传的文件列表（支持多文件选择或文件夹）
        skill_name: Skill 名称
        description: Skill 描述
        category_id: 分类 ID
        project_id: 项目 ID
        preserve_structure: 是否保持目录结构（默认 True）
        
    Returns:
        上传结果统计
    """
    if not files:
        raise HTTPException(status_code=400, detail="没有上传文件")
    
    # 获取项目信息
    project = db.execute("SELECT bucket_name FROM projects WHERE id = :id", {"id": project_id}).fetchone()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    bucket_name = project[0]
    
    # 准备批量上传的文件列表
    files_to_upload = []
    total_size = 0
    file_hashes = []
    
    for file in files:
        # 读取文件内容
        file_content = await file.read()
        file_size = len(file_content)
        
        # 验证文件大小
        if file_size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"文件 {file.filename} 大小超过限制"
            )
        
        # 验证文件类型（可选，根据需求调整）
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext and file_ext not in settings.ALLOWED_EXTENSIONS:
            # 如果设置了允许的扩展名，则验证
            continue
        
        # 计算文件哈希
        file_hash = minio_service.calculate_file_hash(file_content)
        file_hashes.append(file_hash)
        
        # 处理文件路径
        if preserve_structure:
            # 保持原始目录结构
            # 文件名可能包含路径，如 "folder/subfolder/file.md"
            relative_path = file.filename
        else:
            # 扁平化，只保留文件名
            relative_path = os.path.basename(file.filename)
        
        # 标准化路径分隔符（Windows -> Unix）
        relative_path = relative_path.replace("\\", "/")
        
        files_to_upload.append((
            relative_path,
            io.BytesIO(file_content),
            file_size
        ))
        
        total_size += file_size
    
    if not files_to_upload:
        raise HTTPException(status_code=400, detail="没有有效的文件可上传")
    
    # 批量上传到 MinIO
    uploaded_results = minio_service.upload_multiple_files(
        bucket_name=bucket_name,
        base_path=current_user,
        files=files_to_upload,
        content_type="application/octet-stream"
    )
    
    if not uploaded_results:
        raise HTTPException(status_code=500, detail="文件上传失败")
    
    # 计算整体哈希（所有文件哈希的组合）
    combined_hash = minio_service.calculate_file_hash(
        "".join(sorted(file_hashes)).encode()
    )
    
    # 创建 Skill 记录
    # 存储根路径和文件列表
    root_path = f"{bucket_name}/{current_user}"
    
    skill = Skill(
        skill_name=skill_name,
        slug=slugify(skill_name),
        description=description,
        category_id=category_id,
        project_id=project_id,
        owner_open_id=current_user,
        file_path=root_path,
        file_name=f"{skill_name} (批量上传)",
        file_size=total_size,
        file_hash=combined_hash,
        metadata={
            "is_batch": True,
            "file_count": len(uploaded_results),
            "preserve_structure": preserve_structure,
            "files": [
                {
                    "path": item["relative_path"],
                    "size": item["size"]
                }
                for item in uploaded_results
            ]
        }
    )
    
    db.add(skill)
    db.commit()
    db.refresh(skill)
    
    return {
        "skill_id": skill.id,
        "total_files": len(files),
        "uploaded_files": len(uploaded_results),
        "failed_files": len(files) - len(uploaded_results),
        "file_list": uploaded_results,
        "message": f"成功上传 {len(uploaded_results)} 个文件"
    }

@router.get("/{skill_id}/files")
def list_skill_files(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_open_id)
):
    """获取 Skill 的文件列表（用于批量上传的 Skill）"""
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill 不存在")
    
    # 检查是否是批量上传的 Skill
    if not skill.metadata or not skill.metadata.get("is_batch"):
        raise HTTPException(status_code=400, detail="该 Skill 不是批量上传的")
    
    # 从元数据中获取文件列表
    files = skill.metadata.get("files", [])
    
    # 也可以从 MinIO 实时获取
    bucket_name = skill.file_path.split("/")[0]
    prefix = "/".join(skill.file_path.split("/")[1:])
    
    minio_files = minio_service.list_objects(bucket_name, prefix=prefix)
    
    return {
        "skill_id": skill.id,
        "skill_name": skill.skill_name,
        "total_files": len(files),
        "files": files,
        "minio_files": minio_files
    }

@router.get("/{skill_id}/download-file")
async def download_skill_file(
    skill_id: int,
    file_path: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_open_id)
):
    """下载批量上传 Skill 中的单个文件
    
    Args:
        skill_id: Skill ID
        file_path: 文件相对路径
    """
    from fastapi.responses import StreamingResponse
    
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill 不存在")
    
    # 构建完整路径
    bucket_name = skill.file_path.split("/")[0]
    object_path = f"{skill.owner_open_id}/{file_path}"
    
    # 从 MinIO 下载文件
    file_data = minio_service.download_file(bucket_name, object_path)
    
    if not file_data:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    # 增加下载次数
    skill.download_count += 1
    db.commit()
    
    # 返回文件流
    return StreamingResponse(
        io.BytesIO(file_data),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={os.path.basename(file_path)}"
        }
    )
