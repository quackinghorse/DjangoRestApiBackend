from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from empdata.serializers import StudentSerializer
from empdata.models import Student
from django.core.exceptions import ValidationError

@csrf_exempt
def studentApi(request, id=0):
    if request.method == 'GET':
        if id != 0: 
            try:
                student = Student.objects.get(pk=id)
                student_serializer = StudentSerializer(student)
                return JsonResponse(student_serializer.data, safe=False)
            except Student.DoesNotExist:
                return JsonResponse({"error": "Student not found"}, status=404)
        else:  
            students = Student.objects.all()
            student_serializer = StudentSerializer(students, many=True)
            return JsonResponse(student_serializer.data, safe=False)
    
    elif request.method == 'POST':
        student_data = JSONParser().parse(request)
        student_serializer = StudentSerializer(data=student_data)
        if student_serializer.is_valid():
            try:
                student_serializer.save()
                return JsonResponse("Added Successfully", safe=False)
            except ValidationError as e:
                return JsonResponse({"error": e.messages}, status=400)
        return JsonResponse(student_serializer.errors, status=400)
    
    elif request.method == 'PUT':
        student_data = JSONParser().parse(request)
        try:
            student = Student.objects.get(pk=id)
        except Student.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)
        student_serializer = StudentSerializer(student, data=student_data, partial=True)
        if student_serializer.is_valid():
            try:
                student_serializer.save()
                return JsonResponse("Updated Successfully", safe=False)
            except ValidationError as e:
                return JsonResponse({"error": e.messages}, status=400)
        return JsonResponse(student_serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        try:
            student = Student.objects.get(pk=id)
        except Student.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)
        student.delete()
        return JsonResponse("Deleted Successfully", safe=False)
