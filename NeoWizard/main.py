import base64
import csv
import difflib
import glob
import io
import json
import os
import random
import subprocess
import tempfile
import traceback
import uuid
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Callable

import openai
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import models, ocr_client
from tortoise.contrib.fastapi import register_tortoise
from pydantic import BaseModel
from solve_gpt_api.models import Question

ROOT_PATH = "/solvegpt/api/v1"
class DATA(BaseModel):
    LanguageList:list
    type:int
def read_path(path: str, encoding="utf-8") -> str:
    return Path(path).read_text(encoding=encoding)


app = FastAPI()
app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"],
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

openai_config = json.loads(read_path("/root/solvegpt/openai_config.json"))
print(openai_config['api_key'])
openai.api_key = openai_config["api_key"]
openai.api_base = openai_config["base_url"]


class ResponseBean:
    def __init__(self, success, message: str, data):
        self.success = success
        self.message = message
        self.data = data

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def success(msg="", data=None) -> dict:
        return ResponseBean(True, msg, data).to_dict()

    @staticmethod
    def fail(msg, data=None) -> dict:
        return ResponseBean(False, msg, data).to_dict()


def generate_accuracy():
    accuracy_range = None
    rand_num = random.uniform(0, 1)

    if rand_num <= 0.9:
        accuracy_range = (90, 99)
    elif 0.9 < rand_num <= 0.98:
        accuracy_range = (80, 89)
    else:
        accuracy_range = (0, 79)

    return random.randint(accuracy_range[0], accuracy_range[1])


def log_endpoint_data(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        time_format = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{time_format}] Params: {kwargs}")

        response = await func(*args, **kwargs)

        response_data = {
            "status_code": response.status_code,
        }
        try:
            response_content = response.body
            response_data["body"] = json.loads(response_content)
        except (json.JSONDecodeError, AttributeError):
            pass

        time_format = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{time_format}] Response:", response_data)

        return response

    return wrapper


def split_string(input_str):
    if len(input_str) <= 600:
        return [input_str]

    max_length = 500
    sentences = input_str.split("\n")
    result = []

    temp_str = ""
    for sentence in sentences:
        if len(temp_str) + len(sentence) + 1 <= max_length:
            temp_str += sentence + "\n"
        else:
            result.append(temp_str.strip())
            temp_str = sentence + "\n"

    result.append(temp_str.strip())
    return result


def tencent_ocr(img_base64):
    cred = credential.Credential(
        "", ""
    )
    httpProfile = HttpProfile()
    httpProfile.endpoint = "ocr.tencentcloudapi.com"
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = ocr_client.OcrClient(cred, "", clientProfile)
    client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)
    req = models.GeneralAccurateOCRRequest()
    params = {"ImageBase64": img_base64}
    req.from_json_string(json.dumps(params))
    resp = client.GeneralAccurateOCR(req)
    return resp.TextDetections


