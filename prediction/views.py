import os
import joblib

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Prediction
from .serializers import PredictionSerializer
from .disease_info import DISEASE_INFO


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "ml_model",
    "disease_model.pkl"
)

SYMPTOM_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "ml_model",
    "symptoms.pkl"
)

model = joblib.load(MODEL_PATH)
symptoms = joblib.load(SYMPTOM_PATH)


class PredictDiseaseView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        input_data = []

        for symptom in symptoms:

            input_data.append(
                request.data.get(
                    symptom,
                    0
                )
            )

        prediction = model.predict(
            [input_data]
        )[0]

        confidence = max(
            model.predict_proba(
                [input_data]
            )[0]
        ) * 100

        Prediction.objects.create(
            user=request.user,
            disease=prediction,
            confidence=confidence
        )

        info = DISEASE_INFO.get(
            prediction.lower(),
            {
                "description":
                "No description available.",

                "precautions": [
                    "Consult a healthcare professional"
                ]
            }
        )

        return Response({

            "disease": prediction,

            "confidence": round(
                confidence,
                2
            ),

            "description":
            info["description"],

            "precautions":
            info["precautions"]

        })


class PredictionHistoryView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        predictions = Prediction.objects.filter(
            user=request.user
        ).order_by(
            "-created_at"
        )

        serializer = PredictionSerializer(
            predictions,
            many=True
        )

        return Response(
            serializer.data
        )


class SymptomsView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(
            symptoms
        )