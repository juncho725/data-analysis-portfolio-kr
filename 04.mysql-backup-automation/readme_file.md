# 🚀 MySQL 백업 자동화

> **매일 받는 SQL 백업파일을 자동으로 로컬 DB에 적용**

## ✨ 주요 기능

- **자동 스케줄링**: 매일 오전 9시 자동 실행
- **다중 DB 지원**: 여러 지점 데이터베이스 동시 처리  
- **에러 처리**: 파일별 개별 처리로 안정성 확보
- **즉시 실행**: 테스트용 수동 실행 가능

## 🚀 사용법

### 1. 설치
```bash
pip install mysql-connector-python schedule
```

### 2. 설정 변경
```python
# 코드에서 수정
self.db_config = {
    "host": "localhost",
    "user": "root", 
    "password": "실제_비밀번호"  # 여기 변경
}

self.locations = {
    "hongdae": "C:/backup/hongdae",    # 실제 경로로 변경
    "busan": "C:/backup/busan",
    "incheon": "C:/backup/incheon"
}
```

### 3. 실행
```bash
python backup.py
```

## 📊 실행 결과
```
🔄 백업 시작: 2024-01-15 09:00:01
✅ hongdae/backup_20240115.sql
✅ busan/data_backup.sql  
❌ incheon/corrupt_file.sql: Syntax error
✅ 백업 완료: 2024-01-15 09:03:22
```

## 🎯 핵심 코드

### 자동 스케줄링
```python
schedule.every().day.at("09:00").do(self.process_backups)
while True:
    schedule.run_pending()
    time.sleep(60)
```

### SQL 파일 실행
```python
with open(file_path, 'r', encoding='utf-8') as file:
    sql = file.read()
    for command in sql.split(';'):
        if command.strip():
            cursor.execute(command)
```

### 에러 처리
```python
try:
    self.run_sql_file(db_name, file_path)
    print(f"✅ {db_name}/{file_name}")
except Exception as e:
    print(f"❌ {db_name}/{file_name}: {e}")
```

## 💡 실무 효과

| 구분 | 기존 | 자동화 후 |
|------|------|----------|
| **시간** | 30분/일 | 2분/일 |
| **실수** | 가끔 발생 | 없음 |
| **모니터링** | 수동 | 자동 |

## 🔧 확장 방법

**새 지점 추가**
```python
self.locations["gangnam"] = "C:/backup/gangnam"
```

**다른 시간 설정**  
```python
schedule.every().day.at("21:00").do(self.process_backups)  # 오후 9시
schedule.every().monday.do(self.process_backups)           # 매주 월요일
```

---

> **개발 기간**: 1일 | **코드 라인**: 50줄 | **자동화 효과**: 93% 시간 절약