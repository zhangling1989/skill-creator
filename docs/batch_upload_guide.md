# 批量上传文件夹功能使用指南

## 功能概述

Skill Hub 支持批量上传文件夹及其所有内容，并保持原有的目录结构。上传后的文件会按照用户本地的目录层级存储在 MinIO 中。

## 存储结构

### 单文件上传
```
bucket_name (项目名称)
└── open_id (用户ID)
    └── skill.md
```

### 批量上传（保持目录结构）
```
bucket_name (项目名称)
└── open_id (用户ID)
    ├── folder1/
    │   ├── file1.md
    │   └── file2.md
    ├── folder2/
    │   └── subfolder/
    │       └── file3.md
    └── root_file.md
```

## API 接口

### 1. 批量上传文件/文件夹

**端点**: `POST /api/v1/skills/batch-upload`

**请求类型**: `multipart/form-data`

**参数**:
- `files`: 文件列表（必填，支持多文件）
- `skill_name`: Skill 名称（必填）
- `description`: Skill 描述（可选）
- `category_id`: 分类 ID（默认 1）
- `project_id`: 项目 ID（默认 1）
- `preserve_structure`: 是否保持目录结构（默认 true）

**响应示例**:
```json
{
  "skill_id": 123,
  "total_files": 10,
  "uploaded_files": 10,
  "failed_files": 0,
  "file_list": [
    {
      "path": "project-name/open_id/folder1/file1.md",
      "relative_path": "folder1/file1.md",
      "size": 1024
    },
    {
      "path": "project-name/open_id/folder2/subfolder/file3.md",
      "relative_path": "folder2/subfolder/file3.md",
      "size": 2048
    }
  ],
  "message": "成功上传 10 个文件"
}
```

### 2. 获取 Skill 文件列表

**端点**: `GET /api/v1/skills/{skill_id}/files`

**响应示例**:
```json
{
  "skill_id": 123,
  "skill_name": "我的项目文档",
  "total_files": 10,
  "files": [
    {
      "path": "folder1/file1.md",
      "size": 1024
    },
    {
      "path": "folder2/subfolder/file3.md",
      "size": 2048
    }
  ],
  "minio_files": [
    "open_id/folder1/file1.md",
    "open_id/folder2/subfolder/file3.md"
  ]
}
```

### 3. 下载单个文件

**端点**: `GET /api/v1/skills/{skill_id}/download-file?file_path=folder1/file1.md`

**参数**:
- `file_path`: 文件相对路径（必填）

**响应**: 文件流下载

## 使用示例

### Python 客户端示例

```python
import requests

# 批量上传文件夹
def upload_folder(folder_path, skill_name, project_id=1, category_id=1):
    url = "http://localhost:8000/api/v1/skills/batch-upload"
    
    files = []
    file_handles = []
    
    # 遍历文件夹
    import os
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            # 计算相对路径
            relative_path = os.path.relpath(file_path, folder_path)
            
            # 打开文件
            f = open(file_path, 'rb')
            file_handles.append(f)
            files.append(('files', (relative_path, f, 'application/octet-stream')))
    
    # 表单数据
    data = {
        'skill_name': skill_name,
        'description': f'批量上传: {skill_name}',
        'category_id': category_id,
        'project_id': project_id,
        'preserve_structure': True
    }
    
    try:
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        result = response.json()
        print(f"上传成功！Skill ID: {result['skill_id']}")
        print(f"上传文件数: {result['uploaded_files']}/{result['total_files']}")
        return result
    finally:
        # 关闭所有文件句柄
        for f in file_handles:
            f.close()

# 使用示例
upload_folder('./my-project', '我的项目文档', project_id=1, category_id=1)
```

### cURL 示例

```bash
# 上传多个文件（保持目录结构）
curl -X POST "http://localhost:8000/api/v1/skills/batch-upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "files=@folder1/file1.md" \
  -F "files=@folder1/file2.md" \
  -F "files=@folder2/subfolder/file3.md" \
  -F "skill_name=我的项目文档" \
  -F "description=完整的项目文档" \
  -F "category_id=1" \
  -F "project_id=1" \
  -F "preserve_structure=true"

# 获取文件列表
curl -X GET "http://localhost:8000/api/v1/skills/123/files" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 下载单个文件
curl -X GET "http://localhost:8000/api/v1/skills/123/download-file?file_path=folder1/file1.md" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o downloaded_file.md
```

