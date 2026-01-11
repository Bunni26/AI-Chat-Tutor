-- AI Coding Tutor Database Schema

-- Create the database
CREATE DATABASE IF NOT EXISTS ai_coding_tutor;
USE ai_coding_tutor;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB;

-- Topics table
CREATE TABLE topics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topic_name VARCHAR(100) NOT NULL UNIQUE,
    topic_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_topic_name (topic_name)
) ENGINE=InnoDB;

-- Code examples table
CREATE TABLE code_examples (
    id INT AUTO_INCREMENT PRIMARY KEY,
    example_code TEXT NOT NULL,
    language VARCHAR(50) NOT NULL,
    description TEXT,
    topic_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE,
    INDEX idx_language (language),
    INDEX idx_topic_id (topic_id)
) ENGINE=InnoDB;

-- Conversations table
CREATE TABLE conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    conversation_text TEXT NOT NULL,
    conversation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_conversation_date (conversation_date)
) ENGINE=InnoDB;

-- User topics table (for tracking user progress in different topics)
CREATE TABLE user_topics (
    user_id INT NOT NULL,
    topic_id INT NOT NULL,
    topic_progress DECIMAL(5,2) DEFAULT 0.00,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, topic_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE,
    INDEX idx_topic_progress (topic_progress)
) ENGINE=InnoDB;

-- Add some sample data for testing
INSERT INTO topics (topic_name, topic_description) VALUES
('Python Basics', 'Introduction to Python programming language'),
('SQL Fundamentals', 'Basic SQL queries and database operations'),
('Web Development', 'HTML, CSS, and JavaScript basics');

-- Create a test user
INSERT INTO users (username, email, password) VALUES
('testuser', 'test@example.com', 'hashed_password_here'); 