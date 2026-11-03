from fastapi import FastAPI, Form, File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
import uuid

class DeleteFileRequest(BaseModel):
    file_path: str  # Например: "shouldn't cry/Shoudln't cry.wav"

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:80",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Используем ОДНУ общую директорию для чтения и записи
BASE_DIR = "./storage" 

# Вспомогательная функция для поиска имени файла по UUID
def find_file_by_id(folder: str, file_id: str):
    safe_folder = os.path.join(BASE_DIR, folder)
    if not os.path.exists(safe_folder):
        return None, None
    for filename in os.listdir(safe_folder):
        file_path = os.path.join(safe_folder, filename)
        if os.path.isfile(file_path):
            # Генерируем детерминированный UUID на основе относительного пути
            rel_path = f"{folder}/{filename}"
            generated_id = str(uuid.uuid5(uuid.NAMESPACE_URL, rel_path))
            
            if generated_id == file_id:
                return file_path, filename
                
    return None, None

# Вспомогательная функция для поиска имени папки по её UUID
def find_folder_by_id(folder_id: str):
    if not os.path.exists(BASE_DIR):
        return None
        
    for item in os.listdir(BASE_DIR):
        item_path = os.path.join(BASE_DIR, item)
        if os.path.isdir(item_path):
            generated_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"folder:{item}"))
            if generated_id == folder_id:
                return item
                
    return None

@app.get("/")
def read_root():
    return {"message": 'Привет, бэкенд работает!'}

@app.get("/api/folders")
def get_folders():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR, exist_ok=True)
        
    folders_list = []
    for item in os.listdir(BASE_DIR):
        item_path = os.path.join(BASE_DIR, item)
        # Проверяем, что это именно папка
        if os.path.isdir(item_path):
            # Генерируем детерминированный UUID для папки
            folder_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"folder:{item}"))
            folders_list.append({
                "id": folder_id,
                "name": item
            })
            
    return {"folders": folders_list}

@app.get("/api/files/{folder}")
def get_files(folder: str):
    safe_folder = os.path.join(BASE_DIR, folder)
    if not os.path.exists(safe_folder):
        return {"files": []}
        
    files_list = []
    for filename in os.listdir(safe_folder):
        file_path = os.path.join(safe_folder, filename)
        if os.path.isfile(file_path):
            rel_path = f"{folder}/{filename}"
            # Создаем уникальный ID для каждого файла
            file_id = str(uuid.uuid5(uuid.NAMESPACE_URL, rel_path))
            
            files_list.append({
                "id": file_id,
                "name": filename
            })
            
    return {"files": files_list}

# Рекурсивное удаление папки со всем содержимым по UUID
@app.delete("/api/folders/{folder_id}")
def delete_folder(folder_id: str):
    folder_name = find_folder_by_id(folder_id)
    
    if not folder_name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Папка не найдена"
        )
        
    folder_path = os.path.abspath(os.path.join(BASE_DIR, folder_name))
    
    # Дополнительная защита от выхода за пределы хранилища
    if not folder_path.startswith(os.path.abspath(BASE_DIR)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен"
        )
        
    try:
        # shutil.rmtree рекурсивно удаляет папку и все файлы/подпапки внутри нее
        shutil.rmtree(folder_path)
        return {"status": "success", "message": f"Папка {folder_name} и её содержимое успешно удалены"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Не удалось удалить папку: {str(e)}"
        )

@app.post("/api/upload")
async def upload_file(
    folder: str = Form(...),       # Имя папки, куда льем файл (например, "photos" или "ableton/project_v1")
    file: UploadFile = File(...)   # Сам файл
):
    try:
        # 1. Формируем путь к целевой папке и создаем её (вместе с родительскими), если её нет
        target_dir = os.path.abspath(os.path.join(BASE_DIR, folder))
        os.makedirs(target_dir, exist_ok=True)
        
        # 2. Формируем полный путь к будущему файлу
        file_path = os.path.join(target_dir, file.filename)
        
        # 3. Сохраняем файл на диск потоково
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 4. Возвращаем успешный ответ (можно сразу вернуть сгенерированный ID)
        rel_path = f"{folder}/{file.filename}"
        file_id = str(uuid.uuid5(uuid.NAMESPACE_URL, rel_path))
        
        return {
            "status": "success",
            "file": {
                "id": file_id,
                "name": file.filename
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Не удалось загрузить файл: {str(e)}"
        )

@app.delete("/api/files/{folder}/{file_id}")
def delete_file(folder: str, file_id: str):
    # Ищем реальный файл на диске по переданному UUID
    file_path, filename = find_file_by_id(folder, file_id)
    
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Файл не найден"
        )
        
    try:
        os.remove(file_path)
        return {"status": "success", "message": f"Файл {filename} успешно удален"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка удаления: {str(e)}"
        )