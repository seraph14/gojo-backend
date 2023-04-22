from rest_framework import permissions
from users.utilities import UserTypes

class IsTenant(permissions.BasePermission):
    def has_permission(self, request, view):
        role = request.user.role
        return role == UserTypes.TENANT

class IsLandlord(permissions.BasePermission):
    def has_permission(self, request, view):
        role = request.user.role
        return role == UserTypes.LANDLORD

class IsGeneralManager(permissions.BasePermission):
    def has_permission(self, request, view):
        role = request.user.role
        return role == UserTypes.GENERAL_MANAGER

class IsListingManager(permissions.BasePermission):
    def has_permission(self, request, view):
        role = request.user.role
        return role == UserTypes.LISTING_MANAGER

class IsFinancialManager(permissions.BasePermission):
    def has_permission(self, request, view):
        role = request.user.role
        return role == UserTypes.FINANCIAL_MANAGER
        