### JavaScript/TypeScript 示例

```typescript
async function uploadFolder(files: FileList, skillName: string) {
  const formData = new FormData();
  
  // 添加所有文件（浏览器会保持目录结构）
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    // webkitRelativePath 包含完整的相对路径
    formData.append('files', file, file.webkitRelativePath || file.name);
  }
  
  formData.append('skill_name', skillName);
  formData.append('description', '批量上传');
  formData.append('category_id', '1');
  formData.append('project_id', '1');
  formData.append('preserve_structure', 'true');
  
  const response = await fetch('http://localhost:8000/api/v1/skills/batch-upload', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });
  
  const result = await response.json();
  console.log('上传结果:', result);
  return result;
}

// HTML 中使用文件夹选择器
// <input type="file" webkitdirectory directory multiple onchange="handleFolderSelect(event)" />

function handleFolderSelect(event: Event) {
  const input = event.target as HTMLInputElement;
  if (input.files) {
    uploadFolder(input.files, '我的项目');
  }
}
```

## 前端实现示例

### React 组件

```tsx
import React, { useState } from 'react';
import axios from 'axios';

const FolderUploader: React.FC = () => {
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleFolderUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    const formData = new FormData();
    
    // 添加所有文件
    Array.from(files).forEach(file => {
      // @ts-ignore - webkitRelativePath 不在标准类型中
      const relativePath = file.webkitRelativePath || file.name;
      formData.append('files', file, relativePath);
    });

    formData.append('skill_name', '我的项目文档');
    formData.append('description', '批量上传的项目文档');
    formData.append('category_id', '1');
    formData.append('project_id', '1');
    formData.append('preserve_structure', 'true');

    setUploading(true);

    try {
      const response = await axios.post(
        'http://localhost:8000/api/v1/skills/batch-upload',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }
      );

      setResult(response.data);
      alert(`上传成功！共上传 ${response.data.uploaded_files} 个文件`);
    } catch (error) {
      console.error('上传失败:', error);
      alert('上传失败，请重试');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h2>批量上传文件夹</h2>
      <input
        type="file"
        // @ts-ignore
        webkitdirectory="true"
        directory="true"
        multiple
        onChange={handleFolderUpload}
        disabled={uploading}
      />
      
      {uploading && <p>上传中...</p>}
      
      {result && (
        <div>
          <h3>上传结果</h3>
          <p>Skill ID: {result.skill_id}</p>
          <p>成功: {result.uploaded_files} / {result.total_files}</p>
          <p>失败: {result.failed_files}</p>
          
          <h4>文件列表:</h4>
          <ul>
            {result.file_list.map((file: any, index: number) => (
              <li key={index}>
                {file.relative_path} ({file.size} bytes)
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FolderUploader;
```

## 数据库存储

批量上传的 Skill 在数据库中的 `metadata` 字段会存储以下信息：

```json
{
  "is_batch": true,
  "file_count": 10,
  "preserve_structure": true,
  "files": [
    {
      "path": "folder1/file1.md",
      "size": 1024
    },
    {
      "path": "folder2/subfolder/file3.md",
      "size": 2048
    }
  ]
}
```

## 注意事项

1. **文件大小限制**: 单个文件不能超过配置的最大大小（默认 10MB）
2. **文件类型**: 可以通过配置限制允许的文件扩展名
3. **路径处理**: 自动处理 Windows 和 Unix 路径分隔符
4. **权限控制**: 只有文件所有者可以删除或修改
5. **目录结构**: 设置 `preserve_structure=false` 可以扁平化上传（所有文件放在同一目录）

## 性能优化建议

1. 对于大量文件，建议分批上传
2. 使用异步上传提高用户体验
3. 添加上传进度显示
4. 实现断点续传功能（可选）
