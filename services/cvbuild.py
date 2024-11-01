import fitz  # PyMuPDF
import re
from flask import jsonify, request
import services.asst as openai_asst

def extract_work_experience(pdf_path):
    # Открываем PDF файл
    document = fitz.open(pdf_path)
    
    work_experience = []
    
    # Паттерн для поиска раздела "Work Experience"
    experience_pattern = re.compile(r'(?i)(work experience|experience)', re.IGNORECASE)
    
    # Флаг для отслеживания, находимся ли мы в разделе "Work Experience"
    in_experience_section = False

    for page in document:
        text = page.get_text()
        
        # Проверяем, если мы находимся в разделе "Work Experience"
        if experience_pattern.search(text):
            in_experience_section = True
        
        # Если мы нашли раздел "Work Experience", начинаем извлечение
        if in_experience_section:
            # Разделяем текст на строки
            lines = text.split('\n')
            for line in lines:
                # Добавляем только те строки, которые начинаются с "*"
                if line.startswith('•'):
                    work_experience.append(line.strip())

            # Предполагаем, что раздел заканчивается, когда встречаем пустую строку или новый раздел
            if any(not line for line in lines):
                break
    
    document.close()
    
    return work_experience

def upgrade_bullet_points():
    if 'pdf_resume' not in request.files:
        return jsonify({"message": "No file part"}), 400
    
    file = request.files['pdf_resume']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    # Проверка на MIME-тип
    if file.mimetype != 'application/pdf':
        return jsonify({"message": "Invalid file type. Only PDF allowed."}), 400
    
    if file and file.filename.endswith('.pdf'):
        pdf_path = f"resumes/{file.filename}"
        file.save(pdf_path)

        pdf_text = extract_work_experience(pdf_path)
        description = request.form.get('job_vacancy_description', '')
        # tech_skills = request.form.get('technical_skills', '')

        return openai_asst.upgrade_bullet_points(description, '\n'.join(pdf_text))

    return jsonify({"message": "Invalid file type. Only PDF allowed."}), 400