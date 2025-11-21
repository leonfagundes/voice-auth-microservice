-- Script SQL para criar a tabela user_voice_profile
-- Este script é executado automaticamente pelo SQLAlchemy, mas está aqui para referência

CREATE DATABASE IF NOT EXISTS auth_voice_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE auth_voice_db;

-- Tabela de perfis de voz
CREATE TABLE IF NOT EXISTS user_voice_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL UNIQUE,
    embedding JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Exemplo de consulta para ver perfis
-- SELECT id, user_id, JSON_LENGTH(embedding) as embedding_dimension, created_at FROM user_voice_profile;
