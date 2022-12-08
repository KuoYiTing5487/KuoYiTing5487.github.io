from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, HttpResponse
from .script.GetHand import V_Camera2, to_gen2, hand_video
from .script.camera import VideoCamera, gen
from .script.mixed import V_Camera, to_gen
from products.models import Product
from partners.forms import CartForm, Test
from partners.models import Cart, HandSize
# Create your views here.


def home_view(request, *args, **kwargs):
    queryset = Product.objects.all()  # list of objects
    cart_queryset = Cart.objects.filter(account=request.user.id)
    form = CartForm(request.POST or None)

    context = {
        "object_list": queryset,
        "cart": cart_queryset,
        "times": 0,
        "form": form,
    }
    return render(request, "home.html", context)  # 從名為home.html模板中抓取此頁應有樣貌


def cart_add_view(request, p_id):
    form = CartForm(request.POST or None)

    instance = form.save(commit=False)
    instance.account = request.user
    instance.product = Product.objects.get(id=p_id)
    instance.save()
    return redirect('../../')


def cart_delete_view(request, p_id):
    obj = Cart.objects.get(product=p_id, account=request.user.id)
    # if request.method == "POST":
    obj.delete()
    return redirect('../')


def about_view(request, *args, **kwargs):
    return render(request, "about.html")


def threed_model_view(request):
    queryset = Product.objects.all()  # list of objects
    size = HandSize.objects.get(account=request.user.id)
    context = {
        "object_list": queryset,
        "times": 0,
        "size": size
    }
    return render(request, "3D_model/3d_js.html", context)


def button(request):
    form = Test(request.POST or None)
    # if request.method == "POST":
    #
    #     return StreamingHttpResponse(to_gen2(V_Camera2(), False),
    #                                  content_type='multipart/x-mixed-replace; boundary=frame')
    context = {
        'form': form,
        # 'function': to_gen2(V_Camera2(), False),
    }
    return render(request, 'get_hand_button.html', context)


# def get_hand(request):
#
#     return render(request, 'get_hand.html')
    # return HttpResponse(request, 'get_hand.html')


def get_hand(request):
    # hans_size = HandSize.objects.get(member=request.user)
    return StreamingHttpResponse(to_gen2(V_Camera2(), False), content_type='multipart/x-mixed-replace; boundary=frame')
    # return vid vid =


def hand_control(request):
    vid = StreamingHttpResponse(to_gen(V_Camera(), False), content_type='multipart/x-mixed-replace; boundary=frame')
    return vid


# ~~~~ outside ~~~~

def video_stream(request):
    vid = StreamingHttpResponse(gen(VideoCamera(), False), content_type='multipart/x-mixed-replace; boundary=frame')
    return vid

