from django.shortcuts import render, redirect
from rbac import models
from rbac.init_permission import init_permission

# 测试
def login(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        user = models.User.objects.filter(name=name, password=password).first()
        if not user:
            err_msg = '用户名或密码错误'
            return render(request, 'login_r.html', locals())

        # user_permission = models.Permission.objects.filter(role=models.Role.objects.filter(user=user)).values_list(
        #     'url')
        # 存放权限url
        init_permission(user, request)

        return redirect('leads')

    return render(request, 'login_r.html')



def distribute(request):
    return render(request, 'distribute_permissions.html')