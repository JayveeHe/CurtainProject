# coding:utf-8
import leancloud
import time
from leancloud import Object
from leancloud import Query
from requests.packages import urllib3


def leancloud_init():
    '''
    leancloud初始化
    :return:
    '''
    urllib3.disable_warnings()
    leancloud.init('lXyQBue2G2I80NX9OIFY7TRk', 'NkLOGPRHeVrFdJOQiDIGVGJ7')


def add_data(page, time, content, user_id):
    '''
    插入弹幕
    :param page:
    :param time:
    :param content:
    :param user_id:
    :return:
    '''
    curtain_object = Object.extend('CurtainObject')
    object = curtain_object()
    object.set('page', page)
    object.set('time', time)
    object.set('content', content)
    object.set('user_id', user_id)
    object.save()


def query_data(page, user_id, cur_time):
    '''
    查询弹幕
    :param page:
    :param user_id:
    :param cur_time:
    :return: 弹幕数据
    '''
    last_post_time = update_user_info(page, user_id, cur_time)
    data = list()
    curtain_object = Object.extend('CurtainObject')
    query = Query(curtain_object)
    query.equal_to('page', page)
    query.greater_than('time', last_post_time)
    query.less_than('time', cur_time)
    query.ascending('time')
    results = query.find()
    for result in results:
        data.append({'content': result.get('content'), 'timestamp': result.get('time')})
    return data


def update_user_info(page_url, user_id, cur_time):
    '''
    更新user数据，并返回上一次更新的时间
    :param page_url:
    :param user_id:
    :param cur_time:
    :return: 该用户上一次更新的时间戳
    '''
    cls_user = Object.extend('UserInfo')
    query = Query(cls_user)
    query.equal_to('user_id', user_id)
    try:
        result = query.first()
    except Exception, e:
        result = None
    if result == None:
        user_object = cls_user()
        user_object.set('user_id', user_id)
        user_object.set('last_post_time', cur_time)
        user_object.set('page_url', page_url)
        user_object.set('status', 'active')
        user_object.save()
        return cur_time
    else:
        last_t = result.get('last_post_time')
        result.set('last_post_time', cur_time)
        result.set('status', 'active')
        result.set('page_url', page_url)
        result.save()
        return last_t


def update_page_info(page_url, user_id):
    '''
    更新页面数据，暂不使用
    :param page_url:
    :param user_id:
    :return:
    '''
    cls_page = Object.extend('UserInPage')
    query_page = Query(cls_page)
    query_page.equal_to('page_url', page_url)
    try:
        result = query_page.first()
    except Exception, e:
        result = None
    if result == None:
        page_object = cls_page()
        page_object.set('page_url', page_url)
        page_object.set('user_data', {user_id: 'active'})
        page_object.set('user_num', 1)
        page_object.save()
    else:
        user_dict = result.get('user_data')
        user_dict[user_id] = 'active'
        result.set('user_data', user_dict)
        result.set('user_num', result.get('user_num') + 1)
        result.save()


def delete_page_user(page_url, user_id):
    '''
    删除page下某个用户，暂未使用
    :param page_url:
    :param user_id:
    :return:
    '''
    cls_page = Object.extend('UserInPage')
    query_page = Query(cls_page)
    query_page.equal_to('page_url', page_url)
    result = query_page.first()
    user_dict = result.get('user_data')
    del user_dict[user_id]
    result.set('user_data', user_dict)
    result.set('user_num', result.get('user_num') - 1)
    result.save()


def get_user_num(page_url):
    '''
    查询页面用户数
    :param page_url:
    :return: 当前页面用户数
    '''
    # cls_page = Object.extend('UserInPage')
    # query_page = Query(cls_page)
    # query_page.equal_to('page_url', page_url)
    # try:
    #     result = query_page.first()
    # except Exception, e:
    #     return 0
    # return result.get('user_num')
    cls_user = Object.extend('UserInfo')
    query_user = Query(cls_user)
    query_user.equal_to('page_url', page_url)
    query_user.equal_to('status', 'active')
    return query_user.count()


def refresh_page_info(page_url):
    '''
    刷新page下用户数，暂未使用
    :param page_url:
    :return:
    '''
    cls_page = Object.extend('UserInPage')
    query_page = Query(cls_page)
    query_page.equal_to('page_url', page_url)
    result = query_page.first()
    user_dict = result.get('user_data')
    i = 0
    for user_status in user_dict.values():
        if user_status == 'active':
            i += 1
    result.set('user_num', i)
    result.save()


def update_user_status():
    '''
    定时刷新用户数据，标记已过时的用户
    :return:
    '''
    cur_time = time.time()
    cls_user = Object.extend('UserInfo')
    query_user = Query(cls_user)
    query_user.less_than('last_post_time', cur_time - 5)
    query_user.equal_to('status', 'active')
    print query_user.count()
    user_results = query_user.find()
    # cls_page = Object.extend('UserInPage')
    # query_page = Query(cls_page)
    for user_result in user_results:
        user_result.set('status', 'inactive')
        user_result.save()
        # page_url = user_result.get('page_url')
        # user_id = user_result.get('user_id')
        # user_result.destroy()

        # query_page.equal_to('page_url', page_url)
        # page_result = query_page.first()
        # page_dict = page_result.get('user_data')
        # if user_id in page_dict.keys():
        #     del page_dict[user_id]
        #     page_result.set('user_num', page_result.get('user_num') - 1)
        #     page_result.set('user_data', page_dict)
        # page_result.save()