import re
import redis
import pickle
import copy
from django.conf import settings
from celery.task import task

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


@task
def change_field(pk, slug, args):
    cursor = 0
    name = '{}::search_fields'.format(pk)
    print(args)
    lst_dictionary = {}
    for a in args:
        lst_dictionary[a] = ''
    print(lst_dictionary)
    try:
        while True:
            result_tuple = r.hscan(name=name, cursor=cursor)
            print(result_tuple)
            for val in result_tuple[1].values():
                final_data_dict = lst_dictionary
                n = '{}::{}'.format(pk, val.decode())
                data_dict = r.hgetall(name=n)
                print(data_dict)
                for x, y in data_dict.items():
                    if x.decode() in args:
                        print(x.decode())
                        final_data_dict[x.decode()] = y.decode()
                    r.hdel(n, x.decode())
                for final_x, final_y in final_data_dict.items():
                    r.hset(name=n, key=final_x, value=final_y)
            if result_tuple[0] == 0:
                break
            else:
                cursor = result_tuple[0]
        if r.hexists(name="company::expressions", key="{}::{}".format(slug, pk)):
            expression_dict = r.hget(name="company::expressions", key="{}::{}".format(slug, pk))
            print(expression_dict)
            try:
                expression_dict = pickle.loads(expression_dict)
                final_expression_dict = copy.deepcopy(expression_dict)
                print(expression_dict)
                for e_x, e_y in expression_dict.items():
                    if e_x not in args:
                        final_expression_dict.pop(e_x, None)
                        continue
                    else:
                        e_lst = r'[A-Z][\w]*[$a-z0-9]'
                        lst = re.findall(e_lst, e_y)
                        for item in lst:
                            if item not in args:
                                final_expression_dict[e_x] = ''
                print(expression_dict)
                print(final_expression_dict)
                encoded_dict = pickle.dumps(final_expression_dict)
                r.hset(name="company::expressions", key="{}::{}".format(slug, pk), value=encoded_dict)
            except (pickle.PicklingError, pickle.UnpicklingError, pickle.PickleError) as e:
                print(e)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


@task
def change_search_field(field, pk, slug):
    print(field, pk, slug)
    name = 'company::search_fields'
    key = '{}::{}'.format(slug, pk)
    if field == 'None':
        if r.hexists(name, key):
            r.hdel(name, key)
            cursor = 0
            while True:
                result_tuple = r.hscan(name='{}::{}'.format(pk, 'search_fields'), cursor=cursor)
                for val in result_tuple[1].values():
                    n = '{}::{}'.format(pk, val.decode())
                    r.delete(n)
                if result_tuple[0] == 0:
                    break
                else:
                    cursor = result_tuple[0]
    else:
        print('ko')
        print(r.hexists(name, key))
        if r.hexists(name, key):
            r.hset(name, key, field)
            cursor = 0
            while True:
                print('ks')
                result_tuple = r.hscan(name='{}::{}'.format(pk, 'search_fields'), cursor=cursor)
                for key, val in result_tuple[1].items():
                    if key.decode() != 'last_index':
                        r.hdel('{}::{}'.format(pk, 'search_fields'), key.decode())
                        n = '{}::{}'.format(pk, val.decode())
                        new_key = r.hget(n, key=field)
                        print(new_key)
                        if new_key.decode() != '':
                            r.hset(name='{}::{}'.format(pk, 'search_fields'), key=new_key.decode(), value=val.decode())
                if result_tuple[0] == 0:
                    break
                else:
                    cursor = result_tuple[0]
        else:
            r.hset(name, key, field)
