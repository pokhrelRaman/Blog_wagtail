# # from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# # from wagtail.models import Page
# # from rest_framework.response import Response
# # from wagtail.contrib.search_promotions.models import Query

# # from drf_yasg import openapi
# # from drf_yasg.views import get_schema_view
# # from drf_yasg.inspectors import SwaggerAutoSchema
# # from rest_framework import permissions



# #  @swagger_auto_schema(manual_parameters=[
# #         openapi.Parameter('q', openapi.IN_QUERY, description="Search query for filtering items by name", type=openapi.TYPE_STRING),
# #     ])
# # def search(request):
# #     search_query = request.GET.get("query", None)
# #     print(search_query)

# #     if search_query:
# #         search_results = Page.objects.live().search(search_query)
# #         query = Query.get(search_query)

# #         # Record hit
# #         query.add_hit()
# #     else:
# #         search_results = Page.objects.none()

# #     return Response(search_results)

# from wagtail.models import Page
# from wagtail.contrib.search_promotions.models import Query
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from rest_framework import permissions

# from blogmain.serializers import BlogPageSerializer as PageSerializer
# from blogmain.models import BlogsPage

# @swagger_auto_schema(
#     method='get',
#     manual_parameters=[
#         openapi.Parameter('query', openapi.IN_QUERY, description="query", type=openapi.TYPE_STRING),
#     ],
#     responses={200: PageSerializer(many=True)})  # Use the PageSerializer for the response
# @api_view(['GET'])
# @permission_classes((permissions.AllowAny,))
# def search(request):
#     search_query = request.GET.get('query', None)
#     print(search_query)

#     if search_query:
#         search_results = BlogsPage.objects.live().search(search_query)
#         # search_results = BlogsPage.objects.live().search(search_query)
#         query = Query.get(search_query)
#         print(search_results)
#         # Record hit
#         query.add_hit()
#     else:
#         search_results = Page.objects.none()

#     serializer = PageSerializer(search_results, many=True)  # Serialize the search results
#     return Response(serializer.data)

from wagtail.search.backends import get_search_backend
from wagtail.search.models import Query
from wagtail.models import Page
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import permissions

from blogmain.serializers import BlogPageSerializer as PageSerializer
from blogmain.models import BlogsPage

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('query', openapi.IN_QUERY, description="query", type=openapi.TYPE_STRING),
    ],
    responses={200: PageSerializer(many=True)})  
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def search(request):
    search_query = request.GET.get('query', None)
    print(search_query)

    if search_query:
        search_backend = get_search_backend()

        search_results = search_backend.search(search_query, BlogsPage)
        print(search_results)

        Query.get(search_query).add_hit()
    else:
        search_results = Page.objects.none()

    serializer = PageSerializer(search_results, many=True)  
    return Response(serializer.data)

