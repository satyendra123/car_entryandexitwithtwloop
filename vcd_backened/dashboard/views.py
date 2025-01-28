from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import CarLog
from .serializers import CarLogSerializer
from django.db.models import Q
from datetime import datetime

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_data(request):
    # Calculate the total entries, exits, and vehicles for each gate
    gate1_entries = CarLog.objects.filter(gate='1', action='entry').count()
    gate1_exits = CarLog.objects.filter(gate='1', action='exit').count()
    gate1_vehicles = CarLog.objects.filter(gate='1').count()
    
    gate2_entries = CarLog.objects.filter(gate='2', action='entry').count()
    gate2_exits = CarLog.objects.filter(gate='2', action='exit').count()
    gate2_vehicles = CarLog.objects.filter(gate='2').count()

    gate3_entries = CarLog.objects.filter(gate='3', action='entry').count()
    gate3_exits = CarLog.objects.filter(gate='3', action='exit').count()
    gate3_vehicles = CarLog.objects.filter(gate='3').count()
    
    # Prepare the data to send in the response
    data = {
        'gate1': {
            'total_entry': gate1_entries,
            'total_exit': gate1_exits,
            'total_vehicles': gate1_vehicles,
        },
        'gate2': {
            'total_entry': gate2_entries,
            'total_exit': gate2_exits,
            'total_vehicles': gate2_vehicles,
        },
        'gate3': {
            'total_entry': gate3_entries,
            'total_exit': gate3_exits,
            'total_vehicles': gate3_vehicles,
        },
    }
    
    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def generate_report(request):
    # Retrieve query parameters from the request
    from_date = request.data.get('from_date')
    to_date = request.data.get('to_date')
    action_type = request.data.get('action', 'All')
    gate = request.data.get('gate', 'All')

    filter_conditions = Q()

    if from_date:
        filter_conditions &= Q(created_at__gte=datetime.strptime(from_date, '%Y-%m-%d'))
    if to_date:
        filter_conditions &= Q(created_at__lte=datetime.strptime(to_date, '%Y-%m-%d'))

    if action_type != 'All':
        filter_conditions &= Q(action=action_type)

    if gate != 'All':
        filter_conditions &= Q(gate=gate)

    filtered_logs = CarLog.objects.filter(filter_conditions)
    serializer = CarLogSerializer(filtered_logs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def activity_log(request):
    logs = CarLog.objects.all().order_by('-created_at')[:10]
    serializer = CarLogSerializer(logs, many=True)
    return Response(serializer.data)
