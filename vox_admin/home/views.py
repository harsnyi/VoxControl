from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from home.tool_manager import get_tool, add_tool, tools, get_all_tools
from rest_framework.permissions import IsAuthenticated
from home.serializer import ActionSerializer

class HelloWorldView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "HELLO WORLD!", "type":"success"}, status=status.HTTP_200_OK)


class ExecuteCommandView(APIView):
    permission_classes = [IsAuthenticated]  # Ensures the request is authenticated (Bearer token required)

    def post(self, request):
        # Deserialize the incoming data
        serializer = ActionSerializer(data=request.data)

        # Check if the data is valid
        if serializer.is_valid():
            action = serializer.validated_data['action']
            modifier = serializer.validated_data['modifier']
            device_id = serializer.validated_data.get('id')

            # Process the command
            result = self.process_command(action, modifier, device_id)
            if result[1] == 200:
                return Response({"message": result[0]}, status=status.HTTP_200_OK)
            else:
                return Response({"message": result[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        # If the data is invalid, return an error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def process_command(self, action, modifier, device_id):
        # Get the tool by ID
        tool = get_tool(device_id)
        
        if tool is None:
            return (f"Tool with ID {device_id} not found.", 500)

        if action == "turn":
            if modifier == "on":
                tool.turn_on()
                return (f"Turning on {tool.name}.", 200)
            elif modifier == "off":
                tool.turn_off()
                return (f"Turning off {tool.name}.", 200)
            else:
                return (f"Invalid modifier '{modifier}' for action 'turn'.", 500)
        else:
            return (f"Unknown action '{action}'.", 500)

class GetInfoView(APIView):
    """List all tools"""
    
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(get_all_tools())