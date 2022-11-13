from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication,BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.shortcuts import redirect



class IndexView(APIView):
    """
    Requires Token Authentication
    Only Admin users can see all the options
    End-Points: 
    """
    authentication_classes=[BasicAuthentication,SessionAuthentication,TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request,*args,**kwargs):
        
        return redirect('admin/')


@api_view(['get'])
def user_view(request):
    base_url="{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)

    result={
    'create_user':base_url+'user/create'
    }

    return Response(result)