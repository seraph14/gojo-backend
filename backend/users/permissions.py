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

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        role = request.user.role
        return role >= UserTypes.LISTING_MANAGER

class CanEditPropertyDetail(permissions.BasePermission):
    def has_permission(self, request, view):
        role = request.user.role
        return role in [UserTypes.LANDLORD, UserTypes.LISTING_MANAGER, UserTypes.GENERAL_MANAGER]

class CanCreateProperty(permissions.BasePermission):
    def has_permission(self, request, view):
        role = request.user.role
        return role in [UserTypes.LANDLORD, UserTypes.LISTING_MANAGER]

class IsLandLordOrTenant(permissions.BasePermission):
    def has_permission(self, request, view):
        role = request.user.role
        return role in [UserTypes.LANDLORD, UserTypes.TENANT]
