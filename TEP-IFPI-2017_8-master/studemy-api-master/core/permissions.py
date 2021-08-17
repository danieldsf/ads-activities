from rest_framework import permissions


class OnlyTeacherCanEditCourse(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.auth != None:
                if request.user.who_is == 'TE':
                    return True
        return False


class OnlyStudentCourses(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.who_is == 'ST':
            return True
        else:
            if request.method == 'PUT':
                return True
        return False


class OnlyTeacherCan(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.who_is == 'TE':
                return True
        return False