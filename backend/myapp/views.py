# from rest_framework.decorators import api_view
# from rest_framework.response import Response
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
    docker_images = {'python':'python-compiler', 'java': 'java-compiler', 'cpp': 'cpp-compiler'}

    # set the temp directory for the files (main.java etc)
    # temp_dir = "/tmp/docker_compile"
    # temp_dir = os.path.join(os.getcwd(), 'docker_temp')
    temp_dir = '/app'
    # os.makedirs(temp_dir, exist_ok=True)

    if language == 'java':
        file_name = "Main.java" # to ensure filename is Main.java for java (causing problems)
        compiled_file = "Main.class"
    elif language == 'cpp':
        file_name = "main.cpp"
        compiled_file = "main"
    else:
        file_name = f"temp.{extensions[language]}"
        compiled_file = None
    
    docker_image = docker_images[language]

    # using absolute path to ensure the file is created in the current working directory
    # file_path = os.path.join(os.getcwd(), file_name)   # previously 'temp.py' 
    file_path = os.path.join(temp_dir, file_name)

    try:
        # ensure the directory exists
        os.makedirs(temp_dir, exist_ok=True)

        print(f"Creating file: {file_path}")
        # write code to temp file
        with open(file_path, 'w') as f:  # 'temp.py' inplace of file_path here (previously)
            f.write(code)
        
        # check if file exists / verifying file creation
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return f"Error: File not found - {file_path}"
        
        print(f"Running command in Docker: {docker_image}")

        # command to run the docker container
        if language == 'python':
            cmd = ['docker', 'run', '--rm', '-v', 'docker_temp:/app', docker_image, 'python', f'/app/{file_name}']
        elif language == 'java':
            cmd = ['docker', 'run', '--rm', '-v', 'docker_temp:/app', docker_image, 'sh', '-c', f"javac /app/{file_name} && java -cp /app Main"]
        elif language == 'cpp':
            cmd = ['docker', 'run', '--rm', '-v', 'docker_temp:/app', docker_image, 'sh', '-c', f"g++ /app/{file_name} -o /app/main && /app/main"]

        # run the docker container to execute the python code
        print(f"Command to be run: {' '.join(cmd)}")
        result = subprocess.run(cmd,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        
        # capture the output and errors
        output = result.stdout
        error = result.stderr 

        # clean up the temp file
        # os.remove(file_path)
        # if compiled_file and os.path.exists(os.path.join(os.getcwd(), compiled_file)):
        #     os.remove(os.path.join(os.getcwd(), compiled_file))

        print(f"Docker command output: {output}")
        print(f"Docker command error: {error}")

        if error:
            return f"Error: {error}"
        else:
            return output
        
    # except Exception as e:
    except subprocess.CalledProcessError as e:
        return f"Compilation failed: {str(e)}"
    
    finally:
        # to ensure temp file deletion post exec
        if os.path.exists(file_path):
            print(f"Deleting file: {file_path}")
            os.remove(file_path)
        # if compiled_file and os.path.exists(os.path.join(os.getcwd(), compiled_file)):
        #     os.remove(os.path.join(os.getcwd(), compiled_file))
        if compiled_file and os.path.exists(os.path.join(temp_dir, compiled_file)):
            print(f"Deleting compiled file: {os.path.join(temp_dir, compiled_file)}")
            os.remove(os.path.join(temp_dir, compiled_file))
