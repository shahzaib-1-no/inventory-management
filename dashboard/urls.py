from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    ### Notification Section ###
    path(
        "notification/<int:pk>/view/",
        views.notification_redirect_view,
        name="notification_redirect_view",
    ),
    ### Notification Section End ###
    # Roles & Permissions URLs Section Start
    path(
        "user_role_and_permission/",
        views.user_role_and_permission,
        name="user_role_and_permission",
    ),
    path(
        "user_role_and_permission/<int:id>/delete",
        views.delete_role,
        name="delete_role",
    ),
    path(
        "user_role_and_permission/<int:id>/edit",
        views.edit_role,
        name="edit_role",
    ),
    path(
        "user_role_and_permission/bulk_delete/",
        views.bulk_group_delete,
        name="bulk_group_delete",
    ),
    # Roles & Permissions URLs Section End
    # User Management URLs CRUD Section Start
    path("user/add_user/", views.add_user, name="add_user"),
    path("user/all_user/", views.all_user, name="all_user"),
    path("user/<int:id>/delete/", views.delete_user, name="delete_user"),
    path("user/<int:id>/edit/", views.edit_user, name="edit_user"),
    path("user/<int:id>/user_detail/", views.user_detail, name="user_detail"),
    path(
        "ajax_user_list_data/",
        views.UserListJson.as_view(),
        name="ajax_user_list_data",
    ),
    path("users/bulk_delete/", views.bulk_delete_users, name="bulk_delete_users"),
    # User Management URLs CRUD Section End
]
