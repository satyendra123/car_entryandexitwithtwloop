from django.utils.timezone import now
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import CarLog,Boomsig
from .serializers import CarLogSerializer
from django.db.models import Q,F
from datetime import datetime
from datetime import datetime, timedelta


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_data(request):
    today = now().date()

    # Filter CarLog by today's date
    gate1_entries = CarLog.objects.filter(gate='1', action='entry', created_at__gte=today).count()
    gate1_exits = CarLog.objects.filter(gate='1', action='exit', created_at__gte=today).count()
    gate1_vehicles_inside = gate1_entries - gate1_exits
    gate1_barrier_open_count = Boomsig.objects.filter(id=1).values_list('barrier_open_count', flat=True).first()

    gate2_entries = CarLog.objects.filter(gate='2', action='entry', created_at__gte=today).count()
    gate2_exits = CarLog.objects.filter(gate='2', action='exit', created_at__gte=today).count()
    gate2_vehicles_inside = gate2_entries - gate2_exits
    gate2_barrier_open_count = Boomsig.objects.filter(id=2).values_list('barrier_open_count', flat=True).first()

    gate3_entries = CarLog.objects.filter(gate='3', action='entry', created_at__gte=today).count()
    gate3_exits = CarLog.objects.filter(gate='3', action='exit', created_at__gte=today).count()
    gate3_vehicles_inside = gate3_entries - gate3_exits
    gate3_barrier_open_count = Boomsig.objects.filter(id=3).values_list('barrier_open_count', flat=True).first()

    # Prepare the data to send in the response
    data = {
        'gate1': {
            'total_entry': gate1_entries,
            'total_exit': gate1_exits,
            'vehicles_inside': gate1_vehicles_inside,
            'barrier_open_count': gate1_barrier_open_count or 0,
        },
        'gate2': {
            'total_entry': gate2_entries,
            'total_exit': gate2_exits,
            'vehicles_inside': gate2_vehicles_inside,
            'barrier_open_count': gate2_barrier_open_count or 0,
        },
        'gate3': {
            'total_entry': gate3_entries,
            'total_exit': gate3_exits,
            'vehicles_inside': gate3_vehicles_inside,
            'barrier_open_count': gate3_barrier_open_count or 0,
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


@api_view(['POST'])
@permission_classes([AllowAny])
def barrier_open(request):
    gate_number = request.data.get('gate_number')

    if gate_number == 1:
        # Update the entryboom, entrysynctime, and increment the barrier_open_count for gate 1
        Boomsig.objects.filter(id=1).update(entryboom='Y', entrysynctime=timezone.now(),barrier_open_count=F('barrier_open_count') + 1)
        return Response({'message': 'Entry barrier opened'}, status=200)
    elif gate_number == 2:
        # Update the exitboom, exitsynctime, and increment the barrier_open_count for gate 2
        Boomsig.objects.filter(id=2).update(entryboom='Y', exitsynctime=timezone.now(),barrier_open_count=F('barrier_open_count') + 1)
        return Response({'message': 'Exit barrier opened'}, status=200)
    else:
        return Response({'message': 'Invalid gate number'}, status=400)
