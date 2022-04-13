from rest_framework.views import APIView
from rest_framework import authentication,permissions
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication,BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class IndexView(APIView):
    """
    Requires Token Authentication
    Only Admin users can see all the options
    End-Points: 
    """
    authentication_classes=[SessionAuthentication,TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request,*args,**kwargs):
        # print(request.)
        base_url =  "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)
        # base_url=request.stream
        result={
<<<<<<< HEAD
            "search_api":base_url+'api/v1/search/?q={}',
            
=======
            "search_api":base_url+'api/v1/search/?q=',
            "accounts_api":base_url+'api/v1/user/',
            "login_api": base_url+"api/v1/user/login/"
>>>>>>> f1d63e5af8ee04e95ac4dcc554490f98ef11c6df
        }
        return Response(result)