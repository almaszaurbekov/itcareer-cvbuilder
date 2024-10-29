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
        
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=job_vacancy_description
        )

        f_run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=asst_id
        )

        time.sleep(10)

        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=resume_bullet_points
        )

        l_run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=asst_id
        )

        time.sleep(10)

        messages = client.beta.threads.messages.list(thread_id=thread.id, run_id=l_run.id)
        return jsonify({'message': messages.data[0].content[0].text.value}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'message': "Something went wrong."}), 402