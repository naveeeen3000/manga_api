from rest_framework.views import APIView
from rest_framework import authentication,permissions
from rest_framework.response import Response




class IndexView(APIView):
    """
    # home page
    *Requires Token Authentication
    *Only Admin users can see all the options
    """
    # authentication_classes=[authentication.TokenAuthentication,]
    # permission_classes=[permissions.IsAdminUser]

    def get(self,request,*args,**kwargs):
        # print(request.)
        base_url =  "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)
        # base_url=request.stream
        result={
            "search_api":base_url+'api/v1/search/?q=',
            "accounts_api":base_url+'api/v1/user/',
            "login_api": base_url+"api/v1/user/login/"
        }
        return Response(result)