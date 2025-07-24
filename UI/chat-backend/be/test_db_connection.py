#!/usr/bin/env python3
"""
Test script to verify MySQL database connection with root user and no password
"""

import os
import sys
from dotenv import load_dotenv
import mysql.connector
from sqlalchemy import create_engine, text

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def test_mysql_connector():
    """Test connection using mysql-connector-python"""
    print("🔍 Testing MySQL connection with mysql-connector-python...")
    
    try:
        # Get database configuration
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = int(os.getenv("DB_PORT", "3306"))
        DB_USER = os.getenv("DB_USER", "root")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "")
        DB_NAME = os.getenv("DB_NAME", "khoa_luan")
        
        print(f"📋 Connection details:")
        print(f"   Host: {DB_HOST}")
        print(f"   Port: {DB_PORT}")
        print(f"   User: {DB_USER}")
        print(f"   Password: {'(empty)' if not DB_PASSWORD else '(set)'}")
        print(f"   Database: {DB_NAME}")
        
        # Test connection without database first
        connection_params = {
            'host': DB_HOST,
            'port': DB_PORT,
            'user': DB_USER
        }
        if DB_PASSWORD:
            connection_params['password'] = DB_PASSWORD
            
        connection = mysql.connector.connect(**connection_params)
        print("✅ Successfully connected to MySQL server!")
        
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"📊 MySQL version: {version[0]}")
        
        # Test database creation/access
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        print(f"✅ Database '{DB_NAME}' is accessible!")
        
        cursor.close()
        connection.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ MySQL connection failed: {err}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_sqlalchemy():
    """Test connection using SQLAlchemy"""
    print("\n🔍 Testing SQLAlchemy connection...")
    
    try:
        from app.database.base import DATABASE_URL, engine
        
        print(f"📋 Database URL: {DATABASE_URL}")
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            print(f"✅ SQLAlchemy connection successful!")
            print(f"📊 MySQL version: {version}")
            return True
            
    except Exception as e:
        print(f"❌ SQLAlchemy connection failed: {e}")
        return False

def test_database_initialization():
    """Test database initialization"""
    print("\n🔍 Testing database initialization...")
    
    try:
        from app.database.init_db import init_database
        
        result = init_database()
        if result:
            print("✅ Database initialization successful!")
            return True
        else:
            print("❌ Database initialization failed!")
            return False
            
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting MySQL connection tests...\n")
    
    # Test 1: Direct MySQL connection
    mysql_ok = test_mysql_connector()
    
    # Test 2: SQLAlchemy connection
    sqlalchemy_ok = test_sqlalchemy()
    
    # Test 3: Database initialization
    init_ok = test_database_initialization()
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY:")
    print(f"   MySQL Connector: {'✅ PASS' if mysql_ok else '❌ FAIL'}")
    print(f"   SQLAlchemy:      {'✅ PASS' if sqlalchemy_ok else '❌ FAIL'}")
    print(f"   DB Initialization: {'✅ PASS' if init_ok else '❌ FAIL'}")
    
    if all([mysql_ok, sqlalchemy_ok, init_ok]):
        print("\n🎉 All tests passed! Backend is ready to connect to MySQL.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check your MySQL configuration.")
        return 1

if __name__ == "__main__":
    exit(main())