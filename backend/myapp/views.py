from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def compile_code(request):
    data = request.data
    code = data.get('code')
    # add logic to compile code using docker
    output = compile_with_docker(code) 
    return Response({'output': output})

def compile_with_docker(code):
    # add logic for docker-based compilation
    return 'Compiled Output'