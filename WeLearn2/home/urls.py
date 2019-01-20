from django.urls import path
from . import views
from . import ajax

urlpatterns = [
    path('',views.HomeView.as_view(), name='home'),
    path('pack/create/',views.PackCreateView.as_view(),name='pack-create-view'),
    path('pack/<int:pk>/detail',views.PackDetailView.as_view(),name='detail-view'),
    path('pack/<int:pk>/link/add/',views.LinkCreateView.as_view(),name='link-create-view'),
    path('pack/<int:pk>/edit/',views.PackEditView.as_view(),name='pack-edit-view'),
    path('link/<int:pk>/edit/',views.LinkEditView.as_view(),name='link-edit-view'),
    path('pack/<int:pk>/delete/',views.PackDeleteView.as_view(),name='pack-delete-view'),
    path('link/<int:pk>/delete/',views.LinkDeleteView.as_view(),name='link-delete-view'),
    path('user/<int:pk>/profile/',views.ProfileView.as_view(),name='profile-view'),
    path('packs/category/',views.CategoryView.as_view(),name='category-view'),
    path('profile/edit/',views.ProfileEditView.as_view(),name='profile-edit-view'),
    path('notifications/',views.NotificationView.as_view(),name='notifs-view'),
    path('favourites/',views.FavouriteView.as_view(),name='favourites-view'),
    path('bookmarks/',views.BookmarkView.as_view(),name='bookmarks-view'),
    path('pack/like/',ajax.like,name='like'),
    path('pack/book/',ajax.book,name='book'),
    path('notifications/remove/',ajax.remove_notif,name='remove'),
    path('notifications/remove/all/',ajax.remove_all,name='remove-all'),
    path('comment/like/',ajax.comment_like,name='comment-like'),
    path('reply/like/',ajax.reply_like,name='reply-like'),
    path('comment/create/',ajax.create_comment,name='comment-create'),
    path('reply/create/',ajax.create_reply,name='reply-create'),
    path('comment/edit/',ajax.comment_edit,name='comment-edit'),
    path('reply/edit/',ajax.reply_edit,name='reply-edit'),
    path('comment/delete/',ajax.comment_delete,name='comment-delete'),
    path('reply/delete/',ajax.reply_delete,name='reply-delete'),
    path('user/follow/',ajax.follow,name='follow'),
    path('search/',views.SearchView.as_view(),name='search-view')
]