def create_pdf(question: Question, pdf_name):
    latex_content = read_path("tex_template/header.tex")

    definition_template = read_path("tex_template/definition.tex")
    theorem_template = read_path("tex_template/theorem.tex")
    question_template = read_path("tex_template/question.tex")

    frame_break_template = read_path("tex_template/frame_break.tex")
    latex_footer = read_path("tex_template/footer.tex")

    try:
        definition_json = json.loads(question.definition.replace("\\", "\\\\"))
    except Exception as e:
        print(e)
        definition_json = [
            {
                "name": "Json Error",
                "content": "An error occured while handling definitions.\n"
                + question.definition,
            }
        ]

    for definition in definition_json:
        latex_content += definition_template % (
            definition["name"],
            definition["content"],
        )

    try:
        theorem_json = json.loads(question.theorem.replace("\\", "\\\\"))
    except Exception as e:
        print(e)
        theorem_json = [
            {
                "name": "Json Error",
                "content": "An error occured while handling theorems.\n"
                + question.theorem,
            }
        ]

    for theorem in theorem_json:
        latex_content += theorem_template % (theorem["name"], theorem["content"])

    answer_split_list = split_string(question.answer)
    if len(answer_split_list) <= 1:
        latex_content += question_template % (question.question, question.answer)
    else:
        answer_break_str = ""
        for answer_slice in answer_split_list:
            answer_break_str += answer_slice
            answer_break_str += "\n"
            answer_break_str += frame_break_template
            answer_break_str += "\n"
        latex_content += question_template % (question.question, answer_break_str)

    latex_content += latex_footer

    with tempfile.TemporaryDirectory() as tempdir:
        tex_file_path = os.path.join(tempdir, f"{pdf_name}.tex")
        with open(tex_file_path, "w", encoding="utf-8") as f:
            f.write(latex_content)

        cmd = f"xelatex -interaction=nonstopmode {tex_file_path}"
        subprocess.call(
            cmd,
            shell=True,
            cwd=tempdir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )

        pdf_file_path = os.path.join(tempdir, f"{pdf_name}.pdf")
        with open(pdf_file_path, "rb") as f:
            pdf_data = f.read()

        with open(f"static/pdfs/{pdf_name}.pdf", "wb") as f:
            f.write(pdf_data)

        for filename in glob.glob(os.path.join(tempdir, f"{pdf_name}.*")):
            os.remove(filename)


def get_openai_answer(question, model,system_prompt):
    message_content = [{"role": "system", "content": system_prompt}]

    # generate definition
    print("generating definition...")
    message_content.append(
        {"role": "user", "content": openai_config["def_prompt"] % (question)}
    )

    completion = openai.ChatCompletion.create(
        model=model,
        messages=message_content,
        temperature=0.8,
    )

    def_answer = completion.choices[0].message.content
    message_content.append({"role": "assistant", "content": def_answer})

    # generate theorem
    print("generating theorem...")
    message_content.append({"role": "user", "content": openai_config["theorem_prompt"]})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=message_content,
        temperature=0.8,
    )

    theorem_answer = completion.choices[0].message.content
    message_content.append({"role": "assistant", "content": theorem_answer})
    # generate answer
    print("generating answer...")
    message_content.append({"role": "user", "content": openai_config["solve_prompt"]})
    completion = openai.ChatCompletion.create(
        model=model,
        messages=message_content,
        temperature=0.8,
    )
    answer = completion.choices[0].message.content
    message_content.append({"role": "assistant", "content": answer})
    print(message_content)

    return def_answer, theorem_answer, answer


async def get_most_similar_question(question: str) -> Question:
    question_records = await Question.all()
    questions = [record.question for record in question_records]

    if questions.__len__() != 0:
        
        diff_ratios = [
            difflib.SequenceMatcher(
                lambda x: x in r"""!"#$%&'(),.:;?@[\]^_`{|}~""" or x.isspace(),
                question,
                q,
            ).ratio()
            for q in questions
        ]
        max_index = diff_ratios.index(max(diff_ratios))
        similarity_threshold = 0.95
        if diff_ratios[max_index] > similarity_threshold:
            record = question_records[max_index]
            return record

    return None


async def get_answer_internal(question, model,system_prompt) -> Question:
    most_similar_question = await get_most_similar_question(question)

    if most_similar_question is not None:
        return Question.from_record(most_similar_question, 100)

    def_answer, theorem_answer, answer = get_openai_answer(question, model,system_prompt=system_prompt)

    question = Question(
        question=question,
        definition=def_answer,
        theorem=theorem_answer,
        answer=answer,
        accuracy=generate_accuracy(),
    )

    return question


@app.get("/hello")
async def hello():
    return {"message": "Hello World"}


@app.get("/")
async def hello():
    return "你好"


