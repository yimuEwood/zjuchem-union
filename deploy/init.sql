-- 初始化数据库结构
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    name VARCHAR(50) NOT NULL,
    department VARCHAR(50) DEFAULT '',
    role VARCHAR(20) DEFAULT '干事',
    phone VARCHAR(20) DEFAULT '',
    email VARCHAR(100) DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    department VARCHAR(50) DEFAULT '',
    assignee VARCHAR(50) DEFAULT '',
    deadline VARCHAR(20) DEFAULT '',
    description TEXT,
    status VARCHAR(20) DEFAULT '待开始',
    progress INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(500) NOT NULL,
    size VARCHAR(20) DEFAULT '',
    department VARCHAR(50) DEFAULT '',
    uploader VARCHAR(50) DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入默认管理员账号 (密码: admin123)
INSERT INTO users (username, hashed_password, name, department, role)
VALUES ('admin', '$2b$12$LJ3m4ys3GZfnYMz8kVsKaOZ5M5wCFDZQFK2rPNVY6XFvFJL.QHvKq', '管理员', '主席团', '部长');

-- 插入示例任务
INSERT INTO tasks (title, department, assignee, deadline, status, progress) VALUES
('撰写化学文化节策划案', '宣传部', '张三', '2026-06-20', '进行中', 60),
('整理上学期活动报销单据', '办公室', '李四', '2026-06-15', '待开始', 0),
('联系化工厂参观事宜', '外联部', '王五', '2026-06-25', '进行中', 30),
('化学竞赛报名统计', '学术部', '赵六', '2026-06-18', '已完成', 100);
