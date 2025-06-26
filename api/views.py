from django.shortcuts import render

# Create your views here.
# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.core.files.storage import default_storage
from .utils import detect_faces
import os

class FaceDetectView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        image = request.FILES['image']
        blur = request.data.get('blur', 'false') == 'true'

        path = default_storage.save(f'uploads/{image.name}', image)
        full_path = os.path.join(default_storage.location, path)

        output_rel_path, faces = detect_faces(full_path, blur)
        return Response({
            'num_faces': len(faces),
            'faces': faces,
            'image_url': request.build_absolute_uri('/media' + output_rel_path)
        })
