from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, TemplateView, DetailView
from .models import ImageModel
from .forms import ArticleForm, ChangeParamsForm
from PIL import Image
import urllib, os, time, imagehash
from io import BytesIO
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
import base64


class ShowImage(DetailView):
    template_name = 'image.html'
    queryset = ImageModel.objects.all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        p = data.get('imagemodel').pk
        r_data = self.request.GET
        width, height, size = 0, 0, 0

        form = ChangeParamsForm(data.get('view').request.GET)

        if form.is_valid():
            way_to_pic = ImageModel.objects.get(hash=p).img.name
            im = Image.open('media/' + way_to_pic).convert('RGB')

            if r_data:
                width = r_data.get('width', im.width)
                height = r_data.get('height', im.height)
                size = r_data.get('size', 0)

            if not isinstance(width, str):
                width = im.width
            if not isinstance(height, str):
                height = im.height
            if size != 0:
                size = int(size)

            gg = abs(int(width)), abs(int(height))
            im = im.resize(gg, Image.ANTIALIAS)
            buffered = BytesIO()

            if int(size) == 0:
                im.save(buffered, format="jpeg", quality=100)
            else:
                for x in range(91, 0, -10):
                    buffered = BytesIO()
                    im.save(buffered, format="jpeg", quality=x)

                    if x == 1 or buffered.tell() < size:
                        break
                    else:
                        buffered.close()

            img_str = str(base64.b64encode(buffered.getvalue()))[2:-1]

            context = {'context': '',
                       'exp64': img_str,
                       'width': width,
                       'height': height,
                       'size': size,
                       'ChangeParamsForm': form}

            return {'context': context}

        else:
            context = {'ChangeParamsForm': form}
            return {'context': context}


class MainPage(ListView):
    template_name = 'main.html'
    model = ImageModel


class UploadPage(TemplateView):
    template_name = 'upload.html'

    def get_context_data(self, **kwargs):
        context = {'ArticleForm': ArticleForm}
        return context

    def post(self, request):
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data["name"]
            picture = form.cleaned_data["picture"]
            img_model = ImageModel()

            if name:

                image_url = urllib.request.urlretrieve(name)
                fname = os.path.basename(name)

                im = Image.open(image_url[0])
                hash_img = str(imagehash.average_hash(im))
                hash_time = str(hash(time.time()))
                final_hash = hash_img + hash_time

                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urllib.request.urlopen(name).read())
                img_temp.flush()

                img_model.hash = final_hash
                img_model.img.save(fname, File(img_temp))

                return HttpResponseRedirect('/')

            elif picture:

                gg = form.files.get('picture')

                hash_img = str(imagehash.average_hash(Image.open(gg)))
                hash_time = str(hash(time.time()))

                img_model.hash = hash_img + hash_time
                img_model.img = form.cleaned_data["picture"]
                img_model.save()

                return HttpResponseRedirect('/')

        context = {'ArticleForm': form}
        return render(request, 'upload.html', context)
