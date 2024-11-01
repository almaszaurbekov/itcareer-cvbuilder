from openai import OpenAI
from services.config import asst_id, open_api_key
import time
from flask import jsonify

client = OpenAI(api_key=open_api_key)

def check_assistant_exists():
    try:
        response = client.beta.assistants.retrieve(asst_id)
        return True if response else False
    except Exception as e:
        print(f"An error occurred while checking the assistant: {e}", file=sys.stderr)
        return False

def upgrade_bullet_points(resume_bullet_points, job_vacancy_description):
    try:
        thread = client.beta.threads.create()

        content = f"1. JOB DESCRIPTION:\n {job_vacancy_description}\n 2. CANDIDATE'S BULLET POINTS:\n {resume_bullet_points}"
        
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=content
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=asst_id
        )

        time.sleep(10)

        messages = client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)
        return jsonify({'message': messages.data[0].content[0].text.value}), 200

    except Exception as e:
        print(str(e))
        return jsonify({'message': "Something went wrong."}), 402