@app.post(f"/submitImage")
@log_endpoint_data
async def submit_image(image: UploadFile = File(...)):
    contents = await image.read()
    img_base64 = base64.b64encode(contents).decode("utf-8")

    try:
        text_detections = tencent_ocr(img_base64)
    except Exception as err:
        return JSONResponse(ResponseBean.fail(str(err)))

    if text_detections is None:
        return JSONResponse(ResponseBean.fail("No text detected."))

    detected_text = " ".join([item.DetectedText for item in text_detections])

    return_question = Question(question=detected_text).to_json()

    return JSONResponse(ResponseBean.success("Text detected.", return_question))
    # answer = await get_answer_internal(detected_text)
    # q = Question(question=detected_text, answer=answer)
    # return JSONResponse(content=ResponseBean(True, "Answer generated.", q.to_json()).to_dict())


@app.post(f"/submitText")
@log_endpoint_data
async def submit_text(
    text: str = Form(...),
    model: str = Form(...),
    age: str = Form(...),
    language: str = Form(...),
):
    try:
        print(language)
        text = f"你好,我是一位{language}人，目前处于{age}阶段，我的问题如下：\"{text}\"。请使用{language}回答我的问题"
        if language == "Chinese":
            system_prompt = ' Output all contents in Simplified Chinese. You are SolveGPT, a professional assistant for answering mathematics questions. Use Markdown with Latex. Write all formulas in latex format and wrap them with $.'
            question = await get_answer_internal(text, model,system_prompt=system_prompt)
        elif language=='English':
            system_prompt = ' Output all contents in English. You are SolveGPT, a professional assistant for answering mathematics questions. Use Mark with Latex. Write all formulas in latex format and wrap them with $.'
            question = await get_answer_internal(text, model,system_prompt=system_prompt)

        message = (
            "Answer generated from database."
            if question.accuracy == 100
            else "Answer generated from SolveGPT."
        )
        return JSONResponse(ResponseBean.success(message, question.to_json()))
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(ResponseBean.fail(str(e)))


@app.post(f"/save")
async def save_question(
    question: str = Form(...),
    definition: str = Form(...),
    theorem: str = Form(...),
    answer: str = Form(...),
):
    q = Question(
        question=question, answer=answer, definition=definition, theorem=theorem
    )
    await q.save()
    return JSONResponse(ResponseBean.success("Question saved."))


@app.get(f"/getAll")
async def get_all():
    question_records = await Question.all()
    questions = [record.to_json() for record in question_records]
    return JSONResponse(ResponseBean.success("Questions retrieved.", questions))


@app.post(f"/clear")
async def clear():
    await Question.all().delete()
    return JSONResponse(ResponseBean.success("Questions cleared.", None))


@app.get(f"/download")
async def download():
    questions = await Question.all().values(
        "question", "definition", "theorem", "answer"
    )
    output = io.StringIO()
    csv_writer = csv.writer(output, delimiter="\t")
    for question in questions:
        csv_writer.writerow(
            [
                question["question"],
                question["definition"],
                question["theorem"],
                question["answer"],
            ]
        )
    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="questions.csv"'},
    )


@app.post(f"/upload")
async def upload(file: UploadFile = File(...)):
    file_content = await file.read()
    content = io.StringIO(file_content.decode())
    csv_reader = csv.reader(content, delimiter="\t")

    try:
        questions = [Question(question=row[0], answer=row[1]) for row in csv_reader]
    except IndexError:
        return JSONResponse(ResponseBean.fail("File format incorrect."))

    await Question.all().delete()
    await Question.bulk_create(questions)

    return ResponseBean.success("Questions uploaded.")


