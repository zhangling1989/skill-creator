-- Skill Hub 平台数据库建表脚本
-- 数据库: MySQL 8.0+ / PostgreSQL 12+

-- 1. 用户表
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    open_id VARCHAR(128) UNIQUE NOT NULL COMMENT 'SSO系统的open_id',
    username VARCHAR(64) NOT NULL COMMENT '用户名',
    email VARCHAR(128) COMMENT '邮箱',
    avatar_url VARCHAR(512) COMMENT '头像URL',
    status TINYINT DEFAULT 1 COMMENT '状态: 1-正常, 0-禁用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_open_id (open_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 2. 项目表
CREATE TABLE projects (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    project_name VARCHAR(128) UNIQUE NOT NULL COMMENT '项目名称(对应MinIO桶名)',
    display_name VARCHAR(256) NOT NULL COMMENT '项目显示名称',
    description TEXT COMMENT '项目描述',
    owner_id BIGINT NOT NULL COMMENT '项目所有者ID',
    bucket_name VARCHAR(128) UNIQUE NOT NULL COMMENT 'MinIO桶名',
    is_public TINYINT DEFAULT 0 COMMENT '是否公开: 1-公开, 0-私有',
    status TINYINT DEFAULT 1 COMMENT '状态: 1-正常, 0-禁用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_owner_id (owner_id),
    INDEX idx_bucket_name (bucket_name),
    INDEX idx_status (status),
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目表';

-- 3. Skill分类表
CREATE TABLE skill_categories (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(64) UNIQUE NOT NULL COMMENT '分类名称',
    parent_id BIGINT DEFAULT 0 COMMENT '父分类ID, 0表示顶级分类',
    description VARCHAR(512) COMMENT '分类描述',
    icon VARCHAR(256) COMMENT '分类图标',
    sort_order INT DEFAULT 0 COMMENT '排序顺序',
    status TINYINT DEFAULT 1 COMMENT '状态: 1-启用, 0-禁用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_parent_id (parent_id),
    INDEX idx_status (status),
    INDEX idx_sort_order (sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Skill分类表';

-- 4. Skill表 (核心表)
CREATE TABLE skills (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    skill_name VARCHAR(256) NOT NULL COMMENT 'Skill名称',
    slug VARCHAR(256) NOT NULL COMMENT 'URL友好的标识符',
    description TEXT COMMENT 'Skill描述',
    category_id BIGINT NOT NULL COMMENT '分类ID',
    project_id BIGINT NOT NULL COMMENT '所属项目ID',
    owner_open_id VARCHAR(128) NOT NULL COMMENT '上传者的open_id',
    file_path VARCHAR(1024) NOT NULL COMMENT 'MinIO中的完整路径',
    file_name VARCHAR(256) NOT NULL COMMENT '文件名',
    file_size BIGINT COMMENT '文件大小(字节)',
    file_hash VARCHAR(64) COMMENT '文件MD5/SHA256哈希值',
    version VARCHAR(32) DEFAULT '1.0.0' COMMENT '版本号',
    tags JSON COMMENT '标签数组',
    skill_metadata JSON COMMENT '其他元数据',
    price DECIMAL(10,2) DEFAULT 0.00 COMMENT 'Skill价格(元)',
    pricing_model VARCHAR(32) DEFAULT 'per_use' COMMENT '计费模式: free-免费, per_use-按次, subscription-订阅',
    view_count INT DEFAULT 0 COMMENT '浏览次数',
    download_count INT DEFAULT 0 COMMENT '下载次数',
    star_count INT DEFAULT 0 COMMENT '收藏次数',
    usage_count INT DEFAULT 0 COMMENT '使用次数',
    is_public TINYINT DEFAULT 1 COMMENT '是否公开: 1-公开, 0-私有',
    status TINYINT DEFAULT 1 COMMENT '状态: 1-正常, 0-已删除, 2-审核中',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_skill_name (skill_name),
    INDEX idx_slug (slug),
    INDEX idx_category_id (category_id),
    INDEX idx_project_id (project_id),
    INDEX idx_owner_open_id (owner_open_id),
    INDEX idx_file_hash (file_hash),
    INDEX idx_created_at (created_at DESC),
    INDEX idx_project_owner (project_id, owner_open_id),
    INDEX idx_category_status (category_id, status),
    INDEX idx_owner_created (owner_open_id, created_at DESC),
    FOREIGN KEY (category_id) REFERENCES skill_categories(id) ON DELETE RESTRICT,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Skill表';

-- 5. Skill版本历史表
CREATE TABLE skill_versions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    skill_id BIGINT NOT NULL COMMENT 'Skill ID',
    version VARCHAR(32) NOT NULL COMMENT '版本号',
    file_path VARCHAR(1024) NOT NULL COMMENT '该版本的文件路径',
    file_hash VARCHAR(64) COMMENT '文件哈希值',
    change_log TEXT COMMENT '变更日志',
    created_by VARCHAR(128) NOT NULL COMMENT '创建者open_id',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_skill_id (skill_id),
    INDEX idx_version (version),
    INDEX idx_created_at (created_at DESC),
    UNIQUE KEY unique_skill_version (skill_id, version),
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Skill版本历史表';

-- 6. Skill收藏表
CREATE TABLE skill_stars (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    skill_id BIGINT NOT NULL COMMENT 'Skill ID',
    user_open_id VARCHAR(128) NOT NULL COMMENT '用户open_id',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
    INDEX idx_skill_id (skill_id),
    INDEX idx_user_open_id (user_open_id),
    UNIQUE KEY unique_star (skill_id, user_open_id),
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Skill收藏表';

-- 7. Skill使用记录表
CREATE TABLE skill_usage_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    skill_id BIGINT NOT NULL COMMENT 'Skill ID',
    user_open_id VARCHAR(128) NOT NULL COMMENT '使用者open_id',
    agent_id VARCHAR(128) COMMENT 'Agent ID（调用方标识）',
    usage_type VARCHAR(32) DEFAULT 'agent_call' COMMENT '使用类型: agent_call, api_call',
    charge_amount DECIMAL(10,2) DEFAULT 0.00 COMMENT '本次收费金额',
    status TINYINT DEFAULT 1 COMMENT '状态: 1-成功, 0-失败, 2-待支付',
    request_data JSON COMMENT '请求数据',
    response_data JSON COMMENT '响应数据',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '使用时间',
    INDEX idx_skill_id (skill_id),
    INDEX idx_user_open_id (user_open_id),
    INDEX idx_agent_id (agent_id),
    INDEX idx_created_at (created_at DESC),
    INDEX idx_user_created (user_open_id, created_at DESC),
    INDEX idx_skill_created (skill_id, created_at DESC),
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Skill使用记录表';

-- 8. 用户钱包表
CREATE TABLE user_wallets (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_open_id VARCHAR(128) UNIQUE NOT NULL COMMENT '用户open_id',
    balance DECIMAL(10,2) DEFAULT 0.00 COMMENT '余额',
    frozen_balance DECIMAL(10,2) DEFAULT 0.00 COMMENT '冻结金额',
    total_income DECIMAL(10,2) DEFAULT 0.00 COMMENT '总收入',
    total_expense DECIMAL(10,2) DEFAULT 0.00 COMMENT '总支出',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_user_open_id (user_open_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户钱包表';

-- 9. 钱包交易记录表
CREATE TABLE wallet_transactions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    transaction_no VARCHAR(64) UNIQUE NOT NULL COMMENT '交易流水号',
    user_open_id VARCHAR(128) NOT NULL COMMENT '用户open_id',
    transaction_type VARCHAR(32) NOT NULL COMMENT '交易类型: recharge-充值, withdraw-提现, income-收入, expense-支出',
    amount DECIMAL(10,2) NOT NULL COMMENT '交易金额',
    balance_before DECIMAL(10,2) NOT NULL COMMENT '交易前余额',
    balance_after DECIMAL(10,2) NOT NULL COMMENT '交易后余额',
    related_type VARCHAR(32) COMMENT '关联类型: skill_usage, skill_sale',
    related_id BIGINT COMMENT '关联ID',
    description VARCHAR(512) COMMENT '交易描述',
    status TINYINT DEFAULT 1 COMMENT '状态: 1-成功, 0-失败, 2-处理中',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '交易时间',
    INDEX idx_transaction_no (transaction_no),
    INDEX idx_user_open_id (user_open_id),
    INDEX idx_transaction_type (transaction_type),
    INDEX idx_related (related_type, related_id),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='钱包交易记录表';

-- 10. Skill评论表
CREATE TABLE skill_comments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    skill_id BIGINT NOT NULL COMMENT 'Skill ID',
    user_open_id VARCHAR(128) NOT NULL COMMENT '评论者open_id',
    parent_id BIGINT DEFAULT 0 COMMENT '父评论ID, 0表示顶级评论',
    content TEXT NOT NULL COMMENT '评论内容',
    rating TINYINT COMMENT '评分(1-5)',
    status TINYINT DEFAULT 1 COMMENT '状态: 1-正常, 0-已删除',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_skill_id (skill_id),
    INDEX idx_user_open_id (user_open_id),
    INDEX idx_parent_id (parent_id),
    INDEX idx_created_at (created_at DESC),
    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Skill评论表';

-- 11. 操作日志表
CREATE TABLE operation_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_open_id VARCHAR(128) NOT NULL COMMENT '操作者open_id',
    operation_type VARCHAR(32) NOT NULL COMMENT '操作类型: upload, download, delete, update',
    resource_type VARCHAR(32) NOT NULL COMMENT '资源类型: skill, project',
    resource_id BIGINT NOT NULL COMMENT '资源ID',
    ip_address VARCHAR(64) COMMENT 'IP地址',
    user_agent VARCHAR(512) COMMENT '用户代理',
    details JSON COMMENT '操作详情',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
    INDEX idx_user_open_id (user_open_id),
    INDEX idx_operation_type (operation_type),
    INDEX idx_resource (resource_type, resource_id),
    INDEX idx_created_at (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志表';

-- 插入默认分类数据
INSERT INTO skill_categories (category_name, parent_id, description, sort_order) VALUES
('开发工具', 0, '开发相关的技能', 1),
('数据分析', 0, '数据分析相关的技能', 2),
('人工智能', 0, 'AI相关的技能', 3),
('运维部署', 0, '运维和部署相关的技能', 4),
('测试工具', 0, '测试相关的技能', 5),
('其他', 0, '其他类型的技能', 99);
