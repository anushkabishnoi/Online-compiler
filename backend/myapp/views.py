from rest_framework.decorators import api_view
from rest_framework.response import Response

import subprocess
import os 

@api_view(['POST'])
def compile_code(request):
    data = request.data
    code = data.get('code')
    # add logic to compile code using docker
    output = compile_with_docker(code) 
    return Response({'output': output})

def compile_with_docker(code):
    # logic for docker-based compilation
    # write code to temp file
    with open('temp.py', 'w') as f:
        f.write(code)
    # run the docker container to execute the python code
    try:
        result = subprocess.run(['docker', 'run', '--rm', '-v', f"{os.getcwd()}:/app", 'python:3.8-slim', 'python', '/app/temp.py'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # capture the output and errors
        output = result.stdout
        error = result.stderr 

        # clean up the temp file
        os.remove('temp.py')

        if error:
            return f"Error: {error}"
        else:
            return output
        
    except Exception as e:
        return f"Compilation failed: {str(e)}"
    # return 'Compiled Output'