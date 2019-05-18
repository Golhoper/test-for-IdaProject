from django.test import Client, TestCase, SimpleTestCase
from .models import ImageModel


class MainTest(SimpleTestCase):
    allow_database_queries = True

    def setUp(self) -> None:
        ImageModel.objects.get_or_create(hash='fce1dc3e3cd8e1f52008397627667790022', img='articles/ubuntu.png')
        ImageModel.objects.get_or_create(hash='ff8381091989c3ff637945993842669771', img='articles/windows.jpeg')

    def test_access_pages(self):
        c = Client()

        # main page
        response = c.get('')
        self.assertEqual(response.status_code, 200)

        # upload page
        response = c.get('/upload/')
        self.assertEqual(response.status_code, 200)

        # image_hash page
        qrs = ImageModel.objects.all()
        self.assertNotEqual(len(qrs), 0)

        for qr in qrs:
            response = c.get('/image/{}/'.format(qr.hash))
            self.assertEqual(response.status_code, 200)

    def test_main_page(self):
        c = Client()

        qrs = ImageModel.objects.all()

        response = c.get('')
        object_list = response.context_data.get('object_list')
        # Images loaded
        self.assertIsNotNone(response.context_data.get('object_list'))
        # All images on the page
        self.assertEqual(len(qrs), len(object_list))

    def test_image_hash_page(self):
        c = Client()
        qrs = ImageModel.objects.all()
        self.assertNotEqual(len(qrs), 0)

        for qr in qrs:
            response = c.get('/image/{}/'.format(qr.hash))
            self.assertEqual(response.status_code, 200)

            # values list for correct and incorrect page creation
            list_sizes = [[[x * 100, x * 5000], [x * 200, x * 50]] for x in range(1, 4)]

            # testing access page with different parameters
            for crr, incrr in list_sizes:
                wh_tr, sb_tr = crr[0], crr[1]
                wh_fls, sb_fls = incrr[0], incrr[1]

                # --- for correct values
                response = c.get('/image/{}/?width={}&height={}&size={}'.format(qr.hash, wh_tr, wh_tr, sb_tr))
                self.assertEqual(response.status_code, 200)

                context = response.context_data.get('context')
                # image exists
                self.assertGreater(len(context.get('exp64')), 100)
                # all parameters correct
                self.assertEqual([wh_tr, wh_tr, sb_tr], [context.get('width'),
                                                         context.get('height'),
                                                         context.get('size')])
                self.assertFalse(context.get('err_mess'))
                # ---
                # --- for incorrect values
                response = c.get('/image/{}/?width={}&height={}&size={}'.format(qr.hash, wh_fls, wh_fls, sb_fls))
                self.assertEqual(response.status_code, 200)

                context = response.context_data.get('context')
                # image exists
                self.assertGreater(len(context.get('exp64')), 100)
                # all parameters correct
                self.assertEqual([wh_fls, wh_fls, sb_fls], [context.get('width'),
                                                            context.get('height'),
                                                            context.get('size')])
                self.assertGreater(len(context.get('err_mess')), 20)
                # ---