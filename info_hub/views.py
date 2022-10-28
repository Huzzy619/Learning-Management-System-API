from likes.views import LikeView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from hitcount.views import HitCountDetailView
import requests

from .models import *
# from .permissions import IsSchool  # change this to IsMentor
from .serializers import *

# Create your views here.


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    # permission_classes = [IsSchool]


    def get_serializer_context(self):
        return {'user': self.request.user, 'request' : self.request}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddPostSerializer
        return PostSerializer

    def retrieve(self, request, *args, **kwargs):

        #simulate getting this endpoint so that it can trigger the views count.
        domain = request.META['HTTP_HOST']
        id = kwargs['pk']
        requests.get(f"http://{domain}/info/postty/{id}")

        return super().retrieve(request, *args, **kwargs)


class LikePostView (LikeView):
    serializer_class = LikePostSerializer


class CommentViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])

    def get_serializer_context(self):
        return {'user': self.request.user, 'post_id': self.kwargs['post_pk']}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCommentSerializer
        return CommentSerializer


class LikeCommentView(LikeView):
    serializer_class = LikeCommentSerializer


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class NewsletterViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'options']

    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer


class PostDetail (HitCountDetailView):
    model = Post
    count_hit = True