"""
Script para testar conexão com MySQL e criar o banco se necessário
"""
import pymysql
import sys
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'palmeiras')
DB_NAME = os.getenv('DB_NAME', 'api-db')

print("="*60)
print("🔍 TESTANDO CONEXÃO COM MYSQL")
print("="*60)
print(f"Host: {DB_HOST}")
print(f"Port: {DB_PORT}")
print(f"User: {DB_USER}")
print(f"Database: {DB_NAME}")
print()

try:
    # Conectar ao MySQL sem especificar banco
    print("📡 Conectando ao MySQL...")
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )
    print("✅ Conexão bem-sucedida!")
    
    cursor = connection.cursor()
    
    # Verificar se banco existe
    print(f"\n🔍 Verificando se banco '{DB_NAME}' existe...")
    cursor.execute("SHOW DATABASES")
    databases = [db[0] for db in cursor.fetchall()]
    
    if DB_NAME in databases:
        print(f"✅ Banco '{DB_NAME}' já existe!")
    else:
        print(f"⚠️  Banco '{DB_NAME}' não existe. Criando...")
        cursor.execute(f"CREATE DATABASE `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ Banco '{DB_NAME}' criado com sucesso!")
    
    # Conectar ao banco específico
    connection.select_db(DB_NAME)
    
    # Verificar se tabela user_voice_profile existe
    print(f"\n🔍 Verificando tabelas no banco '{DB_NAME}'...")
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    
    if tables:
        print(f"✅ Tabelas encontradas: {', '.join(tables)}")
    else:
        print("⚠️  Nenhuma tabela encontrada. Serão criadas ao iniciar a API.")
    
    cursor.close()
    connection.close()
    
    print("\n" + "="*60)
    print("✅ TESTE CONCLUÍDO - TUDO OK!")
    print("="*60)
    print("\n🚀 Você pode iniciar a API agora com:")
    print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    print()
    
    sys.exit(0)
    
except pymysql.Error as e:
    print(f"\n❌ ERRO DE CONEXÃO: {e}")
    print("\n📋 Verifique:")
    print("   1. MySQL está rodando?")
    print("   2. Credenciais no .env estão corretas?")
    print("   3. Usuário tem permissões adequadas?")
    print()
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    sys.exit(1)
