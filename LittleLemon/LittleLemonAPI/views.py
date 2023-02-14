
# import generics to use class-based views :
from rest_framework import generics

# Import stuff for authantification :
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes # @permission_classes([IsAuthenticated])
