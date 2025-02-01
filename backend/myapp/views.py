from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import subprocess
import tempfile
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def compile_code(request):
    if request.method == 'POST':
        try:
            logger.info("Received request body: %s", request.body.decode('utf-8'))  # Debugging
            data = json.loads(request.body)

            code = data.get('code')
            language = data.get('language')

            if not code or not language:
                logger.error("Invalid input: code=%s, language=%s", code, language)
                return JsonResponse({'error': 'Invalid input. Please provide both "code" and "language".'}, status=400)

            # Compile and execute the code
            output = compile_and_execute(code, language)
            return JsonResponse({'output': output})
        
        except json.JSONDecodeError as e:
            logger.error("JSON decoding error: %s", str(e))
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        
        except Exception as e:
            logger.error("Unexpected error: %s", str(e))
            return JsonResponse({'error': f'Internal server error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def compile_and_execute(code, language):
    extensions = {'python': 'py', 'java': 'java', 'cpp': 'cpp'}
    commands = {
        'python': lambda file_path: ['python', file_path],
        'java': lambda file_path: ['sh', '-c', f"javac {file_path} && java {file_path.split('.')[0]}"],
        'cpp': lambda file_path: ['sh', '-c', f"g++ {file_path} -o /tmp/main && /tmp/main"]
    }

    if language not in extensions or language not in commands:
        return "Unsupported language."

    file_extension = extensions[language]
    command_func = commands[language]

    try:
        with tempfile.NamedTemporaryFile(suffix=f".{file_extension}", delete=True) as temp_file:
            temp_file.write(code.encode())
            temp_file.flush()

            # Run the command
            command = command_func(temp_file.name)
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode != 0:
                return f"Error: {result.stderr.strip()}"

            return result.stdout.strip()

    except Exception as e:
        return f"Execution error: {str(e)}"
