from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import subprocess
import os 

@csrf_exempt
def compile_code(request):
    # add logic to compile code using docker
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code')
        language = data.get('language')
        output = compile_with_docker(code,language)
        return JsonResponse({'output': output})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def compile_with_docker(code, language):
    # logic for docker-based compilation
    
    # Determine the file extension and Docker image based on language
    extensions = {'python': 'py', 'java': 'java', 'cpp': 'cpp'}
    docker_images = {'python':'python:3.8-slim', 'java': 'openjdk:11-slim', 'cpp': 'gcc:latest'}

    if language == 'java':
        file_name = "Main.java" # to ensure filename is MAin.java for java (causing problems)
    else:
        file_name = f"temp.{extensions[language]}"
    docker_image = docker_images[language]

    # using absolute path to ensure the file is created in the current working directory
    file_path = os.path.join(os.getcwd(), file_name)   # previously 'temp.py' 

    # write code to temp file
    with open(file_path, 'w') as f:  # 'temp.py' inplace of file_path here (previously)
        f.write(code)

    # command to run the docker container
    if language == 'python':
        cmd = ['docker', 'run', '--rm', '-v', f"{os.getcwd()}:/app", docker_image, 'python', f'/app/{file_name}']
    elif language == 'java':
        cmd = ['docker', 'run', '--rm', '-v', f"{os.getcwd()}:/app", docker_image, 'sh', '-c', f"javac /app/{file_name} && java -cp /app {file_name.split('.')[0]}"]
    elif language == 'cpp':
        cmd = ['docker', 'run', '--rm', '-v', f"{os.getcwd()}:/app", docker_image, 'sh', '-c', f"g++ /app/{file_name} -o /app/main && /app/main"]

    # run the docker container to execute the python code
    try:
        result = subprocess.run(cmd,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # capture the output and errors
        output = result.stdout
        error = result.stderr 

        # clean up the temp file
        os.remove(file_path)

        if error:
            return f"Error: {error}"
        else:
            return output
        
    except Exception as e:
        return f"Compilation failed: {str(e)}"