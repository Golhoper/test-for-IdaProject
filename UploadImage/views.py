from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, TemplateView, DetailView
from .models import ImageModel
from .forms import ArticleForm
from PIL import Image
import urllib, os, time, imagehash
# from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File


class ShowImage(DetailView):
    template_name = 'image.html'
    queryset = ImageModel.objects.all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        p = data.get('imagemodel').pk
        r_data = self.request.GET
        width, height, size = 0, 0, 0

        if r_data:
            width = r_data.get('width', 0)
            height = r_data.get('height', 0)
            size = r_data.get('size', 0)

            print(width)
            print(height)
            print(size)

        context = ImageModel.objects.filter(hash=p)

        context = {'context': context,
                   'width': width,
                   'height': height,
                   'size': size}

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
                # hash_filename = str(hash(fname))
                # final_hash = hash_img + hash_time + hash_filename
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
                # hash_filename = str(hash(form.cleaned_data["picture"]))

                # img_model.hash = hash_img + hash_time + hash_filename
                img_model.hash = hash_img + hash_time
                img_model.img = form.cleaned_data["picture"]
                img_model.save()

                return HttpResponseRedirect('/')

        context = {'ArticleForm': form}
        return render(request, 'upload.html', context)
