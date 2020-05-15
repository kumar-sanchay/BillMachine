import json
import redis
from django.conf import settings
from channels.db import database_sync_to_async
from company.models import Company
from .models import FileStorage
from channels.generic.websocket import AsyncWebsocketConsumer


r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class SearchConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.pk = self.scope['url_route']['kwargs']['pk']
        self.slug = self.scope['url_route']['kwargs']['slug']
        self.user = self.scope['user']
        self.company_exists = await self.check_company(self.user, self.pk, self.slug)
        print(self.company_exists)
        if self.company_exists:
            if r.hexists(name="company::search_fields", key="{}::{}".format(self.slug, self.pk)):
                self.search_key = r.hget(name="company::search_fields", key="{}::{}".format(self.slug, self.pk))
                await self.accept()
            else:
                await self.close()
        else:
           await self.close()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        texts = json.loads(text_data)
        search_id = texts['search_id']
        search_data = texts['search_data']
        print(texts)
        print(search_data)
        if search_id == "1":
            cursor_count = 0
            while True:
                result_tuple = r.hscan(name="{}::search_fields".format(self.pk),
                                             cursor=cursor_count, match="{}*".format(search_data), count=10)
                result = {}
                for y in result_tuple[1]:
                    if y.decode() != 'last_index':
                        result[y.decode()] = result_tuple[1].get(y).decode()
                # result = {y.decode(): result_tuple[1].get(y).decode() for y in result_tuple[1]}

                print(result)
                # print(type(result_tuple[0]))
                await self.send(json.dumps({"result": result, "result_id": 1}))
                if result_tuple[0] == 0:
                    break
                cursor_count = result_tuple[0]
        elif search_id == "2":
            index = texts["index"]
            dict_val = r.hgetall(name="{}::{}".format(self.pk, index))
            lst_val = [val.decode() for val in dict_val.values()]
            print(lst_val)
            lst = [i for i in lst_val]
            print(lst)
            await self.send(json.dumps({
                "result": lst,
                "result_id": 2
            }))
        elif search_id == 'done':
            data = texts['data']
            to = texts['to']
            invoice = texts['invoice']
            result_data = texts['result_data']
            result = await self.add_bill(to, invoice, data, result_data)
            print(result)
            if result is True:
                await self.send(json.dumps({
                    'result_id': 'done',
                }))
            else:
                await self.send(json.dumps({
                    'result_id': 'not_done',
                }))

    @database_sync_to_async
    def check_company(self, user, pk, slug):
        return Company.objects.get(pk=pk, slug=slug, user=user, active=True)

    @database_sync_to_async
    def add_bill(self, to, invoice, data, result_data):
        print(self.company_exists)
        try:
            company = self.company_exists
            print(self.user)
            print('done')
            FileStorage.objects.create(user=self.user, company=company, to=to, invoice_no=invoice,
                        data=data, result=result_data, gst=company.gst, cgst=company.cgst_no,
                                       sgst=company.sgst_no, igst=company.igst_no)
        except Exception as e:
            print(e)
            print('nope')
            return False
        return True

    async def websocket_disconnect(self, message):
        print(message)
        await self.close()