@app.post(f"/pdf")
async def serve_pdf(
    question: str = Form(...),
    definition: str = Form(...),
    theorem: str = Form(...),
    answer: str = Form(...),
):
    most_similar_question = await get_most_similar_question(question)
    pdf_name = None

    if most_similar_question is not None:
        if most_similar_question.pdf_name is not None:
            pdf_name = most_similar_question.pdf_name

    if pdf_name is None or not os.path.exists(
        os.path.join("static/pdfs", f"{pdf_name}.pdf")
    ):
        pdf_name = uuid.uuid1()
        file_path = os.path.join("static/pdfs", f"{pdf_name}.pdf")
        create_pdf(
            Question(
                question=question, definition=definition, theorem=theorem, answer=answer
            ),
            pdf_name,
        )

    file_path = os.path.join("static/pdfs", f"{pdf_name}.pdf")

    if most_similar_question is not None:
        most_similar_question.pdf_name = pdf_name
        await most_similar_question.save()

    if os.path.isfile(file_path):
        return ResponseBean.success(data={"pdf_url": f"/static/pdfs/{pdf_name}.pdf"})
    else:
        return ResponseBean.fail("Error")


@app.get( "/pdf/{pdf_name}")
async def get_pdf(pdf_name: str):
    file_path = os.path.join("/root/solvegpt/static/pdfs", f"{pdf_name}.pdf")
    if os.path.isfile(file_path):
        return FileResponse(file_path, media_type="application/pdf")
    else:
        return {"error": "File not found"}

@app.post('/language')
def dmeo_index(a:DATA):
     
    
    data=a.LanguageList
    print(data)
    if a.type==1:
        return_data=['', '', '', '', 'SolveGPT - AI Jizhi Math Teacher', '', '', '', '', 'Advanced Settings', '', '', 'Switch Theme ', '', 'Image to text', '', 'Comprehensive mode (recommended)', '', 'Switch language', '', 'Check balance', '', 'Unbound account', '' , 'Logout', '', '', '', '', '', '', '', '', '', 'List of supported models:', '', '', 'gpt-4 -0613', '', 'gpt-4', '', 'gpt-3.5-turbo-0613', '', 'gpt-3.5-turbo', '', '', '', '', ' Answer language setting', '', '', 'Chinese', '', 'Chinese', '', '', '', '', 'Use age options', '', '', 'Primary school' , '', 'Middle School', '', 'High School', '', 'University', '', '', '', 'Question:', '', '', '', '', 'Upload Picture:', '', '', '', 'picture to text', '', 'one-key solution', '', '', 'knowledge and answer:', '', '', '' , 'Store Knowledge Base', '', 'View pdf', '', 'Knowledge Treasure:', '', 'Download', '', '', 'Upload', '', '', '', '', '', 'question', '', 'definition/theorem/answer', '', '', '', '', '', '', '', '', '', '' , 'Token account number:', '', '', '', '', 'Select payment currency:', '', '', '', '', '', 'Confirm query', ' ','','','']    
  
        return {'LanguageList':return_data} 
    elif a.type==2:
        return_data=['', '', '', '', 'SolveGPT - AI Jizhi Math Teacher', '', '', '', '', 'Advanced Settings', '', '', 'Switch Theme ', '', 'Image to text', '', 'Comprehensive mode (recommended)', '', 'Switch language', '', 'Log out', '', '', '', '', '', '', '', '', '', 'List of supported models:', '', '', 'gpt-4-0613', '', 'gpt-4', '', 'gpt -3.5-turbo-0613', '', 'gpt-3.5-turbo', '', '', '', '', 'Answer language setting', '', '', 'Chinese', '', 'English', '', '', '', '', 'Use age stage options', '', '', 'Primary School', '', 'Middle School', '', 'High School', '', 'University', '', '', '', 'Question:', '', '', '', '', 'Upload image:', '', '', '', 'Image to text' , '', 'One-click problem solving', '', '', 'Knowledge and answers:', '', '', '', 'Store knowledge base', '', 'View pdf', '', 'Knowledge treasure house:', '', 'download', '', '', 'upload', '', '', '', '', '', 'Question', '', 'Definition/Theorem/ Answer', '', '', '', '', '', '', '', '']
        return {'LanguageList':return_data} 
  
   
TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["solve_gpt_api.models"],
            "default_connection": "default",
        },
    },
}

register_tortoise(
    app,
    generate_schemas=True,
    add_exception_handlers=True,
    config=TORTOISE_ORM,
)
