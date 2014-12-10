import os
import webapp2
from webapp2_extras import auth, sessions

ADMINS = []
current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, '../admin.txt')) as f:
    ADMINS = set([l.strip() for l in f])


class LoginRequiredMixin(object):

    def dispatch(self, *args, **kwargs):
        self.session_store = sessions.get_store(request=self.request)
        if not self.auth.get_user_by_session():
            #self.redirect(users.create_login_url(self.request.url))
            self.redirect('/_ah/login_required?continue=%s' % self.request.url)
        else:
            user = self.current_user
            user_id = user.email.split('@')[0]
            user.user_id = user_id
            user.is_admin = user_id in ADMINS
            self.context = {
                'user': user,
                'user_id': user_id,
                'request': self.request,
            }
            super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

    @webapp2.cached_property
    def current_user(self):
        user_dict = self.auth.get_user_by_session()
        return self.auth.store.user_model.get_by_id(user_dict['user_id'])

    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()


class AdminRequiredMixin(object):

    def dispatch(self, *args, **kwargs):
        user = self.context.get('user')
        print 'admin check', user and user.user_id in ADMINS
        print user.user_id
        if user and user.is_admin:
            user.is_admin = True
            self.context['user'] = user
            return super(AdminRequiredMixin, self).dispatch(*args, **kwargs)
        else:
            self.error(403)
            self.response.write('You don\'t have this permission.')

