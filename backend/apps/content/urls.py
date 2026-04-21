from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CategoryViewSet, TagViewSet, MediaViewSet, TestimonialViewSet, PartnerViewSet

router = DefaultRouter()
router.register("posts",         PostViewSet,         basename="posts")
router.register("categories",    CategoryViewSet,     basename="categories")
router.register("tags",          TagViewSet,          basename="tags")
router.register("media",         MediaViewSet,        basename="media")
router.register("testimonials",  TestimonialViewSet,  basename="testimonials")
router.register("partners",      PartnerViewSet,      basename="partners")

urlpatterns = [path("", include(router.urls))]
