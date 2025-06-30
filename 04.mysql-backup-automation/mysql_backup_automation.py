import os
import schedule
import time
import mysql.connector

class BackupAutomation:
    def __init__(self):
        # DB 설정
        self.db_config = {
            "host": "localhost",
            "user": "root", 
            "password": "your_password"
        }
        
        # 백업 경로
        self.locations = {
            "hongdae": "C:/backup/hongdae",
            "busan": "C:/backup/busan",
            "incheon": "C:/backup/incheon"
        }
    
    def run_sql_file(self, database, file_path):
        """SQL 파일 실행"""
        conn = mysql.connector.connect(database=database, **self.db_config)
        cursor = conn.cursor()
        
        with open(file_path, 'r', encoding='utf-8') as file:
            sql = file.read()
            for command in sql.split(';'):
                if command.strip():
                    cursor.execute(command)
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def process_backups(self):
        """백업 파일 처리"""
        print(f"🔄 백업 시작: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        for db_name, path in self.locations.items():
            if not os.path.exists(path):
                continue
                
            sql_files = [f for f in os.listdir(path) if f.endswith('.sql')]
            
            for file_name in sql_files:
                try:
                    self.run_sql_file(db_name, os.path.join(path, file_name))
                    print(f"✅ {db_name}/{file_name}")
                except Exception as e:
                    print(f"❌ {db_name}/{file_name}: {e}")
        
        print(f"✅ 백업 완료: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def start_scheduler(self):
        """매일 오전 9시 자동 실행"""
        schedule.every().day.at("09:00").do(self.process_backups)
        print("📅 스케줄러 시작 - 매일 09:00에 자동 실행")
        
        while True:
            schedule.run_pending()
            time.sleep(60)

# 실행
if __name__ == "__main__":
    backup = BackupAutomation()
    
    print("1️⃣ 지금 실행")
    print("2️⃣ 스케줄러 시작")
    
    if input("선택: ") == "1":
        backup.process_backups()
    else:
        backup.start_scheduler()